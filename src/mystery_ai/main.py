import argparse
import logging
import os
from dotenv import load_dotenv
import uuid
from typing import Optional

# Import the main orchestrator function
from .orchestration.main_orchestrator import run_generation_pipeline

# Import trace from agents SDK
from agents import trace 

# Import CaseContext from core data models
from .core.data_models import CaseContext

DEFAULT_WORKFLOW_NAME = "MysteryGeneration_MVP"

def setup_logging(debug_mode: bool = False):
    """Configures basic logging for the application."""
    log_level = logging.DEBUG if debug_mode else logging.INFO
    logging.basicConfig(level=log_level, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Optionally, quiet down very verbose loggers from dependencies if needed
    # logging.getLogger("httpx").setLevel(logging.WARNING) # Example

def load_environment():
    """Loads .env file from the project root."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    dotenv_path = os.path.join(project_root, '.env')
    
    if not os.path.exists(dotenv_path):
        logging.warning(f".env file not found at {dotenv_path}. API calls might fail.")
        return False
    
    loaded = load_dotenv(dotenv_path=dotenv_path)
    if loaded:
        logging.info(f"Successfully loaded .env file from {dotenv_path}")
    else:
        logging.warning(f"Failed to load .env file from {dotenv_path} or it was empty.")
    return loaded

def main():
    """Main entry point for the Mystery.AI generation script."""
    parser = argparse.ArgumentParser(description="Mystery.AI - Murder Mystery Generation Tool (MVP)")
    parser.add_argument("--theme", type=str, default="Cyberpunk Noir Detective", 
                        help="The theme for the murder mystery (e.g., 'Cyberpunk', 'Pirate Ship').")
    parser.add_argument("--debug", action="store_true", 
                        help="Enable debug logging.")

    args = parser.parse_args()

    setup_logging(args.debug)
    load_environment()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error("OPENAI_API_KEY not found. Please ensure it is set in your .env file.")
        return
    logging.info("OPENAI_API_KEY found.")

    current_trace_id = f"trace_{uuid.uuid4().hex}"
    # Ensure all metadata values are strings for OpenAI tracing
    trace_metadata = {
        "input_theme": str(args.theme),
        "debug_mode": str(args.debug) 
    }

    logging.info(f"Starting Mystery Generation for theme: '{args.theme}'")
    logging.info(f"Trace ID for this run: {current_trace_id}")

    try:
        # The trace_id passed to the context manager is used by the SDK.
        # We use current_trace_id for our own logging and passing to functions if needed.
        with trace(DEFAULT_WORKFLOW_NAME, trace_id=current_trace_id, metadata=trace_metadata):
            logging.info(f"Workflow '{DEFAULT_WORKFLOW_NAME}' started. Trace ID for this run: {current_trace_id}")
            
            case_context_result: Optional[CaseContext] = run_generation_pipeline(theme=args.theme, trace_id=current_trace_id)
            
            logging.info("Mystery generation pipeline finished.")
            print("\n--- Orchestrator Output (Story 1.6) ---")
            if case_context_result:
                print(case_context_result.model_dump_json(indent=2))
            else:
                print("No CaseContext returned from pipeline.")
            print("-------------------------------------")

    except Exception as e:
        logging.error(f"An unexpected error occurred during mystery generation: {e}", exc_info=True)

if __name__ == "__main__":
    main() 