import logging
import json # Added for dumping dict to JSON string
from typing import List, Dict, Any, Optional
import os # For path operations
import datetime # For timestamp in filename
import random # Added for random selection

from ..core.data_models import CaseContext, VictimProfile, SuspectProfile, MMO, Suspect, ModifiedMMOElement, EvidenceItem, MMOElementType
from ..agents.case_initializer import case_initializer_agent
from ..agents.suspect_generator import suspect_generator_agent
from ..agents.mmo_generator import mmo_generator_agent
from ..agents.killer_selector import select_killer_randomly # Direct function for MVP
from ..agents.mmo_modifier import mmo_modifier_agent, prepare_mmo_modification_input
from ..agents.evidence_generator import evidence_generator_agent, prepare_evidence_generation_input

from agents import Runner, ModelSettings # OpenAI Agents SDK components

logger = logging.getLogger(__name__)

OUTPUT_DIRECTORY = "generated_mysteries"
CONFIG_DIRECTORY = "config/master_lists" # Added for master lists path
NUM_ATTRIBUTE_OPTIONS = 3 # Configurable number of items to select for sub-lists

# Helper function to load master lists
def _load_master_list(filename: str, list_key: str) -> List[str]:
    """Loads a master list from a JSON file."""
    # Construct the full path relative to the project root or a known base directory
    # Assuming the script is run from a context where 'MurderMysteryGen' is accessible
    # or this path needs adjustment based on execution context.
    # For now, let's assume 'CONFIG_DIRECTORY' is relative to the project root.
    # A more robust solution might use __file__ to determine base path if this script is part of a package.
    
    # Simplified path for now, assuming execution from project root or similar
    # For a file like 'MurderMysteryGen/config/master_lists/cause_of_death.json'
    # If this script is 'MurderMysteryGen/src/mystery_ai/orchestration/main_orchestrator.py'
    # then relative path from this script to 'config' is '../../config/master_lists'
    
    # Let's assume CONFIG_DIRECTORY is a subdirectory of MurderMysteryGen,
    # and this script might be run from the MurderMysteryGen directory.
    # This path construction needs to be robust.
    # For now:
    base_path = os.path.join(os.path.dirname(__file__), "..", "..", "..") # Adjust if necessary to reach project root
    # This navigates three levels up from src/mystery_ai/orchestration to MurderMysteryGen
    
    file_path = os.path.join(base_path, CONFIG_DIRECTORY, filename)
    
    logger.debug(f"Attempting to load master list from: {file_path}")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            master_list = data.get(list_key, [])
            if not master_list:
                logger.warning(f"Master list '{list_key}' is empty or not found in {filename}.")
            logger.info(f"Successfully loaded {len(master_list)} items for '{list_key}' from {filename}.")
            if master_list:
                 logger.debug(f"First 3 items from '{list_key}': {master_list[:3]}")
            return master_list
    except FileNotFoundError:
        logger.error(f"Master list file not found: {file_path}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from master list file: {file_path}")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred while loading master list {file_path}: {e}")
        return []

def ensure_output_directory():
    """Ensures the output directory for JSON files exists."""
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
        logger.info(f"Created output directory: {OUTPUT_DIRECTORY}")

def generate_filename(theme: str) -> str:
    """Generates a unique filename for the mystery JSON output."""
    # Sanitize theme for filename
    safe_theme = "".join(c if c.isalnum() or c in (' ', '-') else '' for c in theme).rstrip()
    safe_theme = safe_theme.replace(' ', '_')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(OUTPUT_DIRECTORY, f"mystery_{safe_theme}_{timestamp}.json")

def run_generation_pipeline(theme: str, trace_id: str) -> Optional[CaseContext]:
    """
    Main orchestration function for the mystery generation pipeline.
    Returns CaseContext or None if a critical step fails.
    Also writes the final CaseContext to a JSON file if successful.
    """
    logger.info(f"Orchestration pipeline started for theme: '{theme}'. Trace ID: {trace_id}")
    ensure_output_directory() # Ensure output directory exists
    case_context = CaseContext(theme=theme)

    # ----- Load Master Attribute Lists (Story 5.2) -----
    logger.info("[Orchestrator] --- Stage: Loading Master Attribute Lists (Story 5.2) ---")
    cause_of_death_list = _load_master_list("cause_of_death.json", "causes_of_death")
    motive_categories_list = _load_master_list("motive_categories.json", "motive_categories")
    occupation_archetypes_list = _load_master_list("occupation_archetypes.json", "occupation_archetypes")
    personality_archetypes_list = _load_master_list("personality_archetypes.json", "personality_archetypes")

    # Check if all lists were loaded successfully (or handle partially loaded lists)
    if not all([cause_of_death_list, motive_categories_list, occupation_archetypes_list, personality_archetypes_list]):
        logger.error("One or more master attribute lists failed to load. Cannot proceed with attribute sub-list selection.")
        # Depending on requirements, either return None or proceed without these options.
        # For Story 5.2, these are crucial for the CaseInitializationAgent input.
        return None

    # ----- Select Sub-lists of Attributes (Story 5.2) -----
    logger.info("[Orchestrator] --- Stage: Selecting Attribute Sub-lists (Story 5.2) ---")
    
    selected_causes = random.sample(cause_of_death_list, min(NUM_ATTRIBUTE_OPTIONS, len(cause_of_death_list)))
    selected_motives = random.sample(motive_categories_list, min(NUM_ATTRIBUTE_OPTIONS, len(motive_categories_list)))
    selected_occupations = random.sample(occupation_archetypes_list, min(NUM_ATTRIBUTE_OPTIONS, len(occupation_archetypes_list)))
    selected_personalities = random.sample(personality_archetypes_list, min(NUM_ATTRIBUTE_OPTIONS, len(personality_archetypes_list)))

    attribute_options_for_agent = {
        "cause_of_death_options": selected_causes,
        "motive_category_options": selected_motives,
        "occupation_archetype_options": selected_occupations, # Key name matches story 5.1
        "personality_archetype_options": selected_personalities, # Key name matches story 5.1
    }
    logger.info(f"Selected attribute options for CaseInitializationAgent: {json.dumps(attribute_options_for_agent, indent=2)}")
    # TODO (Story 5.3): Pass 'attribute_options_for_agent' to CaseInitializationAgent.
    # The agent's input signature and internal logic will need to be updated.

    # ----- EPIC 1: Case Initialization ----- 
    logger.info("[Orchestrator] === Stage: Case Initialization (Epic 1) ===")
    try:
        logger.info(f"Running CaseInitializationAgent for theme: {theme} with attribute options.")
        
        case_init_input = {
            "theme": theme,
            "attribute_options": attribute_options_for_agent
        }
        logger.debug(f"CaseInitializationAgent input: {json.dumps(case_init_input)}")
        result = Runner.run_sync(case_initializer_agent, input=json.dumps(case_init_input))
        
        if result and result.final_output:
            case_context.victim = result.final_output_as(VictimProfile)
            logger.info(f"CaseInitializationAgent completed. Victim: {getattr(case_context.victim, 'name', 'N/A')}")
            # Log the chosen categories for verification
            if case_context.victim:
                logger.info(f"  Chosen CoD Category: {case_context.victim.chosen_cause_of_death_category}")
                # Removed motive category logging since it's now per-suspect
                logger.info(f"  Chosen Occupation Archetype: {case_context.victim.chosen_occupation_archetype}")
                logger.info(f"  Chosen Personality Archetype: {case_context.victim.chosen_personality_archetype}")
        else:
            logger.error("CaseInitializationAgent failed to produce a victim profile.")
            return None # Critical failure
    except Exception as e:
        logger.error(f"Error running CaseInitializationAgent: {e}", exc_info=True)
        return None # Critical failure
    
    if not case_context.victim:
        logger.error("Victim profile is missing after case initialization. Cannot proceed.")
        return None
    logger.info(f"[Orchestrator] CaseContext after Epic 1: Victim '{case_context.victim.name}' generated for theme '{case_context.theme}'")

    # ----- EPIC 2: Suspect & MMO Generation ----- 
    logger.info("[Orchestrator] === Stage: Suspect & MMO Generation (Epic 2) ===")
    generated_suspects: List[Suspect] = []
    try:
        logger.info("Running SuspectGenerationAgent...")
        suspect_gen_input_dict = {
            "theme": case_context.theme,
            "victim": case_context.victim.model_dump(),
            "motive_category_options": selected_motives  # Pass the motive options to the suspect generator
        }
        # Convert the input dictionary to a JSON string
        suspect_gen_input_json_str = json.dumps(suspect_gen_input_dict)
        logger.debug(f"SuspectGenerationAgent input (JSON string): {suspect_gen_input_json_str}")
        
        suspect_profiles_result = Runner.run_sync(suspect_generator_agent, input=suspect_gen_input_json_str)
        
        if not (suspect_profiles_result and suspect_profiles_result.final_output):
            logger.error("SuspectGenerationAgent failed to produce output.")
            return None # Critical failure

        # The output_type=List[SuspectProfile] should handle parsing the JSON list output from the LLM
        suspect_profiles: List[SuspectProfile] = suspect_profiles_result.final_output # No need for final_output_as here if output_type is set
        logger.info(f"SuspectGenerationAgent completed. Generated {len(suspect_profiles)} suspect profiles.")

        for i, s_profile in enumerate(suspect_profiles):
            logger.info(f"Processing suspect {i+1}/{len(suspect_profiles)}: {s_profile.name} for MMO generation.")
            mmo_gen_input_dict = {
                "theme": case_context.theme,
                "victim": case_context.victim.model_dump(),
                "suspect_profile": s_profile.model_dump()
            }
            # Convert the input dictionary to a JSON string
            mmo_gen_input_json_str = json.dumps(mmo_gen_input_dict)
            logger.debug(f"MMOGenerationAgent input (JSON string): {mmo_gen_input_json_str}")
            
            mmo_result = Runner.run_sync(mmo_generator_agent, input=mmo_gen_input_json_str)
            
            if not (mmo_result and mmo_result.final_output):
                logger.error(f"MMOGenerationAgent failed for suspect: {s_profile.name}")
                # Decide: skip this suspect or halt? For MVP, let's try to continue if some fail, but log it.
                # Or, more strictly, halt if any part fails.
                # For now, let's halt if an MMO isn't generated, as it's core.
                return None # Critical failure
            
            current_mmo = mmo_result.final_output # No need for final_output_as here
            logger.info(f"MMOGenerationAgent completed for suspect: {s_profile.name}")
            
            # Create the full Suspect object
            full_suspect = Suspect(profile=s_profile, original_mmo=current_mmo)
            generated_suspects.append(full_suspect)
        
        case_context.suspects = generated_suspects
        logger.info(f"Successfully generated MMOs for {len(generated_suspects)} suspects.")

    except Exception as e:
        logger.error(f"Error during Suspect/MMO Generation (Epic 2): {e}", exc_info=True)
        return None # Critical failure

    if not case_context.suspects or len(case_context.suspects) == 0:
        logger.error("No suspects were generated. Cannot proceed.")
        return None
    logger.info(f"[Orchestrator] CaseContext after Epic 2: {len(case_context.suspects)} suspects with MMOs generated.")

    # ----- EPIC 3: Killer Selection, MMO Modification, Evidence Generation -----
    logger.info("[Orchestrator] === Stage: Killer Selection & MMO Modification (Epic 3) ===")
    try:
        # Killer Selection (direct Python function for MVP)
        if not case_context.suspects:
            logger.error("No suspects available for killer selection.")
            return None
        case_context.suspects = select_killer_randomly(case_context.suspects)
        killer = case_context.get_killer()
        if killer:
            logger.info(f"Killer selected: {killer.profile.name}")
        else:
            logger.error("Failed to select a killer.")
            return None

        # MMO Modification for non-killers
        for i, suspect in enumerate(case_context.suspects):
            # Log the chosen categories for each suspect
            logger.info(f"Suspect {i+1}: {suspect.profile.name}")
            logger.info(f"  Chosen Motive Category: {suspect.profile.chosen_motive_category}")
            if suspect.profile.chosen_occupation_archetype:
                logger.info(f"  Chosen Occupation Archetype: {suspect.profile.chosen_occupation_archetype}")
            if suspect.profile.chosen_personality_archetype:
                logger.info(f"  Chosen Personality Archetype: {suspect.profile.chosen_personality_archetype}")
                
            if not suspect.is_killer:
                logger.info(f"Modifying MMO for non-killer: {suspect.profile.name}")
                mmo_mod_input_dict, chosen_element_type = prepare_mmo_modification_input(
                    victim=case_context.victim,
                    suspect=suspect
                )
                # Add theme to the input dict for mmo_modifier_agent, if its instructions expect it
                mmo_mod_input_dict["theme"] = case_context.theme 
                
                logger.debug(f"MMOModifierAgent input: {json.dumps(mmo_mod_input_dict)}")
                mmo_mod_result = Runner.run_sync(mmo_modifier_agent, input=json.dumps(mmo_mod_input_dict))
                
                if mmo_mod_result and mmo_mod_result.final_output:
                    modified_element = mmo_mod_result.final_output_as(ModifiedMMOElement)
                    suspect.modified_mmo_elements.append(modified_element)
                    logger.info(f"MMO for {suspect.profile.name} modified (element: {modified_element.element_type.value}).")
                else:
                    logger.error(f"MMOModificationAgent failed for suspect: {suspect.profile.name}")
                    # Optionally, decide if this is a critical failure for MVP
                    return None # For now, consider it critical
        logger.info("MMO modifications for non-killers complete.")

        # Evidence Generation
        logger.info("[Orchestrator] --- Stage: Evidence Generation (Epic 3) ---")
        all_evidence: List[EvidenceItem] = []
        for suspect in case_context.suspects:
            logger.info(f"Generating evidence for suspect: {suspect.profile.name} (Killer: {suspect.is_killer})")
            evidence_gen_input_dict = prepare_evidence_generation_input(case_context, suspect)
            logger.debug(f"EvidenceGenerationAgent input: {json.dumps(evidence_gen_input_dict)}")
            evidence_result = Runner.run_sync(evidence_generator_agent, input=json.dumps(evidence_gen_input_dict))

            if evidence_result and evidence_result.final_output:
                generated_evidence_for_suspect = evidence_result.final_output_as(List[EvidenceItem])
                all_evidence.extend(generated_evidence_for_suspect)
                logger.info(f"Generated {len(generated_evidence_for_suspect)} evidence items for {suspect.profile.name}.")
            else:
                logger.error(f"EvidenceGenerationAgent failed for suspect: {suspect.profile.name}")
                return None # Critical failure
        case_context.evidence_items = all_evidence
        logger.info(f"Total evidence items generated: {len(case_context.evidence_items)}.")

    except Exception as e:
        logger.error(f"Error during Epic 3 processing: {e}", exc_info=True)
        return None
    if not case_context.evidence_items: 
        # Allow empty evidence if generation for some suspects failed but we didn't halt earlier
        # However, our current logic halts on individual agent failures within Epic 3.
        logger.warning("No evidence items were generated. This might be an issue.")

    # ----- EPIC 4: Final Output Generation -----
    logger.info("[Orchestrator] === Stage: JSON Output Generation (Epic 4) ===")
    try:
        output_filename = generate_filename(case_context.theme)
        with open(output_filename, 'w') as f:
            # Use model_dump_json for direct serialization from Pydantic model to JSON string
            f.write(case_context.model_dump_json(indent=2))
        logger.info(f"Successfully wrote mystery to {output_filename}")
    except Exception as e:
        logger.error(f"Failed to write output JSON to file: {e}", exc_info=True)
        # Still return the case_context if generation was successful but file write failed
        # The main.py can still print it. The user will see the error about file writing.

    logger.info("Orchestration pipeline fully complete.") # Updated log message
    return case_context

# Example of how main.py might call this (actual call will be uncommented/refined in main.py later)
# if __name__ == '__main__':
#     # This is for direct testing of the orchestrator, assuming .env is loaded and logging set up
#     # from dotenv import load_dotenv
#     # import os
#     # project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
#     # dotenv_path = os.path.join(project_root, '.env')
#     # load_dotenv(dotenv_path=dotenv_path)
#     # logging.basicConfig(level=logging.INFO)
# 
#     test_theme = "Haunted Library"
#     test_trace_id = f"trace_orchestrator_test_{uuid.uuid4().hex}"
#     final_result = run_generation_pipeline(test_theme, test_trace_id)
#     print("\n--- Orchestrator Test Output ---")
#     print(final_result)
#     print("------------------------------") 