"""
Environment verification module for the Murder Mystery Generation system.

This module provides utility functions to check if the environment is properly set up
with necessary API keys and dependencies. It verifies that the OpenAI API key is present
and that the required libraries are installed.
"""

import importlib.util
import os

from dotenv import load_dotenv


def main():
    """Loads environment variables and verifies OpenAI API key presence."""
    # Construct the path to the .env file in the project root (MurderMysteryGen)
    # This script is in MurderMysteryGen/src/mystery_ai/core/
    # So, ../../.env from this script's location
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env")

    if not os.path.exists(dotenv_path):
        print(f"Error: .env file not found at expected path: {os.path.abspath(dotenv_path)}")
        print("Please ensure a .env file exists in the MurderMysteryGen/ directory.")
        return

    load_dotenv(dotenv_path=dotenv_path)
    print(f"Attempting to load .env from: {os.path.abspath(dotenv_path)}")

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        print("Successfully loaded OPENAI_API_KEY.")
        print(f"API Key starts with: {api_key[:5]}...")  # Print a snippet for verification
    else:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please check your .env file in the MurderMysteryGen/ directory.")
        return

    # Check if agents package is available without importing it
    agents_spec = importlib.util.find_spec("agents")
    if agents_spec is not None:
        print("Successfully found 'agents' (OpenAI Agents SDK).")
    else:
        print("Error: 'agents' (OpenAI Agents SDK) is not installed.")
        print("Please ensure openai-agents is installed in your .venv environment.")


if __name__ == "__main__":
    main()
