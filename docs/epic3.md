# Epic 3: Killer Selection, MMO Modification & Initial Evidence Generation

**Goal:** Implement the logic for an agent to designate one suspect as the killer, appropriately weaken an MMO element for all non-killer suspects, and then generate a small, distinct set of initial evidence pieces (both direct and red herring) for all suspects.

**Deployability:** This epic builds upon the `CaseContext` containing suspects with full MMOs (from Epic 2). It introduces agent capabilities for critical plot mechanics: selecting the killer, modifying other suspects to create red herrings, and generating initial evidence. The output will be the `CaseContext` now augmented with a designated killer, modified MMOs for non-killers, and a list of evidence items. This is a significant step towards a complete mystery core.

## Epic-Specific Technical Context

- **Agent Logic:** `select_killer_randomly` function implemented. `MMOModificationAgent` and `EvidenceGenerationAgent` defined and integrated.
- **Pydantic Model Updates:** `Suspect` model updated with `is_killer` and `modified_mmo_elements`. `ModifiedMMOElement`, `MMOElementType`, and `EvidenceItem` models defined. `CaseContext` updated with `evidence_items`.
- **Orchestration:** `main_orchestrator.py` now handles killer selection, MMO modification loop, and evidence generation loop for all suspects.

## Local Testability & Command-Line Access

- **Local Development:** Main script (`src/mystery_ai/main.py`) runs Epics 1, 2, and 3.
- **Output:** Script outputs the `CaseContext` with killer identified, non-killer MMOs modified, and the initial evidence list for verification.

## Story List

### Story 3.1: Define Killer Selection & MMO Modification Agent(s)

- **User Story / Goal:** As a Developer, I want specialized agent capabilities/logic to select a killer from the suspect list and then modify the MMOs of non-killer suspects to create red herrings.
- **Detailed Requirements:** Implemented (Python function for killer selection, `MMOModificationAgent` for modifications).
- **Acceptance Criteria (ACs):**
  - AC1: `select_killer_randomly` function and `MMOModificationAgent` are defined and used. **(COMPLETED)**
  - AC2: Killer selection logic correctly flags one suspect as killer. **(COMPLETED)**
  - AC3: `MMOModificationAgent` (called by orchestrator) plausibly weakens/alters one MMO component for each non-killer suspect. **(COMPLETED)**
  - AC4: `Suspect` Pydantic model reflects killer status and modified MMOs. **(COMPLETED)**
- **Dependencies:** Story 2.3.
- **Status:** COMPLETED

---

### Story 3.2: Define Evidence Generation Agent

- **User Story / Goal:** As a Developer, I want a specialized `EvidenceGenerationAgent` that can create textual descriptions of evidence items, linking them to specific suspects and their MMO elements.
- **Detailed Requirements:** Implemented.
- **Acceptance Criteria (ACs):**
  - AC1: `EvidenceGenerationAgent` class/definition exists. **(COMPLETED)**
  - AC2: `EvidenceItem` Pydantic model is defined. **(COMPLETED)**
  - AC3: Agent (called by orchestrator) generates evidence for the killer, consistent with their MMO. **(COMPLETED)**
  - AC4: Agent (called by orchestrator) generates red herring evidence for non-killers. **(COMPLETED)**
- **Dependencies:** Story 3.1.
- **Status:** COMPLETED

---

### Story 3.3: Integrate Killer Selection, MMO Modification, and Evidence Generation

- **User Story / Goal:** As a Developer, I want the system to orchestrate the selection of a killer, modification of other suspects' MMOs, and generation of all initial evidence, updating the `CaseContext`.
- **Detailed Requirements:** Implemented in `main_orchestrator.py`.
- **Acceptance Criteria (ACs):**
  - AC1: Orchestrator correctly calls killer selection, MMO modification, and evidence generation logic/agents in sequence. **(COMPLETED)**
  - AC2: `CaseContext` is correctly updated with `is_killer` flag, modified MMOs, and the list of `EvidenceItem` objects. **(COMPLETED)**
  - AC3: The generated evidence list contains appropriate items for both the killer and non-killer suspects. **(COMPLETED)**
  - AC4: Orchestrator can output the `CaseContext` showing all new information. **(COMPLETED)**
- **Dependencies:** Story 2.3, Story 3.1, Story 3.2.
- **Status:** COMPLETED

---

### Story 3.4: Handoffs & Data Flow for Plot Mechanics

- **User Story / Goal:** As an `OrchestratorAgent`, I want to ensure correct data passage through killer selection, MMO modification, and evidence generation stages, maintaining data integrity in `CaseContext`.
- **Detailed Requirements:** Implemented in `main_orchestrator.py`.
- **Acceptance Criteria (ACs):**
  - AC1: Data flows correctly through all logic/agent calls in this epic. **(COMPLETED)**
  - AC2: All relevant parts of `CaseContext` (killer status, modified MMOs, evidence list) are accurately populated. **(COMPLETED)**
  - AC3: No data corruption occurs during these handoffs/data manipulations. **(COMPLETED)**
- **Dependencies:** Story 3.3.
- **Status:** COMPLETED

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
|        |      | 0.1     | Initial draft of Epic 3 | PM Agent |
|        |      | 0.2     | Marked stories 3.1-3.4 COMPLETED after successful integration and test. | Dev Agent | 