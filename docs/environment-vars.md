# Environment Variables

This document lists the environment variables required by the Mystery.AI system, including the Branching Evidence System.

## Core System

### `OPENAI_API_KEY`

-   **Description:** Your secret API key for accessing OpenAI services, including the language models used by the agents.
-   **Required:** Yes, for any operations involving LLM calls (i.e., most agent executions).
-   **Usage:** The system uses the `python-dotenv` library to load this variable from a `.env` file located in the project root (`MurderMysteryGen/.env`).
-   **Setup:**
    1.  Create a file named `.env` in the `MurderMysteryGen/` root directory.
    2.  Add the following line to the `.env` file, replacing `your_actual_api_key_here` with your key:
        ```
        OPENAI_API_KEY=your_actual_api_key_here
        ```
    3.  Ensure that `.env` is listed in your `.gitignore` file to prevent accidental commitment of your API key. An `.env.example` file should be provided in the repository as a template.

## Other Variables

For the current MVP scope of both the foundational mystery generation and the branching evidence system, no other specific environment variables are defined as mandatory. Configuration parameters are primarily managed via CLI arguments or hardcoded constants within agent definitions or orchestration scripts, as detailed in `docs/developer_guide.md` and the respective architecture sections. 