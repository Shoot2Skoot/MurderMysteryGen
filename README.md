# Mystery.AI - MVP

## 1. Project Overview

Mystery.AI is an AI-driven agentic system designed to autonomously generate the foundational elements for "murder mystery in a box" style games. This Minimum Viable Product (MVP) focuses on creating the core logical structure of a mystery:

-   A victim profile (name, occupation, personality, cause of death).
-   2-3 suspect profiles (name, description, relationship to victim).
-   For each suspect, a plausible Means, Motive, and Opportunity (MMO).
-   Designation of one suspect as the killer.
-   Modification of one MMO element for non-killer suspects to create compelling red herrings.
-   Generation of initial evidence items (direct evidence for the killer, red herrings for others) linked to suspects' MMOs.

The system takes a simple theme as input (e.g., "Cyberpunk Noir Detective", "Victorian London Séance") and outputs a detailed JSON file containing the complete mystery framework. This output is intended for review and as a creative starting point for authors and game designers.

The project is built using Python and the OpenAI Agents SDK.

## 2. Setup Instructions

### Prerequisites

-   Python 3.12.3 (as per original user environment; likely compatible with other Python 3.9+ versions, but 3.12.3 is tested).
-   An OpenAI API Key.

### Setup Steps

1.  **Clone the Repository (if applicable)**
    ```bash
    # git clone <repository_url>
    # cd MurderMysteryGen
    ```

2.  **Create and Activate Virtual Environment:**
    It is highly recommended to use a virtual environment.
    ```bash
    python -m venv .venv
    ```
    Activate it:
    -   Windows (PowerShell/CMD):
        ```powershell
        .venv\Scripts\activate
        ```
    -   macOS/Linux (bash/zsh):
        ```bash
        source .venv/bin/activate
        ```

3.  **Install Dependencies:**
    Install the required Python packages from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
    This will install `openai-agents`, `python-dotenv`, and any other necessary libraries.

4.  **Set Up OpenAI API Key:**
    -   Rename the `.env.example` file in the project root (`MurderMysteryGen/`) to `.env`.
    -   Open the `.env` file and replace `your_api_key_here` with your actual OpenAI API key:
        ```
        OPENAI_API_KEY=sk-YourActualOpenAIKeyHere
        ```
    -   The `.env` file is included in `.gitignore` and should not be committed to version control.

## 3. How to Run the Mystery Generator

Once the setup is complete, you can generate a mystery from the command line.

1.  Ensure your virtual environment is activated.
2.  Navigate to the `MurderMysteryGen` root directory in your terminal.
3.  Run the main script using the following command structure:

    ```bash
    python -m src.mystery_ai.main --theme "YOUR_CHOSEN_THEME"
    ```

    **Arguments:**
    -   `--theme "YOUR_CHOSEN_THEME"`: (Required, though it has a default) Specifies the theme for the mystery to be generated. Enclose themes with spaces in quotes. 
        Examples:
        -   `--theme "Futuristic Mars Colony Uprising"`
        -   `--theme "Roaring Twenties Speakeasy"`
        -   `--theme "Haunted Library"`
        (Default if not provided: "Cyberpunk Noir Detective")
    -   `--debug`: (Optional) Add this flag to enable more verbose debug logging to the console.
        Example: `python -m src.mystery_ai.main --theme "Wild West Ghost Town" --debug`

## 4. Understanding the Output

-   **Console Output:** The script will print status messages and logs to the console during generation. Upon successful completion, it will print a JSON representation of the generated `CaseContext` (the full mystery structure).
-   **JSON File Output:**
    -   A JSON file containing the full mystery data will be saved in the `MurderMysteryGen/generated_mysteries/` directory.
    -   The filename will be in the format: `mystery_<sanitized_theme>_<YYYYMMDD_HHMMSS>.json` (e.g., `mystery_Futuristic_Mars_Colony_Uprising_20230510_230000.json`).
    -   This file contains the structured `CaseContext` object, which includes:
        -   The input `theme`.
        -   The generated `victim` profile.
        -   A list of `suspects`, each with their `profile`, `original_mmo`, `is_killer` status, and any `modified_mmo_elements` (for non-killers).
        -   A list of `evidence_items` generated for the case.
        -   An optional `author_notes` field (currently defaults to `null`).
    -   The detailed schema for this JSON output can be found in `docs/data-models.md`.

## 5. Project Structure

The project code is primarily located within the `src/mystery_ai/` directory, organized as follows:

-   `agents/`: Contains the definitions for specialized AI agents (e.g., `CaseInitializationAgent`, `SuspectGenerationAgent`).
-   `core/`: Includes core data models (`data_models.py` with Pydantic schemas) and shared utilities.
-   `orchestration/`: Houses the main pipeline logic (`main_orchestrator.py`).
-   `main.py`: The command-line entry point for the application.

For a detailed breakdown of the project structure, please refer to `docs/project-structure.md`.

## 6. Key Documentation

For more in-depth information about the project, refer to the following documents in the `docs/` directory:

-   `project-brief.md`: Initial project vision, goals, and high-level scope.
-   `prd.md`: Product Requirements Document detailing MVP features and requirements.
-   `architecture.md`: System architecture, component breakdown, and agent interactions.
-   `data-models.md`: Detailed Pydantic model definitions and the output JSON schema.
-   `tech-stack.md`: Specific technologies and libraries used.
-   `coding-standards.md`: Coding conventions and best practices.
-   `testing-strategy.md`: Approach to testing the MVP.
-   `epic1.md`, `epic2.md`, `epic3.md`, `epic4.md`: Detailed breakdown of work for each completed MVP epic, including user stories.

## 7. Development Notes & Troubleshooting

-   Ensure your `OPENAI_API_KEY` is correctly set in the `.env` file and that the file is in the `MurderMysteryGen` root.
-   If you encounter import errors when running `main.py`, make sure your virtual environment is activated and you are running the script as a module (`python -m src.mystery_ai.main`) from the `MurderMysteryGen` directory.
-   The OpenAI Agents SDK includes tracing capabilities. By default, traces might be sent to the OpenAI dashboard if your API key is configured for it. Refer to `docs/coding-standards.md` and the SDK documentation for more on tracing.
-   The quality and diversity of generated content (e.g., causes of death, suspect variety) are known areas for future improvement beyond this MVP. 