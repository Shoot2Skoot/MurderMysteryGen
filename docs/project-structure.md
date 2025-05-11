# Mystery.AI - Project Structure (MVP)

This document outlines the proposed project directory and file structure for the Mystery.AI MVP. The structure aims for clarity, modularity, and ease of understanding, especially considering future development potentially involving AI developer agents.

## 1. Root Directory (`MurderMysteryGen/`)

```
MurderMysteryGen/
├── .venv/                     # Python virtual environment
├── docs/                      # All project documentation
│   ├── templates/             # Document templates
│   ├── architecture.md
│   ├── data-models.md
│   ├── deep-research-report-BA.md
│   ├── epic1.md
│   ├── epic2.md
│   ├── epic3.md
│   ├── epic4.md
│   ├── prd.md
│   ├── project-brief.md
│   ├── project-structure.md
│   ├── tech-stack.md
│   └── testing-strategy.md    # (To be detailed later)
│   └── coding-standards.md    # (To be created)
│   └── ... (other docs as needed)
├── src/
│   └── mystery_ai/            # Main application package for Mystery.AI
│       ├── __init__.py
│       ├── agents/              # Specialized agent definitions
│       │   ├── __init__.py
│       │   ├── base_agent.py      # (Optional: A base class if common logic emerges)
│       │   ├── case_initializer.py # Implements CaseInitializationAgent
│       │   ├── suspect_generator.py # Implements SuspectGenerationAgent
│       │   ├── mmo_generator.py     # Implements MMOGenerationAgent
│       │   ├── killer_selector.py   # Implements KillerSelectionAgent
│       │   ├── mmo_modifier.py      # Implements MMOModificationAgent
│       │   └── evidence_generator.py# Implements EvidenceGenerationAgent
│       ├── core/                # Core logic, data models, shared utilities
│       │   ├── __init__.py
│       │   ├── data_models.py     # All Pydantic models (CaseContext, VictimProfile, etc.)
│       │   └── utils.py           # Shared utility functions (if any)
│       │   └── config.py          # (Optional: For loading app configuration if it grows)
│       ├── orchestration/       # Orchestration logic
│       │   ├── __init__.py
│       │   └── main_orchestrator.py # Main script to run the pipeline (e.g., run_mystery_generation.py)
│       └── main.py                # Main entry point script (e.g., could call main_orchestrator.py)
├── tests/                     # Unit and integration tests
│   ├── __init__.py
│   ├── agents/
│   │   └── ... (tests for each agent)
│   ├── core/
│   │   └── ... (tests for data_models, utils)
│   └── orchestration/
│       └── ... (integration tests for the pipeline)
├── .env.example               # Example environment variables file
├── .gitignore
├── LICENSE                    # (To be added if open-sourcing)
└── README.md                  # Project README
└── requirements.txt           # Python dependencies
```

## 2. Key Directories Explained

-   **`MurderMysteryGen/`**: The absolute root of this specific project.
    -   **`.venv/`**: Standard Python virtual environment. Not committed to Git.
    -   **`docs/`**: Contains all markdown documentation (PRD, architecture, epics, tech stack, this file, etc.).
        -   `templates/`: Holds the templates used for generating various documents.
    -   **`src/`**: Contains all the source code for the application.
        -   **`mystery_ai/`**: This is the main Python package for the Mystery.AI system.
            -   `agents/`: Each key agent identified in the architecture (e.g., `CaseInitializationAgent`, `SuspectGenerationAgent`) will have its own Python module (e.g., `case_initializer.py`). This promotes modularity. An optional `base_agent.py` could be introduced if significant common functionality or setup is identified across agents.
            -   `core/`: For shared functionalities.
                -   `data_models.py`: **Crucial file.** This will contain all Pydantic model definitions (`CaseContext`, `VictimProfile`, `SuspectProfile`, `MMO`, `EvidenceItem`, etc.) used throughout the application, ensuring a single source of truth for data structures. These models must adhere to OpenAI's structured output constraints.
                -   `utils.py`: For any general utility functions that don't belong to a specific agent but might be used by multiple components (e.g., helper for sanitizing strings for filenames, if needed).
                -   `config.py` (Optional): If configuration grows beyond simple CLI args and `.env`, this could house logic for loading and accessing configuration. For MVP, this might not be strictly necessary if constants in `main_orchestrator.py` or `main.py` suffice.
            -   `orchestration/`:
                -   `main_orchestrator.py`: Contains the primary logic for the sequential execution of the agent pipeline as defined in `architecture.md`. This script will instantiate and run agents using the OpenAI Agents SDK's `Runner`. This might be the script named `run_mystery_generation.py` in earlier discussions.
            -   `main.py`: The top-level executable script for the CLI. It will handle `argparse` for CLI arguments (like `--theme`, `--debug`), set up logging, load the `.env` file, and then likely call a main function within `orchestration/main_orchestrator.py` to start the generation process.
    -   **`tests/`**: Contains all automated tests. The structure within `tests/` should mirror the `src/mystery_ai/` structure to make it easy to locate tests for specific modules or components.
    -   `.env.example`**: Template for the `.env` file, showing necessary environment variables like `OPENAI_API_KEY`.
    -   `.gitignore`**: Specifies intentionally untracked files (e.g., `.venv/`, `__pycache__/`, `.env`, `*.json` output files if desired).
    -   `LICENSE`**: Important if the project will be open-sourced.
    -   `README.md`**: Main entry point for developers, explaining what the project is, how to set it up, run it, and contribute.
    -   `requirements.txt`**: Lists all Python dependencies for `pip install -r requirements.txt`.

## 3. Naming Conventions

-   **Python Modules:** `snake_case.py` (e.g., `case_initializer.py`).
-   **Python Packages (Directories):** `snake_case` (e.g., `mystery_ai`, `agents`).
-   **Agent Classes:** `PascalCase` and suffixed with `Agent` (e.g., `CaseInitializationAgent`).
-   **Pydantic Models:** `PascalCase` (e.g., `CaseContext`, `VictimProfile`).
-   **Avoid `agents.py`:** As per previous discussions, to avoid conflict with the `openai-agents` SDK import (`import agents`), no custom module will be named `agents.py`. The directory `src/mystery_ai/agents/` is acceptable as it forms part of a package path (`mystery_ai.agents`).

This structure is designed to be logical and scalable as the project grows beyond the MVP. 