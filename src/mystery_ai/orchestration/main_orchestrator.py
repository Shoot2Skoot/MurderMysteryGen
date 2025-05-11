import logging

from ..core.data_models import CaseContext, VictimProfile
from ..agents.case_initializer import case_initializer_agent # Import the agent instance
from agents import Runner, ModelSettings # OpenAI Agents SDK components

logger = logging.getLogger(__name__)

def run_generation_pipeline(theme: str, trace_id: str) -> CaseContext:
    """
    Main orchestration function for the mystery generation pipeline.

    Args:
        theme (str): The theme for the mystery.
        trace_id (str): The unique trace ID for this entire run.

    Returns:
        CaseContext: The populated CaseContext object after initializiation.
    """
    logger.info(f"Orchestration pipeline started for theme: '{theme}'. Trace ID: {trace_id}")

    # Initialize the main data structure
    case_context = CaseContext(theme=theme, victim=None) # Suspects and evidence will be added later

    # ----- EPIC 1: Case Initialization ----- 
    logger.info("[Orchestrator] Current step: Case Initialization (Epic 1)")
    
    try:
        logger.info(f"Running CaseInitializationAgent for theme: {theme}")
        # The input for an agent expecting structured output via output_type is the content it processes.
        # The case_initializer_agent is instructed to take the theme as input.
        result = Runner.run_sync(case_initializer_agent, input=theme)
        
        if result and result.final_output:
            victim_profile_output = result.final_output_as(VictimProfile)
            case_context.victim = victim_profile_output
            logger.info(f"CaseInitializationAgent completed. Victim: {getattr(case_context.victim, 'name', 'N/A')}")
        else:
            logger.error("CaseInitializationAgent did not produce the expected output.")
            # Potentially raise an error or return a partially completed case_context
            # For MVP, logging and continuing with a None victim might be handled by subsequent checks
            # or simply lead to an incomplete final output, which is a form of failure.
            # Let's assume for now that if victim is None, it's an issue.
            raise ValueError("CaseInitializationAgent failed to produce a victim profile.")

    except Exception as e:
        logger.error(f"Error running CaseInitializationAgent: {e}", exc_info=True)
        # Re-raise the exception to halt the process if case initialization fails, as it's foundational.
        raise
    
    logger.info(f"[Orchestrator] CaseContext after Epic 1: Victim '{getattr(case_context.victim, "name", "Unknown")}' generated for theme '{case_context.theme}'")

    # ----- EPIC 2: Suspect & MMO Generation (Placeholder) -----
    logger.info("[Orchestrator] Next step: Suspect & MMO Generation (Epic 2) - Placeholder")
    # ... logic for Epic 2 agents, passing and updating case_context ...
    # case_context_after_epic2 = {**case_context_after_epic1, "suspects_placeholder": "List of suspects with MMOs from Epic 2"}
    # logger.info(f"[Placeholder] CaseContext after Epic 2 (simulated): {case_context_after_epic2}")

    # ----- EPIC 3: Killer Selection, MMO Mod, Evidence (Placeholder) -----
    logger.info("[Orchestrator] Next step: Killer Sel, MMO Mod, Evidence (Epic 3) - Placeholder")
    # ... logic for Epic 3 agents ...
    # case_context_after_epic3 = {**case_context_after_epic2, "killer_placeholder": "Designated Killer", "evidence_placeholder": "List of evidence"}
    # logger.info(f"[Placeholder] CaseContext after Epic 3 (simulated): {case_context_after_epic3}")
    
    # ----- EPIC 4: Final Output Generation (Placeholder) -----
    logger.info("[Orchestrator] Final step: JSON Output (Epic 4) - Placeholder")
    # ... logic to serialize case_context to JSON and save to file ...
    logger.info("Orchestration pipeline (Epic 1 part) complete.")
    
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