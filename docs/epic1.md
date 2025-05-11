# Epic 1: Core Agent Setup & Case Initialization

**Goal:** Establish the basic multi-agent framework using the OpenAI Agents SDK, define the initial agent roles, and implement the capability to initialize a new mystery case with a theme and generate victim details.

**Deployability:** This epic establishes the foundational Python project structure, installs necessary dependencies (OpenAI Agents SDK), and creates the first operational agent(s) capable of performing the initial step of a mystery generation (case/victim setup). The output will be a structured representation of the victim and case theme. This forms the basis upon which all subsequent epics will build.

## Epic-Specific Technical Context

- **Project Scaffolding:** Create a new Python project directory (e.g., `src/mystery_generator` or similar within `MurderMysteryGen`), initialize `venv`, and set up `requirements.txt` including `openai-agents`.
- **API Key Management:** Implement secure API key handling using an environment variable (`OPENAI_API_KEY`) and a `.env` file (added to `.gitignore`).
- **Initial Agent Definitions:** Define Python classes or structures for the initial agents using the OpenAI Agents SDK syntax. This includes an `OrchestratorAgent` (or main script acting as orchestrator) and a `CaseInitializationAgent`.
- **Data Structures:** Define initial Pydantic models for input (e.g., theme) and output (e.g., CaseDetails including VictimProfile).

## Local Testability & Command-Line Access

- **Local Development:** Developers can run a main Python script (e.g., `main.py` or `run_epic1_test.py`) that triggers the Epic 1 functionality.
- **Command-Line Testing:** The script should accept a theme as a CLI argument (e.g., `python main.py --theme "Cyberpunk"`).
- **Environment Testing:** The script should run successfully in the local development `venv` environment.
- **Testing Prerequisites:** OpenAI API key must be set in the environment. Python and `openai-agents` SDK installed.

## Story List

### Story 1.1: Project & SDK Setup

- **User Story / Goal:** As a Developer, I want a properly set up Python project with the OpenAI Agents SDK installed and API key management configured, so that I can start building the agentic system.
- **Detailed Requirements:**
  - Create a Python project structure within `MurderMysteryGen/src/`.
  - Initialize a virtual environment (`.venv`).
  - Install `openai-agents` and any other core libraries (e.g., `python-dotenv` for .env file handling) and save to `requirements.txt`.
  - Create a `.env.example` file for `OPENAI_API_KEY`.
  - Ensure `.env` is in `.gitignore`.
  - Write a simple script to load the API key from `.env` to verify setup.
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
- **Detailed Requirements:**
  - Create a main Python script (e.g., `orchestrator.py` or `main.py`) that will serve as the entry point.
  - Define the basic structure for an `OrchestratorAgent` using the OpenAI Agents SDK (if adopting a full agent for orchestration) or outline the procedural flow in the main script.
  - This agent/script will eventually call other agents. For this story, it should be set up to call the `CaseInitializationAgent`.
- **Acceptance Criteria (ACs):**
  - AC1: A Python script exists that defines the entry point for the generation process. **(COMPLETED)**
  - AC2: The script/agent structure is prepared to integrate and call other agents. **(COMPLETED)**
  - AC3: Placeholder for calling `CaseInitializationAgent` is present. **(COMPLETED)**
- **Dependencies:** Story 1.1.
- **Status:** COMPLETED

---

### Story 1.3: Define Case Initialization Agent

- **User Story / Goal:** As a Developer, I want a specialized `CaseInitializationAgent` that is responsible for taking a theme and generating the initial victim profile.
- **Detailed Requirements:**
  - Define a new agent, `CaseInitializationAgent`, using the OpenAI Agents SDK.
  - Instructions for this agent should specify its role: to receive a theme and generate victim details (Name, Occupation, Personality, Cause of Death).
  - The agent should be configured to use an appropriate OpenAI model (e.g., `gpt-4.1-mini`).
  - The agent should be designed to output these details in a structured format (Pydantic model to be defined in Story 1.5).
- **Acceptance Criteria (ACs):**
  - AC1: `CaseInitializationAgent` class/definition exists with appropriate SDK constructs. **(COMPLETED)**
  - AC2: Agent instructions clearly define its purpose regarding theme input and victim detail generation. **(COMPLETED)**
  - AC3: Agent is configured with a specified LLM model. **(COMPLETED)**
- **Dependencies:** Story 1.1.
- **Status:** COMPLETED

---

### Story 1.4: Implement Theme Input Mechanism

- **User Story / Goal:** As a Developer, I want the system to accept a basic theme (e.g., "Cyberpunk", "Pirate Ship") as input via a CLI argument, so that the generation can be guided.
- **Detailed Requirements:**
  - Modify the main orchestrator script (from Story 1.2) to use `argparse` (or a similar library) to accept a `--theme` command-line argument.
  - The theme string should be passed to the `CaseInitializationAgent`.
- **Acceptance Criteria (ACs):**
  - AC1: The main script can be run with a `--theme` argument (e.g., `python main.py --theme "Noir"`). **(COMPLETED)**
  - AC2: The provided theme string is correctly captured and available for use by the `OrchestratorAgent` / main script. **(COMPLETED)**
  - AC3: If no theme is provided, a default theme can be used or an error message shown. **(COMPLETED)**
- **Dependencies:** Story 1.2.
- **Status:** COMPLETED

---

### Story 1.5: Implement Victim Profile Generation

- **User Story / Goal:** As a `CaseInitializationAgent`, I want to generate a victim's Name, Occupation, Personality, and Cause of Death based on the provided theme, so that the core of the mystery is established.
- **Detailed Requirements:**
  - The `CaseInitializationAgent` (from Story 1.3) prompts an LLM to generate the four victim attributes.
  - The generation should be guided by the input theme.
  - Define a Pydantic model (e.g., `VictimProfile`) for the victim's details (name: str, occupation: str, personality: str, cause_of_death: str).
  - The `CaseInitializationAgent` should be configured to return its output matching this Pydantic model structure (using SDK's `output_type`).
  - Define another Pydantic model (e.g. `CaseContext`) to hold the initial theme and the generated `VictimProfile`.
- **Acceptance Criteria (ACs):**
  - AC1: `CaseInitializationAgent` successfully calls an LLM to generate victim details. **(Partially Met - Definition in place, execution in 1.6)**
  - AC2: Generated victim details (Name, Occupation, Personality, Cause of Death) are plausible and consistent with the input theme. **(Partially Met - Definition in place, execution/validation in 1.6)**
  - AC3: The output of the `CaseInitializationAgent` is a Pydantic object of type `VictimProfile` (or contained within `CaseContext`). **(Partially Met - Agent configured, execution/validation in 1.6)**
  - AC4: `VictimProfile` and `CaseContext` Pydantic models are defined. **(COMPLETED)**
- **Dependencies:** Story 1.3, Story 1.4.
- **Status:** COMPLETED

---

### Story 1.6: Basic Handoff & Data Flow for Case Initialization

- **User Story / Goal:** As an `OrchestratorAgent` (or main script), I want to invoke the `CaseInitializationAgent`, pass it the theme, and receive back the structured victim details and theme.
- **Detailed Requirements:**
  - Implement the logic in the `OrchestratorAgent` (or main script) to run the `CaseInitializationAgent`.
  - The input to the `CaseInitializationAgent` run should be the theme string.
  - The output from the `CaseInitializationAgent` (the `CaseContext` Pydantic model including `VictimProfile`) should be received and stored/printed by the orchestrator.
  - This demonstrates the basic agent handoff/call mechanism of the SDK.
- **Acceptance Criteria (ACs):**
  - AC1: The `OrchestratorAgent` successfully runs/calls the `CaseInitializationAgent`. **(COMPLETED)**
  - AC2: The theme is correctly passed as input to the `CaseInitializationAgent`. **(COMPLETED)**
  - AC3: The `OrchestratorAgent` receives the `CaseContext` (with `VictimProfile`) object from the `CaseInitializationAgent`. **(COMPLETED)**
  - AC4: The orchestrator can print or log the received victim details and theme. **(COMPLETED)**
- **Dependencies:** Story 1.2, Story 1.5.
- **Status:** COMPLETED

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
|        |      | 0.1     | Initial draft of Epic 1 | PM Agent | 