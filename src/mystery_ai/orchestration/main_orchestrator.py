import logging
import json # Added for dumping dict to JSON string
from typing import List, Dict, Any, Optional

from ..core.data_models import CaseContext, VictimProfile, SuspectProfile, MMO, Suspect
from ..agents.case_initializer import case_initializer_agent
from ..agents.suspect_generator import suspect_generator_agent
from ..agents.mmo_generator import mmo_generator_agent

from agents import Runner, ModelSettings # OpenAI Agents SDK components

logger = logging.getLogger(__name__)

def run_generation_pipeline(theme: str, trace_id: str) -> Optional[CaseContext]:
    """
    Main orchestration function for the mystery generation pipeline.

    Args:
        theme (str): The theme for the mystery.
        trace_id (str): The unique trace ID for this entire run.

    Returns:
        Optional[CaseContext]: The populated CaseContext object, or None if a critical step fails.
    """
    logger.info(f"Orchestration pipeline started for theme: '{theme}'. Trace ID: {trace_id}")

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

    # ----- EPIC 3: Killer Selection, MMO Mod, Evidence (Placeholder) -----
    logger.info("[Orchestrator] === Stage: Killer Sel, MMO Mod, Evidence (Epic 3) - Placeholder ===")
    # ... logic for Epic 3 agents ...
    
    # ----- EPIC 4: Final Output Generation (Placeholder) -----
    logger.info("[Orchestrator] === Stage: JSON Output (Epic 4) - Placeholder ===")
    logger.info("Orchestration pipeline (Epic 1 & 2 parts) complete.")
    
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