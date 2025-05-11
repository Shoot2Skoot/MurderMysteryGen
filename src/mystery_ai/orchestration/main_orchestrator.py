import logging
import json # Added for dumping dict to JSON string
from typing import List, Dict, Any, Optional
import os # For path operations
import datetime # For timestamp in filename

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

    # ----- EPIC 1: Case Initialization ----- 
    logger.info("[Orchestrator] === Stage: Case Initialization (Epic 1) ===")
    try:
        logger.info(f"Running CaseInitializationAgent for theme: {theme}")
        result = Runner.run_sync(case_initializer_agent, input=theme)
        if result and result.final_output:
            case_context.victim = result.final_output_as(VictimProfile)
            logger.info(f"CaseInitializationAgent completed. Victim: {getattr(case_context.victim, 'name', 'N/A')}")
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
            "victim": case_context.victim.model_dump()
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