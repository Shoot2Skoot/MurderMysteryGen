# Mystery.AI - Project Structure (MVP)

This document outlines the proposed project directory and file structure for the Mystery.AI MVP. The structure aims for clarity, modularity, and ease of understanding, especially considering future development potentially involving AI developer agents.

## 1. Root Directory (`MurderMysteryGen/`)

```
MurderMysteryGen/
├── .venv/                     # Python virtual environment
├── config/                    # Project-wide configuration files
│   └── master_lists/          # Specific master lists for generation diversity
│       ├── cause_of_death.json
│       ├── motive_categories.json
│       ├── occupation_archetypes.json
│       └── personality_archetypes.json
├── docs/                      # All project documentation
│   ├── templates/             # Document templates
│   ├── architecture.md
│   ├── data-models.md
│   ├── deep-research-report-BA.md
│   ├── developer_guide.md
│   ├── environment-vars.md
│   ├── api-reference.md
│   ├── prd.md
│   ├── project-brief.md
│   ├── project-structure.md
│   ├── tech-stack.md
│   ├── testing-strategy.md
│   ├── coding-standards.md
│   ├── branching-evidence-design.md
│   ├── prd-branching-evidence.md
│   ├── epic1-branching-evidence-models-narrative.md
│   ├── epic2-branching-evidence-timeline-alibi.md
│   ├── epic3-branching-evidence-blueprinting.md
│   ├── epic4-branching-evidence-weaving.md
│   ├── epic5-branching-evidence-coherence-orchestration.md
│   ├── pm-checklist-branching-evidence.md
│   ├── ... (other epics for foundational system, e.g., epic1.md, epic2.md etc.)
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
│       │   ├── evidence_generator.py# Implements EvidenceGenerationAgent
│       │   # Branching Evidence System Agents:
│       │   ├── narrative_refinement_agent.py
│       │   ├── timeline_orchestrator_agent.py
│       │   ├── information_blueprint_agent.py
│       │   ├── clue_weaving_agent.py
│       │   ├── evidence_distribution_agent.py
│       │   └── master_coherence_agent.py
│       ├── core/                # Core logic, data models, shared utilities
│       │   ├── __init__.py
│       │   ├── data_models.py     # Pydantic models for foundational system (CaseContext, etc.)
│       │   ├── data_models_branching.py # Pydantic models for Branching Evidence (BranchingCaseContext, etc.)
│       │   └── utils.py           # Shared utility functions (if any)
│       │   └── config.py          # (Optional: For loading app configuration if it grows)
│       ├── orchestration/       # Orchestration logic
│       │   ├── __init__.py
│       │   ├── main_orchestrator.py # Main script for foundational mystery generation pipeline
│       │   └── run_full_branching_pipeline.py # Main script for Branching Evidence MVP pipeline
│       └── main.py                # Main entry point script (e.g., could call main_orchestrator.py)
├── tests/                     # Unit and integration tests
│   ├── __init__.py
│   ├── agents/
│   │   └── ... (tests for each agent, including new branching agents like test_narrative_refinement_agent.py)
│   ├── core/
│   │   └── ... (tests for data_models.py, data_models_branching.py, utils)
│   └── orchestration/
│       └── ... (integration tests for pipelines, including test_full_branching_pipeline.py)
├── tools/
│   ├── branching_evidence_runners/ # CLI scripts for testing individual branching evidence epics/agents
│   │   ├── __init__.py
│   │   ├── run_narrative_refinement_mvp.py
│   │   ├── run_timeline_orchestrator_mvp.py
│   │   ├── run_information_blueprint_mvp.py
│   │   └── run_clue_weaving_mvp.py
│   └── ... (other existing tools like bmad)
├── .env.example               # Example environment variables file
├── .gitignore
├── LICENSE                    # (To be added if open-sourcing)
└── README.md                  # Project README
└── requirements.txt           # Python dependencies
```

## 2. Key Directories Explained

-   **`MurderMysteryGen/`**: The absolute root of this specific project.
    -   **`.venv/`**: Standard Python virtual environment. Not committed to Git.
    -   **`config/`**: Contains project-wide configuration files. This includes master lists used for injecting diversity into the generation process (e.g., causes of death, motive categories, character archetypes) and could later include other global settings.
        -   `master_lists/`: Subdirectory specifically for JSON-based master lists.
    -   **`docs/`**: Contains all markdown documentation (PRD, architecture, epics, tech stack, this file, etc.).
        -   `templates/`: Holds the templates used for generating various documents.
    -   **`src/`**: Contains all the source code for the application.
        -   **`mystery_ai/`**: This is the main Python package for the Mystery.AI system.
            -   `agents/`: Each key agent identified in the architecture will have its own Python module. This includes agents for the foundational system (e.g., `case_initializer.py`) and agents for the Branching Evidence System (e.g., `narrative_refinement_agent.py`).
            -   `core/`: For shared functionalities.
                -   `data_models.py`: Contains Pydantic models for the foundational mystery generation (e.g., `CaseContext`, `VictimProfile`).
                -   `data_models_branching.py`: Contains Pydantic models specific to the Branching Evidence System (e.g., `BranchingCaseContext`, `InformationNugget`).
                -   `utils.py`: For any general utility functions that don't belong to a specific agent but might be used by multiple components (e.g., helper for sanitizing strings for filenames, if needed).
                -   `config.py` (Optional): If configuration grows beyond simple CLI args and `.env`, this could house logic for loading and accessing configuration **from the `MurderMysteryGen/config/` directory** or for managing Python-specific configurations not suitable for JSON. For MVP, this might not be strictly necessary if constants in `main_orchestrator.py` or `main.py` suffice for simple parameters.
            -   `orchestration/`:
                -   `main_orchestrator.py`: Contains the primary logic for the foundational mystery generation pipeline.
                -   `run_full_branching_pipeline.py`: Contains the primary logic for the Branching Evidence System MVP pipeline.
            -   `main.py`: The top-level executable script for the CLI. It will handle `argparse` for CLI arguments (like `--theme`, `--debug`), set up logging, load the `.env` file, and then likely call a main function within `orchestration/main_orchestrator.py` to start the generation process.
    -   **`tests/`**: Contains all automated tests. The structure within `tests/` should mirror the `src/mystery_ai/` structure. New tests for branching evidence agents, data models, and orchestration will be added accordingly.
    -   **`tools/`**: Contains utility scripts for development, testing, or specific tasks. Includes runners for individual Branching Evidence System agents/epics under `tools/branching_evidence_runners/`.
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