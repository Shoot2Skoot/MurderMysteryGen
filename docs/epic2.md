# Epic 2: Suspect & MMO Generation

**Goal:** Develop the agent(s) responsible for generating 2-3 unique suspect profiles and, for each suspect, creating a plausible and distinct Means, Motive, and Opportunity (MMO) consistent with the initialized case.

**Deployability:** This epic builds upon the initialized case (theme and victim details from Epic 1). It introduces new agent capabilities for suspect and MMO generation. The output will be the `CaseContext` data structure, now augmented with a list of suspects, each having a profile and a fully fleshed-out MMO. This state is testable and provides a richer dataset for the next epic.

## Epic-Specific Technical Context

- **New Agent Definitions:** Define `SuspectGenerationAgent` and potentially a separate `MMOGenerationAgent` (or combine into one if simpler for MVP). These agents will take `CaseContext` (theme, victim) as input.
- **Pydantic Model Expansion:**
  - Define `SuspectProfile` model (e.g., name: str, brief_description: str, relationship_to_victim: str).
  - Define `MMO` model (means: str, motive: str, opportunity: str).
  - Update `CaseContext` to include a list of `Suspect` objects, where `Suspect` contains `SuspectProfile` and its `MMO`.
- **Agent Instructions & Prompts:** Develop clear instructions for the new agent(s) to generate 2-3 distinct suspects and their respective MMOs, ensuring they are consistent with the theme and victim.

## Local Testability & Command-Line Access

- **Local Development:** Developers can run a test script that first executes Epic 1 logic (or uses a fixture/mock `CaseContext` from Epic 1) and then triggers Epic 2 functionality.
- **Command-Line Testing:** The test script could optionally take the theme as input (to run Epic 1 first) or load a pre-generated `CaseContext` JSON file.
- **Output:** The script should output the augmented `CaseContext` (including suspects and their MMOs) as JSON to the console or a file for verification.

## Story List

### Story 2.1: Define Suspect Generation Agent

- **User Story / Goal:** As a Developer, I want a specialized `SuspectGenerationAgent` that, given the case context (theme & victim), can generate a list of 2-3 unique suspect profiles.
- **Detailed Requirements:**
  - Define a new agent, `SuspectGenerationAgent`, using the OpenAI Agents SDK.
  - Instructions should specify its role: to receive `CaseContext` (theme, victim details) and generate 2-3 distinct suspect profiles.
  - Each suspect profile should include a name, a brief description/archetype, and their relationship to the victim.
  - Agent should be configured to use an appropriate OpenAI model.
  - Define a Pydantic model `SuspectProfile` (name: str, description: str, relationship_to_victim: str).
  - Agent should aim to output a list of `SuspectProfile` objects.
- **Acceptance Criteria (ACs):**
  - AC1: `SuspectGenerationAgent` class/definition exists.
  - AC2: Agent instructions clearly define its purpose for generating 2-3 suspect profiles based on case context.
  - AC3: `SuspectProfile` Pydantic model is defined.
  - AC4: Agent can be invoked (in isolation for testing) and produces a list of 2-3 `SuspectProfile` like structures (even if MMOs are not yet attached).
- **Dependencies:** Story 1.5 (for `CaseContext` and `VictimProfile` definitions).

---

### Story 2.2: Define MMO Generation Agent & Logic

- **User Story / Goal:** As a Developer, I want an agent capability (either within `SuspectGenerationAgent` or a new `MMOGenerationAgent`) to generate a plausible Means, Motive, and Opportunity (MMO) for a given suspect profile and case context.
- **Detailed Requirements:**
  - Decide on agent structure: either extend `SuspectGenerationAgent` or create a new `MMOGenerationAgent`.
  - The agent instructions must guide the LLM to generate one distinct Means, one Motive, and one Opportunity for a single suspect, ensuring logical consistency with the suspect's profile, the victim's details, and the overall case theme.
  - Define a Pydantic model `MMO` (means: str, motive: str, opportunity: str).
  - The agent performing MMO generation should output an `MMO` object for a suspect.
- **Acceptance Criteria (ACs):**
  - AC1: Agent structure for MMO generation is defined.
  - AC2: Agent instructions clearly guide the LLM to create plausible Means, Motive, and Opportunity for one suspect.
  - AC3: `MMO` Pydantic model is defined.
  - AC4: Agent can be invoked with a `SuspectProfile` and `CaseContext`, and it returns a populated `MMO` object.
- **Dependencies:** Story 2.1.

---

### Story 2.3: Integrate Suspect & MMO Generation

- **User Story / Goal:** As a Developer, I want the system to generate 2-3 suspects, and for each suspect, generate their full MMO, then integrate this into the main `CaseContext` data structure.
- **Detailed Requirements:**
  - The `OrchestratorAgent` (or main script) will first call the `CaseInitializationAgent` (from Epic 1) to get `CaseContext`.
  - Then, the `OrchestratorAgent` will call the `SuspectGenerationAgent` (and `MMOGenerationAgent` if separate). This might involve a loop:
    - Generate a `SuspectProfile`.
    - For that `SuspectProfile`, generate its `MMO`.
    - Combine them into a new Pydantic model, e.g., `Suspect` (containing `SuspectProfile` and `MMO`).
  - Collect all `Suspect` objects into a list.
  - Update the main `CaseContext` Pydantic model to include `suspects: List[Suspect]`.
  - The final output of this epic's flow is the `CaseContext` now containing the list of suspects, each with their profile and MMO.
- **Acceptance Criteria (ACs):**
  - AC1: The `OrchestratorAgent` successfully orchestrates the generation of 2-3 suspects.
  - AC2: Each generated suspect has a complete `SuspectProfile` and a complete `MMO` object associated with them.
  - AC3: The `CaseContext` Pydantic model is updated to include a list of these `Suspect` objects.
  - AC4: The orchestrator can output (print/log) the `CaseContext` showing victim, theme, and all suspects with their MMOs.
- **Dependencies:** Story 1.6, Story 2.1, Story 2.2.

---

### Story 2.4: Handoffs & Data Flow for Suspect/MMO Generation

- **User Story / Goal:** As an `OrchestratorAgent`, I want to correctly manage the data flow and handoffs between case initialization and suspect/MMO generation, ensuring all necessary context is passed and results are aggregated.
- **Detailed Requirements:**
  - Ensure the `CaseContext` (with victim details and theme from Epic 1) is correctly passed as input to the `SuspectGenerationAgent` (and `MMOGenerationAgent` if applicable).
  - Ensure the list of fully formed `Suspect` objects (profile + MMO) is correctly returned to the `OrchestratorAgent`.
  - The `OrchestratorAgent` updates its main `CaseContext` with this new list of suspects.
- **Acceptance Criteria (ACs):**
  - AC1: Data flows correctly from `CaseInitializationAgent` output to `SuspectGenerationAgent` input.
  - AC2: `SuspectGenerationAgent` (and `MMOGenerationAgent`) produce the expected list of `Suspect` objects.
  - AC3: The `OrchestratorAgent` successfully incorporates the suspect list into the main `CaseContext`.
  - AC4: No data is lost or corrupted during handoffs relevant to this epic.
- **Dependencies:** Story 2.3.

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
|        |      | 0.1     | Initial draft of Epic 2 | PM Agent | 