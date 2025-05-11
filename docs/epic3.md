# Epic 3: Killer Selection, MMO Modification & Initial Evidence Generation

**Goal:** Implement the logic for an agent to designate one suspect as the killer, appropriately weaken an MMO element for all non-killer suspects, and then generate a small, distinct set of initial evidence pieces (both direct and red herring) for all suspects.

**Deployability:** This epic builds upon the `CaseContext` containing suspects with full MMOs (from Epic 2). It introduces agent capabilities for critical plot mechanics: selecting the killer, modifying other suspects to create red herrings, and generating initial evidence. The output will be the `CaseContext` now augmented with a designated killer, modified MMOs for non-killers, and a list of evidence items. This is a significant step towards a complete mystery core.

## Epic-Specific Technical Context

- **New Agent Definitions:** `KillerSelectionAgent`, `MMOModificationAgent`, `EvidenceGenerationAgent` (these could be combined or kept separate for modularity).
- **Pydantic Model Updates:**
  - `Suspect` model: Add `is_killer: bool` field. Add optional fields for `modified_means: str`, `modified_motive: str`, `modified_opportunity: str` or a nested `ModifiedMMO` object.
  - `EvidenceItem` model: (e.g., description: str, related_suspect_name: str, points_to_mmo_element: str enum{Means, Motive, Opportunity}, is_red_herring: bool).
  - `CaseContext`: Update to include a list of `EvidenceItem` objects.
- **Logic Implementation:** Develop Python logic within agents for random killer selection, strategic (or random for MVP) weakening of one MMO element for non-killers, and prompting for evidence generation tailored to original/modified MMOs.

## Local Testability & Command-Line Access

- **Local Development:** Test script loads `CaseContext` from Epic 2 (or runs Epics 1 & 2) then triggers Epic 3 functionality.
- **Output:** Script outputs the `CaseContext` with killer identified, non-killer MMOs modified, and initial evidence list, for verification.

## Story List

### Story 3.1: Define Killer Selection & MMO Modification Agent(s)

- **User Story / Goal:** As a Developer, I want specialized agent capabilities to select a killer from the suspect list and then modify the MMOs of non-killer suspects to create red herrings.
- **Detailed Requirements:**
  - Define `KillerSelectionAgent`: Takes the list of `Suspect` objects; randomly selects one as the killer; updates the `is_killer` flag on the `Suspect` objects.
  - Define `MMOModificationAgent`: For each non-killer `Suspect`, this agent will choose one element of their original MMO (Means, Motive, or Opportunity – randomly for MVP) and prompt an LLM to generate a significantly weakened or invalidated version of that element. The original MMO should be preserved, and the modified element stored.
  - Update `Suspect` Pydantic model: add `is_killer: bool` and fields to store the modified MMO element (e.g., `modified_mmo_element_type: str`, `modified_mmo_element_description: str`, or a more structured `ModifiedMMO` object).
- **Acceptance Criteria (ACs):**
  - AC1: `KillerSelectionAgent` and `MMOModificationAgent` (or combined equivalent) are defined.
  - AC2: `KillerSelectionAgent` correctly flags one suspect as killer and others as not.
  - AC3: `MMOModificationAgent` plausibly weakens/alters one MMO component for each non-killer suspect.
  - AC4: `Suspect` Pydantic model is updated to reflect killer status and modified MMOs.
- **Dependencies:** Story 2.3.

---

### Story 3.2: Define Evidence Generation Agent

- **User Story / Goal:** As a Developer, I want a specialized `EvidenceGenerationAgent` that can create textual descriptions of evidence items, linking them to specific suspects and their MMO elements.
- **Detailed Requirements:**
  - Define `EvidenceGenerationAgent` using the OpenAI Agents SDK.
  - Agent instructions should guide LLM to generate: 
    - For the killer: 2-3 pieces of evidence directly supporting their original (and still valid) MMO.
    - For non-killers: 1-2 pieces of red herring evidence related to their *original* (now weakened) MMO components, to create misdirection.
  - Define `EvidenceItem` Pydantic model (e.g., `description: str`, `related_suspect_name: str` (or ID), `points_to_mmo_element: str` (Means/Motive/Opportunity), `is_red_herring: bool`).
  - Agent should output a list of `EvidenceItem` objects.
- **Acceptance Criteria (ACs):**
  - AC1: `EvidenceGenerationAgent` class/definition exists.
  - AC2: `EvidenceItem` Pydantic model is defined.
  - AC3: Agent can generate evidence for a killer, consistent with their MMO.
  - AC4: Agent can generate red herring evidence for non-killers, consistent with their original MMOs but leading away from the truth.
- **Dependencies:** Story 3.1.

---

### Story 3.3: Integrate Killer Selection, MMO Modification, and Evidence Generation

- **User Story / Goal:** As a Developer, I want the system to orchestrate the selection of a killer, modification of other suspects' MMOs, and generation of all initial evidence, updating the `CaseContext`.
- **Detailed Requirements:**
  - The `OrchestratorAgent` receives `CaseContext` (with suspects and full MMOs from Epic 2).
  - It calls `KillerSelectionAgent` to mark the killer.
  - It calls `MMOModificationAgent` to weaken MMOs for non-killers.
  - It calls `EvidenceGenerationAgent`, providing it with the list of suspects (with killer status and original/modified MMOs) to generate all evidence items.
  - The list of `EvidenceItem` objects is added to the `CaseContext`.
  - Update `CaseContext` Pydantic model to include `evidence: List[EvidenceItem]`.
- **Acceptance Criteria (ACs):**
  - AC1: Orchestrator correctly calls killer selection, MMO modification, and evidence generation agents in sequence.
  - AC2: `CaseContext` is correctly updated with the `is_killer` flag, modified MMOs, and the list of `EvidenceItem` objects.
  - AC3: The generated evidence list contains appropriate items for both the killer and non-killer suspects.
  - AC4: Orchestrator can output the `CaseContext` showing all new information.
- **Dependencies:** Story 2.3, Story 3.1, Story 3.2.

---

### Story 3.4: Handoffs & Data Flow for Plot Mechanics

- **User Story / Goal:** As an `OrchestratorAgent`, I want to ensure correct data passage through killer selection, MMO modification, and evidence generation stages, maintaining data integrity in `CaseContext`.
- **Detailed Requirements:**
  - Ensure `CaseContext` (with suspects having full MMOs) is correctly passed to `KillerSelectionAgent`.
  - Ensure the updated list of suspects (with `is_killer` flags) is passed to `MMOModificationAgent`.
  - Ensure the list of suspects (with `is_killer` and modified MMOs) is passed to `EvidenceGenerationAgent`.
  - Ensure the generated list of `EvidenceItem` is correctly returned and integrated into the main `CaseContext` by the `OrchestratorAgent`.
- **Acceptance Criteria (ACs):**
  - AC1: Data flows correctly through all agent calls in this epic.
  - AC2: All relevant parts of `CaseContext` (killer status, modified MMOs, evidence list) are accurately populated.
  - AC3: No data corruption occurs during these handoffs.
- **Dependencies:** Story 3.3.

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
|        |      | 0.1     | Initial draft of Epic 3 | PM Agent | 