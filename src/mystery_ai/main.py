"""
Main entry point for the Murder Mystery Generation system.

This module provides the command-line interface for generating murder mysteries,
handling argument parsing and executing the main generation pipeline.
"""

import argparse
import logging
import os
import uuid
from typing import Optional

from dotenv import load_dotenv

from .orchestration.main_orchestrator import run_generation_pipeline

# Set up OpenAI Agents tracing if needed
has_trace = False
try:
    from agents import trace
    has_trace = True
except ImportError:
    # OpenAI Agents SDK not available
    pass

DEFAULT_WORKFLOW_NAME = "MysteryGeneration_MVP"


def setup_logging(debug=False):
    """Configure logging for the application."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def load_environment():
    """Loads .env file from the project root."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    dotenv_path = os.path.join(project_root, ".env")

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
    """Main entry point for the application."""
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Generate a murder mystery case")
    parser.add_argument(
        "--theme",
        type=str,
        default="Haunted Library",
        help="The theme for the mystery (e.g., 'Cyberpunk Dystopia')",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
    args = parser.parse_args()

    # Setup logging
    setup_logging(args.debug)
    logger = logging.getLogger(__name__)

    # Load environment variables from .env file
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
        logger.info("Loaded environment variables from %s", dotenv_path)
    else:
        logger.warning("No .env file found at %s", dotenv_path)

    # Check for OPENAI_API_KEY
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment variables. Please set it in the .env file.")
        return 1

    # Setup trace_id for debugging/tracking if using the OpenAI Agents SDK
    trace_id = None
    if has_trace:
        trace_id = f"trace_main_{uuid.uuid4().hex}"

    # Run the generation pipeline
    try:
        logger.info("Starting mystery generation with theme: %s", args.theme)
        case_context = run_generation_pipeline(theme=args.theme, trace_id=trace_id)
        
        if case_context:
            logger.info("Mystery generation completed successfully!")
            return 0
        else:
            logger.error("Mystery generation failed. See logs for details.")
            return 1
    except Exception as e:
        logger.error("An error occurred during generation: %s", e, exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
