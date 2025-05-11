# Epic 1: Core Agent Setup & Case Initialization

**Goal:** Establish the basic multi-agent framework using the OpenAI Agents SDK, define the initial agent roles, and implement the capability to initialize a new mystery case with a theme and generate victim details.

**Deployability:** This epic established the foundational Python project structure (`src/mystery_ai/`), installed necessary dependencies (`openai-agents`, `python-dotenv`), and created the first operational agent (`CaseInitializationAgent`) capable of performing the initial step of a mystery generation. The main script (`src/mystery_ai/main.py`) can be run, taking a theme as input, and the system will output a `CaseContext` object (printed as JSON to console) containing the theme and the generated `VictimProfile`. This forms the basis upon which all subsequent epics build.

## Epic-Specific Technical Context

- **Project Scaffolding:** Python project structure created under `src/mystery_ai/` with sub-packages for `agents`, `core`, and `orchestration`. Virtual environment `.venv` and `requirements.txt` are in place.
- **API Key Management:** Secure API key handling via `OPENAI_API_KEY` environment variable, loaded from a `.env` file (with `.env.example` provided and `.env` gitignored).
- **Initial Agent Definition:** `CaseInitializationAgent` defined in `src/mystery_ai/agents/case_initializer.py` using OpenAI Agents SDK.
- **Orchestration Entry Point:** `src/mystery_ai/main.py` (CLI) calls `src/mystery_ai/orchestration/main_orchestrator.py`.
- **Data Structures:** Initial Pydantic models `VictimProfile` and `CaseContext` (holding theme and victim) defined in `src/mystery_ai/core/data_models.py`.
- **Logging & Tracing:** Basic logging and OpenAI Agents SDK tracing (with workflow name, trace ID, metadata) are set up in `main.py`.

## Local Testability & Command-Line Access

- **Local Development:** Developers can run `python -m src.mystery_ai.main --theme "Your Theme"` from the `MurderMysteryGen` root directory.
- **Command-Line Testing:** The script accepts a `--theme` argument. A `--debug` flag enables verbose logging.
- **Environment Testing:** The script runs successfully in the local development `.venv` environment.
- **Testing Prerequisites:** OpenAI API key must be set in the `.env` file. Python and dependencies from `requirements.txt` installed.
- **Verification:** Successful execution of this epic is verified by console output showing the theme and a generated `VictimProfile` (name, occupation, personality, cause of death) consistent with the theme.

## Story List

### Story 1.1: Project & SDK Setup

- **User Story / Goal:** As a Developer, I want a properly set up Python project with the OpenAI Agents SDK installed and API key management configured, so that I can start building the agentic system.
- **Detailed Requirements:** Implemented.
- **Acceptance Criteria (ACs):**
  - AC1: Virtual environment is created and can be activated. **(COMPLETED)**
  - AC2: `openai-agents` SDK is listed in `requirements.txt` and can be imported. **(COMPLETED)**
  - AC3: `OPENAI_API_KEY` can be loaded successfully from an `.env` file. **(COMPLETED)**
  - AC4: `.env` file is correctly ignored by git. **(COMPLETED)**
- **Dependencies:** None.
- **Status:** COMPLETED

---

### Story 1.2: Define Orchestrator Agent (or Main Script)

- **User Story / Goal:** As a Developer, I want a basic orchestrator agent (or main script structure) that can manage the overall flow and invoke other specialized agents, starting with case initialization.
- **Detailed Requirements:** `main.py` and `orchestration/main_orchestrator.py` created.
- **Acceptance Criteria (ACs):**
  - AC1: A Python script exists that defines the entry point for the generation process. **(COMPLETED)**
  - AC2: The script/agent structure is prepared to integrate and call other agents. **(COMPLETED)**
  - AC3: Placeholder (now actual call) for `CaseInitializationAgent` is present in orchestrator. **(COMPLETED)**
- **Dependencies:** Story 1.1.
- **Status:** COMPLETED

---

### Story 1.3: Define Case Initialization Agent

- **User Story / Goal:** As a Developer, I want a specialized `CaseInitializationAgent` that is responsible for taking a theme and generating the initial victim profile.
- **Detailed Requirements:** `CaseInitializationAgent` defined in `agents/case_initializer.py`.
- **Acceptance Criteria (ACs):**
  - AC1: `CaseInitializationAgent` class/definition exists with appropriate SDK constructs. **(COMPLETED)**
  - AC2: Agent instructions clearly define its purpose regarding theme input and victim detail generation. **(COMPLETED)**
  - AC3: Agent is configured with a specified LLM model (`gpt-4.1-mini`). **(COMPLETED)**
- **Dependencies:** Story 1.1.
- **Status:** COMPLETED

---

### Story 1.4: Implement Theme Input Mechanism

- **User Story / Goal:** As a Developer, I want the system to accept a basic theme (e.g., "Cyberpunk", "Pirate Ship") as input via a CLI argument, so that the generation can be guided.
- **Detailed Requirements:** Implemented in `main.py` using `argparse`.
- **Acceptance Criteria (ACs):**
  - AC1: The main script can be run with a `--theme` argument (e.g., `python main.py --theme "Noir"`). **(COMPLETED)**
  - AC2: The provided theme string is correctly captured and available for use by the orchestrator. **(COMPLETED)**
  - AC3: If no theme is provided, a default theme is used. **(COMPLETED)**
- **Dependencies:** Story 1.2.
- **Status:** COMPLETED

---

### Story 1.5: Implement Victim Profile Generation

- **User Story / Goal:** As a `CaseInitializationAgent`, I want to generate a victim's Name, Occupation, Personality, and Cause of Death based on the provided theme, so that the core of the mystery is established.
- **Detailed Requirements:** `CaseInitializationAgent` prompts LLM; `VictimProfile` and `CaseContext` Pydantic models defined.
- **Acceptance Criteria (ACs):**
  - AC1: `CaseInitializationAgent` successfully calls an LLM to generate victim details. **(COMPLETED via Story 1.6 test)**
  - AC2: Generated victim details are plausible and consistent with the input theme. **(COMPLETED via Story 1.6 test)**
  - AC3: The output of `CaseInitializationAgent` is a Pydantic `VictimProfile` object. **(COMPLETED via Story 1.6 test)**
  - AC4: `VictimProfile` and initial `CaseContext` Pydantic models are defined. **(COMPLETED)**
- **Dependencies:** Story 1.3, Story 1.4.
- **Status:** COMPLETED

---

### Story 1.6: Basic Handoff & Data Flow for Case Initialization

- **User Story / Goal:** As an `OrchestratorAgent` (or main script), I want to invoke the `CaseInitializationAgent`, pass it the theme, and receive back the structured victim details and theme.
- **Detailed Requirements:** Implemented in `orchestration/main_orchestrator.py`.
- **Acceptance Criteria (ACs):**
  - AC1: The orchestrator successfully runs/calls the `CaseInitializationAgent`. **(COMPLETED)**
  - AC2: The theme is correctly passed as input to the `CaseInitializationAgent`. **(COMPLETED)**
  - AC3: The orchestrator receives the `CaseContext` (with `VictimProfile`) object. **(COMPLETED)**
  - AC4: The orchestrator can print or log the received victim details and theme. **(COMPLETED)**
- **Dependencies:** Story 1.2, Story 1.5.
- **Status:** COMPLETED

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
|        |      | 0.1     | Initial draft of Epic 1 | PM Agent |
|        |      | 0.2     | Stories 1.1-1.6 marked COMPLETED. Epic 1 fully implemented. | Dev Agent | 