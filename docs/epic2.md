# Epic 2: Suspect & MMO Generation

**Goal:** Develop the agent(s) responsible for generating 2-3 unique suspect profiles and, for each suspect, creating a plausible and distinct Means, Motive, and Opportunity (MMO) consistent with the initialized case.

**Deployability:** This epic builds upon the initialized case (theme and victim details from Epic 1). It introduces new agent capabilities for suspect and MMO generation. The output will be the `CaseContext` data structure, now augmented with a list of suspects, each having a profile and a fully fleshed-out MMO. This state is testable and provides a richer dataset for the next epic.

## Epic-Specific Technical Context

- **New Agent Definitions:** Define `SuspectGenerationAgent` and `MMOGenerationAgent`.
- **Pydantic Model Expansion:** `SuspectProfile`, `MMO`, `Suspect` models defined; `CaseContext` updated.
- **Agent Instructions & Prompts:** Developed for suspect and MMO generation.

## Local Testability & Command-Line Access

- **Local Development:** Developers can run the main script (`src/mystery_ai/main.py`) which now includes Epic 1 and Epic 2 functionality.
- **Command-Line Testing:** The main script accepts a theme via `--theme`.
- **Output:** The script outputs the `CaseContext` (including victim, suspects, and their MMOs) as JSON to the console for verification.

## Story List

### Story 2.1: Define Suspect Generation Agent

- **User Story / Goal:** As a Developer, I want a specialized `SuspectGenerationAgent` that, given the case context (theme & victim), can generate a list of 2-3 unique suspect profiles.
- **Detailed Requirements:** Implemented.
- **Acceptance Criteria (ACs):**
  - AC1: `SuspectGenerationAgent` class/definition exists. **(COMPLETED)**
  - AC2: Agent instructions clearly define its purpose. **(COMPLETED)**
  - AC3: `SuspectProfile` Pydantic model is defined. **(COMPLETED)**
  - AC4: Agent is invoked by orchestrator and produces a list of `SuspectProfile` objects. **(COMPLETED)**
- **Dependencies:** Story 1.5.
- **Status:** COMPLETED

---

### Story 2.2: Define MMO Generation Agent & Logic

- **User Story / Goal:** As a Developer, I want an `MMOGenerationAgent` to generate a plausible Means, Motive, and Opportunity (MMO) for a given suspect profile and case context.
- **Detailed Requirements:** Implemented.
- **Acceptance Criteria (ACs):**
  - AC1: `MMOGenerationAgent` structure for MMO generation is defined. **(COMPLETED)**
  - AC2: Agent instructions clearly guide the LLM. **(COMPLETED)**
  - AC3: `MMO` Pydantic model is defined. **(COMPLETED)**
  - AC4: Agent is invoked by orchestrator with `SuspectProfile` and `CaseContext`, and it returns a populated `MMO` object. **(COMPLETED)**
- **Dependencies:** Story 2.1.
- **Status:** COMPLETED

---

### Story 2.3: Integrate Suspect & MMO Generation

- **User Story / Goal:** As a Developer, I want the system to generate 2-3 suspects, and for each suspect, generate their full MMO, then integrate this into the main `CaseContext` data structure.
- **Detailed Requirements:** Implemented in `main_orchestrator.py`.
- **Acceptance Criteria (ACs):**
  - AC1: The `OrchestratorAgent` successfully orchestrates the generation of 2-3 suspects. **(COMPLETED)**
  - AC2: Each generated suspect has a complete `SuspectProfile` and a complete `MMO` object. **(COMPLETED)**
  - AC3: The `CaseContext` Pydantic model is updated with a list of these `Suspect` objects. **(COMPLETED)**
  - AC4: The orchestrator can output the `CaseContext` showing victim, theme, and all suspects with their MMOs. **(COMPLETED)**
- **Dependencies:** Story 1.6, Story 2.1, Story 2.2.
- **Status:** COMPLETED

---

### Story 2.4: Handoffs & Data Flow for Suspect/MMO Generation

- **User Story / Goal:** As an `OrchestratorAgent`, I want to correctly manage the data flow and handoffs between case initialization and suspect/MMO generation, ensuring all necessary context is passed and results are aggregated.
- **Detailed Requirements:** Implemented in `main_orchestrator.py`.
- **Acceptance Criteria (ACs):**
  - AC1: Data flows correctly from `CaseInitializationAgent` output to `SuspectGenerationAgent` input. **(COMPLETED)**
  - AC2: `SuspectGenerationAgent` and `MMOGenerationAgent` produce the expected list of `Suspect` objects (via profiles and MMOs). **(COMPLETED)**
  - AC3: The `OrchestratorAgent` successfully incorporates the suspect list into the main `CaseContext`. **(COMPLETED)**
  - AC4: No data is lost or corrupted during handoffs relevant to this epic. **(COMPLETED)**
- **Dependencies:** Story 2.3.
- **Status:** COMPLETED

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
|        |      | 0.1     | Initial draft of Epic 2 | PM Agent |
|        |      | 0.2     | Marked stories 2.1-2.4 COMPLETED after successful integration and test. | Dev Agent | 