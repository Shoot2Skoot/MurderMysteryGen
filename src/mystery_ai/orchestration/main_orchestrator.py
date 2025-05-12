"""
Main orchestration module for the Murder Mystery Generation system.

This module coordinates the entire generation pipeline, handling the flow of data between
various agents and ensuring the creation of a complete, coherent murder mystery narrative.
It manages the initialization, character generation, MMO creation, evidence generation,
and final mystery output.
"""

import json  # Added for dumping dict to JSON string
import logging
import os  # For path operations
import random  # Added for random selection
import datetime # Moved from generate_filename
from typing import List, Optional

from agents import Runner

from ..agents.case_initializer import case_initializer_agent
from ..agents.evidence_generator import (
    evidence_generator_agent,
    prepare_evidence_generation_input,
)
from ..agents.killer_selector import select_killer_randomly  # Direct function for MVP
from ..agents.mmo_generator import mmo_generator_agent
from ..agents.mmo_modifier import mmo_modifier_agent
from ..agents.pre_initialization_ideation_agent import (
    ThematicNameLists,
    pre_initialization_ideation_agent,
)
from ..agents.suspect_generator import suspect_generator_agent
from ..core.data_models import (
    CaseContext,
    EvidenceItem,
    MMO,  # Added for type hinting if needed, assumed from context
    ModifiedMMOElement,
    Suspect,
    SuspectProfile,
    VictimProfile,
)

logger = logging.getLogger(__name__)

OUTPUT_DIRECTORY = "generated_mysteries"
# Added for master lists path
CONFIG_DIRECTORY = os.path.join("config", "master_lists")
# Configurable number of items to select for sub-lists
NUM_ATTRIBUTE_OPTIONS = 3
# Number of names to include in the random sample for victim agent
VICTIM_NAME_SAMPLE_SIZE = 3
# Number of names to include in the random sample for suspect agent
SUSPECT_NAME_SAMPLE_SIZE = 8
NUM_EVIDENCE_CATEGORY_OPTIONS = 5 # Number of evidence categories to provide to the agent


# Helper function to load master lists
def _load_master_list(filename: str, list_key: str) -> List[str]:
    """Loads a master list from a JSON file."""
    # Construct the full path relative to the project root.
    # Assumes the script is run from a context where 'MurderMysteryGen' is accessible
    # or this path needs adjustment based on execution context.
    # A more robust solution might use __file__ to determine base path.

    # Navigate three levels up from src/mystery_ai/orchestration to MurderMysteryGen
    base_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )

    file_path = os.path.join(base_path, CONFIG_DIRECTORY, filename)

    logger.debug("Attempting to load master list from: %s", file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as f: # Specify encoding
            data = json.load(f)
            master_list = data.get(list_key, [])
            if not master_list:
                logger.warning(
                    "Master list '%s' is empty or not found in %s.", list_key, filename
                )
            else:
                logger.info(
                    "Successfully loaded %d items for '%s' from %s.",
                    len(master_list),
                    list_key,
                    filename,
                )
                logger.debug("First 3 items from '%s': %s", list_key, master_list[:3])
            return master_list
    except FileNotFoundError:
        logger.error("Master list file not found: %s", file_path)
        return []
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from master list file: %s", file_path)
        return []
    except Exception: # Removed 'as e'
        logger.exception( # Use logger.exception to include traceback
            "Unexpected error loading master list '%s' from %s", filename, file_path
        )
        return []


# Helper function to sample random names from the full list
def _sample_names(names_list: List[str], sample_size: int) -> List[str]:
    """
    Takes a random sample of names from the provided list.

    Args:
        names_list: The full list of names to sample from.
        sample_size: Number of names to include in the sample.

    Returns:
        A list containing randomly sampled names.
    """
    if not names_list:
        logger.warning("Empty names list provided for sampling.")
        return []

    # Ensure we don't try to sample more names than exist in the list
    actual_sample_size = min(sample_size, len(names_list))

    # Take a random sample
    sampled_names = random.sample(names_list, actual_sample_size)
    logger.debug(
        "Sampled %d names from list of %d", len(sampled_names), len(names_list)
    )

    return sampled_names


def ensure_output_directory():
    """Ensures the output directory for JSON files exists."""
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
        logger.info("Created output directory: %s", OUTPUT_DIRECTORY)


def generate_filename(theme: str) -> str:
    """Generates a unique filename for the mystery JSON output."""
    # Sanitize theme for filename
    safe_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -")
    sanitized_theme = "".join(c for c in theme if c in safe_chars).strip()
    safe_theme = sanitized_theme.replace(" ", "_")
    # Use datetime directly here since it's only needed for the timestamp
    # import datetime # Removed, moved to top
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(OUTPUT_DIRECTORY, f"mystery_{safe_theme}_{timestamp}.json")


# --- Stage Helper Functions ---

def _run_pre_initialization_stage(theme: str, case_context: CaseContext) -> bool:
    """Runs the pre-initialization stage to generate thematic names."""
    logger.info(
        "[Orchestrator] --- Stage: Generating Thematic Name Lists (Story 6.1 & 6.2) ---"
    )
    try:
        name_lists_result = Runner.run_sync(
            pre_initialization_ideation_agent,
            input=theme
        )
        if name_lists_result and name_lists_result.final_output:
            name_lists = name_lists_result.final_output_as(ThematicNameLists)
            case_context.thematic_first_names = name_lists.first_names
            case_context.thematic_last_names = name_lists.last_names
            logger.info(
                "PreInitAgent completed. Generated %d first names and %d last names.",
                len(case_context.thematic_first_names),
                len(case_context.thematic_last_names),
            )
            if case_context.thematic_first_names and case_context.thematic_last_names:
                sample_first = list(case_context.thematic_first_names)[:5]
                sample_last = list(case_context.thematic_last_names)[:5]
                logger.info(
                    "Sample first names: %s", ", ".join(sample_first)
                )
                logger.info(
                    "Sample last names: %s", ", ".join(sample_last)
                )
            return True
        else:
            logger.error("PreInitAgent failed to produce thematic name lists.")
            return False
    except Exception: # Removed 'as e'
        logger.exception("Error running PreInitializationIdeationAgent") # Use exception
        return False


def _load_and_select_attributes() -> Optional[dict]:
    """Loads master attribute lists and selects sub-lists for the agents."""
    logger.info(
        "[Orchestrator] --- Stage: Loading & Selecting Attributes (Story 5.2) ---"
    )
    # Load Master Lists
    cod_list = _load_master_list("cause_of_death.json", "causes_of_death")
    motive_list = _load_master_list("motive_categories.json", "motive_categories")
    occupation_list = _load_master_list(
        "occupation_archetypes.json", "occupation_archetypes"
    )
    personality_list = _load_master_list(
        "personality_archetypes.json", "personality_archetypes"
    )
    # Load the new evidence categories list (Story 7.1)
    evidence_categories_master_list = _load_master_list( # Renamed for clarity
        "evidence_categories.json", "evidence_categories"
    )

    if not all([cod_list, motive_list, occupation_list, personality_list, evidence_categories_master_list]):
        logger.error("One or more master attribute lists (including evidence categories) failed to load.")
        return None

    # Select Sub-lists
    def _safe_sample(lst: List[str], k: int) -> List[str]:
        return random.sample(lst, min(k, len(lst)))

    selected_causes = _safe_sample(cod_list, NUM_ATTRIBUTE_OPTIONS)
    selected_motives = _safe_sample(motive_list, NUM_ATTRIBUTE_OPTIONS)
    selected_occupations = _safe_sample(occupation_list, NUM_ATTRIBUTE_OPTIONS)
    selected_personalities = _safe_sample(personality_list, NUM_ATTRIBUTE_OPTIONS)
    selected_evidence_categories = _safe_sample( # Select sub-list for evidence categories
        evidence_categories_master_list, NUM_EVIDENCE_CATEGORY_OPTIONS
    )

    attribute_options = {
        "cause_of_death_options": selected_causes,
        "motive_category_options": selected_motives,
        "occupation_archetype_options": selected_occupations,
        "personality_archetype_options": selected_personalities,
        "evidence_category_options": selected_evidence_categories # Add to dict
    }
    # Use dumps with indent for multi-line logging of the dict
    logger.info("Selected attribute options:")
    logger.info(json.dumps(attribute_options, indent=2))
    return attribute_options


def _run_case_initialization_stage(
    case_context: CaseContext, attribute_options: dict
) -> bool:
    """Runs the case initialization stage to generate the victim profile."""
    logger.info("[Orchestrator] === Stage: Case Initialization (Epic 1) ===")
    try:
        sampled_first = _sample_names(
            case_context.thematic_first_names, VICTIM_NAME_SAMPLE_SIZE
        )
        sampled_last = _sample_names(
            case_context.thematic_last_names, VICTIM_NAME_SAMPLE_SIZE
        )
        logger.info(
            "Sending sample of %d first/%d last names to CaseInitAgent",
            len(sampled_first), len(sampled_last)
        )

        case_init_input = {
            "theme": case_context.theme,
            "attribute_options": attribute_options,
            "thematic_names": {
                "first_names": sampled_first,
                "last_names": sampled_last,
            },
        }
        input_json = json.dumps(case_init_input)
        logger.debug("CaseInitializationAgent input: %s", input_json)
        result = Runner.run_sync(
            case_initializer_agent,
            input=input_json
        )

        if result and result.final_output:
            case_context.victim = result.final_output_as(VictimProfile)
            victim_name = getattr(case_context.victim, 'name', 'N/A')
            logger.info(
                "CaseInitAgent completed. Victim: %s", victim_name
            )
            # Log chosen categories
            if case_context.victim:
                cod = case_context.victim.chosen_cause_of_death_category
                occ = case_context.victim.chosen_occupation_archetype
                pers = case_context.victim.chosen_personality_archetype
                logger.info("  Chosen CoD: %s", cod)
                logger.info("  Chosen Occupation: %s", occ)
                logger.info("  Chosen Personality: %s", pers)
            return True
        else:
            logger.error("CaseInitAgent failed to produce a victim profile.")
            return False
    except Exception: # Removed 'as e'
        logger.exception("Error running CaseInitializationAgent") # Use exception
        return False


def _run_suspect_mmo_generation_stage(
    case_context: CaseContext, attribute_options: dict
) -> bool:
    """Runs suspect generation and MMO generation for each suspect."""
    logger.info("[Orchestrator] === Stage: Suspect & MMO Generation (Epic 2) ===")

    if not case_context.victim:
        logger.error("Victim profile missing at start of Suspect/MMO stage.")
        return False

    generated_suspects: List[Suspect] = []
    try:
        sampled_first = _sample_names(
            case_context.thematic_first_names, SUSPECT_NAME_SAMPLE_SIZE
        )
        sampled_last = _sample_names(
            case_context.thematic_last_names, SUSPECT_NAME_SAMPLE_SIZE
        )
        logger.info(
            "Sending sample of %d first/%d last names to SuspectGenAgent",
            len(sampled_first), len(sampled_last)
        )

        suspect_gen_input_dict = {
            "theme": case_context.theme,
            "victim": case_context.victim.model_dump(),
            "motive_category_options": attribute_options.get("motive_category_options", []),
            "occupation_archetype_options": attribute_options.get("occupation_archetype_options", []),
            "personality_archetype_options": attribute_options.get("personality_archetype_options", []),
            "thematic_names": {
                "first_names": sampled_first,
                "last_names": sampled_last,
            },
        }
        suspect_gen_input_json = json.dumps(suspect_gen_input_dict)
        logger.debug("SuspectGenerationAgent input: %s", suspect_gen_input_json)

        suspect_profiles_result = Runner.run_sync(
            suspect_generator_agent,
            input=suspect_gen_input_json
        )

        if not (suspect_profiles_result and suspect_profiles_result.final_output):
            logger.error("SuspectGenerationAgent failed to produce output.")
            return False

        suspect_profiles: List[SuspectProfile] = suspect_profiles_result.final_output
        logger.info("Generated %d suspect profiles.", len(suspect_profiles))

        for i, s_profile in enumerate(suspect_profiles):
            logger.info(
                "Generating MMO for suspect %d/%d: %s",
                 i + 1, len(suspect_profiles), s_profile.name
            )
            mmo_gen_input_dict = {
                "theme": case_context.theme,
                "victim": case_context.victim.model_dump(),
                "suspect_profile": s_profile.model_dump(),
            }
            mmo_gen_input_json = json.dumps(mmo_gen_input_dict)
            logger.debug("MMOGenerationAgent input: %s", mmo_gen_input_json)

            mmo_result = Runner.run_sync(
                mmo_generator_agent,
                input=mmo_gen_input_json
            )

            if not (mmo_result and mmo_result.final_output):
                logger.error(
                    "MMOGenerationAgent failed for suspect: %s", s_profile.name
                )
                return False  # Halt on MMO failure

            # Assuming final_output is already parsed if output_type=MMO was set
            current_mmo: MMO = mmo_result.final_output
            full_suspect = Suspect(profile=s_profile, original_mmo=current_mmo)
            generated_suspects.append(full_suspect)

        case_context.suspects = generated_suspects
        logger.info(
            "Successfully generated MMOs for %d suspects.", len(generated_suspects)
        )
        return True

    except Exception: # Removed 'as e'
        logger.exception("Error during Suspect/MMO Generation (Epic 2)") # Use exception
        return False


def _run_killer_mod_evidence_stage(case_context: CaseContext, attribute_options: dict) -> bool:
    """Runs killer selection, MMO modification, and evidence generation."""
    stage_name = "[Orchestrator] === Stage: Killer Sel/MMO Mod/Evidence (Epic 3) ==="
    logger.info(stage_name)

    evidence_category_options_for_agent = attribute_options.get("evidence_category_options", [])

    try:
        # --- Killer Selection ---
        if not case_context.suspects:
            logger.error("No suspects available for killer selection.")
            return False
        case_context.suspects = select_killer_randomly(case_context.suspects)
        killer = case_context.get_killer()
        if killer:
            logger.info("Killer selected: %s", killer.profile.name)
        else:
            logger.error("Failed to select a killer.")
            return False

        # --- MMO Modification & Logging Chosen Categories ---
        logger.info("--- Processing Suspect Details & Modifying MMOs ---")
        for i, suspect in enumerate(case_context.suspects):
            log_prefix = f"Suspect {i+1} ({suspect.profile.name}, Killer: {suspect.is_killer})"
            logger.info(log_prefix)
            logger.info("  Chosen Motive: %s", suspect.profile.chosen_motive_category)
            if suspect.profile.chosen_occupation_archetype:
                logger.info(
                     "  Chosen Occupation: %s",
                     suspect.profile.chosen_occupation_archetype
                 )
            if suspect.profile.chosen_personality_archetype:
                logger.info(
                     "  Chosen Personality: %s",
                     suspect.profile.chosen_personality_archetype
                 )

            if not suspect.is_killer:
                logger.info("Modifying MMO for non-killer: %s", suspect.profile.name)
                element_types = ["means", "motive", "opportunity"]
                chosen_element = random.choice(element_types)
                original_value = getattr(suspect.original_mmo, chosen_element)

                mmo_mod_input_dict = {
                    "theme": case_context.theme,
                    "suspect_profile": suspect.profile.model_dump(),
                    "original_mmo": suspect.original_mmo.model_dump(),
                    "element_to_modify": chosen_element,
                    "original_element_value_to_modify": original_value
                }
                mmo_mod_input_json = json.dumps(mmo_mod_input_dict)
                logger.debug("MMOModifierAgent input: %s", mmo_mod_input_json)

                mmo_mod_result = Runner.run_sync(
                    mmo_modifier_agent,
                    input=mmo_mod_input_json
                )
                if mmo_mod_result and mmo_mod_result.final_output:
                    mod_element = mmo_mod_result.final_output_as(ModifiedMMOElement)
                    suspect.modified_mmo_elements.append(mod_element)
                    logger.info(
                        "MMO for %s modified (element: %s).",
                         suspect.profile.name, mod_element.element_type.value
                    )
                else:
                    logger.error(
                        "MMOModificationAgent failed for suspect: %s",
                         suspect.profile.name
                    )
                    return False # Halt on modification failure

        # --- Evidence Generation ---
        logger.info("--- Generating Evidence ---")
        all_evidence: List[EvidenceItem] = []
        for suspect in case_context.suspects:
            logger.info("Generating evidence for suspect: %s", suspect.profile.name)
            evidence_gen_input = prepare_evidence_generation_input(
                case_context, 
                suspect,
                evidence_category_options_for_agent # Pass the options
            )
            evidence_gen_input_json = json.dumps(evidence_gen_input)
            logger.debug(
                "EvidenceGenerationAgent input: %s", evidence_gen_input_json
            )
            evidence_result = Runner.run_sync(
                evidence_generator_agent,
                input=evidence_gen_input_json
            )
            if evidence_result and evidence_result.final_output:
                # Assuming output_type=List[EvidenceItem]
                evidence_list = evidence_result.final_output
                all_evidence.extend(evidence_list)
                logger.info(
                    "Generated %d evidence items for %s.",
                    len(evidence_list), suspect.profile.name
                )
            else:
                logger.error(
                    "EvidenceGenerationAgent failed for suspect: %s",
                    suspect.profile.name
                )
                return False # Halt on evidence failure

        case_context.evidence_items = all_evidence
        logger.info(
            "Total evidence items generated: %d.", len(case_context.evidence_items)
        )
        return True

    except Exception: # Removed 'as e'
        logger.exception("Error during Epic 3 processing") # Use exception
        return False


def _write_output_file(case_context: CaseContext) -> None:
    """Writes the final CaseContext to a JSON file."""
    logger.info("[Orchestrator] === Stage: JSON Output Generation (Epic 4) ===")
    try:
        ensure_output_directory() # Ensure directory exists before writing
        output_filename = generate_filename(case_context.theme)
        with open(output_filename, "w", encoding="utf-8") as f: # Specify encoding
            f.write(case_context.model_dump_json(indent=2))
        logger.info("Successfully wrote mystery to %s", output_filename)
    except Exception: # Removed 'as e'
        logger.exception("Failed to write output JSON to file") # Use exception
        # Don't return False here, as the context might still be valid


# --- Main Pipeline ---

def run_generation_pipeline(
    theme: str, trace_id: Optional[str] = None
) -> Optional[CaseContext]:
    """
    Main function to run the complete mystery generation pipeline.

    Args:
        theme: The theme for the mystery.
        trace_id: Optional trace ID for tracking the pipeline execution.

    Returns:
        CaseContext object with the fully generated mystery, or None if a
        critical error occurs.
    """
    case_context = CaseContext(theme=theme)
    logger.info(
        "Orchestration pipeline started for theme: '%s'. Trace ID: %s",
        theme, trace_id
    )

    # Stage: Pre-Initialization
    if not _run_pre_initialization_stage(theme, case_context):
        logger.error("Pre-initialization stage failed. Aborting pipeline.")
        return None

    # Stage: Load & Select Attributes
    attribute_options = _load_and_select_attributes()
    if not attribute_options:
        logger.error("Loading/selecting attributes failed. Aborting pipeline.")
        return None

    # Stage: Case Initialization
    if not _run_case_initialization_stage(case_context, attribute_options):
        logger.error("Case initialization stage failed. Aborting pipeline.")
        return None
    if not case_context.victim: # Double check after stage completion
        logger.error("Victim profile missing after initialization. Aborting.")
        return None
    # Linter might still complain here due to complex type inference
    victim_name = getattr(case_context.victim, 'name', 'UNKNOWN')
    logger.info(f"Stage complete: Victim '{victim_name}' generated.")


    # Stage: Suspect & MMO Generation
    if not _run_suspect_mmo_generation_stage(case_context, attribute_options):
        logger.error("Suspect/MMO generation stage failed. Aborting pipeline.")
        return None
    if not case_context.suspects: # Double check after stage completion
        logger.error("No suspects generated. Aborting pipeline.")
        return None
    logger.info(
        "Stage complete: %d suspects with MMOs generated.", len(case_context.suspects)
    )

    # Stage: Killer Selection, MMO Modification, Evidence Generation
    if not _run_killer_mod_evidence_stage(case_context, attribute_options):
        logger.error("Killer selection/MMO mod/Evidence stage failed. Aborting.")
        return None
    logger.info("Stage complete: Killer selected, MMOs modified, Evidence generated.")

    # Stage: Output Generation
    _write_output_file(case_context) # Write output even if errors occurred

    logger.info("Orchestration pipeline finished successfully.")
    return case_context


# Example of how main.py might call this (refined in main.py later)
if __name__ == "__main__":
    # This is for direct testing of the orchestrator
    import uuid

    from dotenv import load_dotenv

    # Configure logging for this test run
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" # UPPER_CASE
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    # Ensure the module logger is used if it was already configured
    logger = logging.getLogger(__name__)

    # Load environment variables
    # Use os imported at the module level
    PROJ_ROOT = os.path.abspath( # UPPER_CASE
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )
    DOTENV_PATH = os.path.join(PROJ_ROOT, ".env") # UPPER_CASE
    if os.path.exists(DOTENV_PATH):
        load_dotenv(dotenv_path=DOTENV_PATH)
        logger.info(".env file loaded from %s", DOTENV_PATH)
    else:
        logger.warning(".env file not found at %s", DOTENV_PATH)

    # Test theme
    TEST_THEME = "Haunted Library" # UPPER_CASE
    TEST_TRACE_ID = f"trace_orchestrator_test_{uuid.uuid4().hex}" # UPPER_CASE

    # Run the orchestration pipeline
    print(f"\nRunning orchestration pipeline with theme: {TEST_THEME}")
    final_result = run_generation_pipeline(TEST_THEME, TEST_TRACE_ID)

    print("\n--- Orchestration Test Output ---")
    if final_result:
        print("Pipeline completed successfully!")
        print(f"Theme: {final_result.theme}")
        # Add check for victim before accessing name
        VICTIM_NAME = "N/A" # UPPER_CASE
        if final_result.victim:
             # Linter might still complain about type inference here
            VICTIM_NAME = getattr(final_result.victim, 'name', 'N/A')
        print(f"Victim: {VICTIM_NAME}")
        num_suspects = len(final_result.suspects)
        num_evidence = len(final_result.evidence_items)
        print(f"Suspects: {num_suspects}")
        print(f"Evidence items: {num_evidence}")
        first_names = final_result.thematic_first_names[:5]
        last_names = final_result.thematic_last_names[:5]
        print(f"Thematic first names (sample): {', '.join(first_names)}")
        print(f"Thematic last names (sample): {', '.join(last_names)}")
    else:
        print("Pipeline failed!")
    print("------------------------------")
