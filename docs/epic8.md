# Epic 8: System Orchestration & Data Model Finalization for Phase 2

**Goal:** Ensure all Phase 2 features (from Epics 5, 6, and 7) are correctly and cohesively integrated into the main orchestration flow, that all Pydantic data models (`CaseContext`, `VictimProfile`, `SuspectProfile`, `EvidenceItem`, and any new ones) are finalized and consistently used, and that the overall system functions reliably with these enhancements.

**Deployability:** This is the capstone epic for Phase 2. Upon its completion, Mystery.AI will have demonstrably incorporated all the new diversity and evidence richness features. The final JSON output will consistently reflect all new data fields and thematic integrations. The system will be stable and ready for Phase 3 (Branching Evidence Architecture & Design).

## Epic-Specific Technical Context

This epic primarily involves refining and solidifying work done in Epics 5, 6, and 7, with a focus on integration, data consistency, and overall system robustness.

- **Orchestration Logic (`main_orchestrator.py`):**
    - Final review and refactoring of the orchestration flow to ensure:
        - Correct sequencing of all new and modified agent calls (`PreInitializationIdeationAgent`, `CaseInitializationAgent`, `SuspectGenerationAgent`, `EvidenceGenerationAgent`).
        - Efficient and clear handling of data pass-through (e.g., master list sub-selections, generated name lists, evidence category options).
        - Robust error handling for new agent interactions or data processing steps.
- **Pydantic Models (`core/data_models.py`):**
    - Final validation of all data models modified or introduced in Phase 2 (e.g., `VictimProfile`, `SuspectProfile`, `EvidenceItem`, `ThematicNameLists`).
    - Ensure all descriptions, field types, and default values are correct and consistently applied.
    - Update `docs/data-models.md` to comprehensively reflect the final state of all Pydantic models and the overall `CaseContext` JSON schema after Phase 2 changes.
- **Configuration Management (`MurderMysteryGen/config/`):
    - Ensure master lists (attributes, evidence categories) are stored in their finalized JSON format in `MurderMysteryGen/config/master_lists/` and are correctly loaded by the orchestrator.
    - Confirm any new configurable parameters (e.g., number of items to select for sub-lists, number of names to generate) are handled appropriately (e.g., constants, config file entries).
- **Logging & Debugging:**
    - Enhance logging throughout the orchestration and within modified agents to provide clear traceability for the new diversity and evidence crafting features (e.g., log selected list items, chosen categories, generated names).

## Local Testability & Command-Line Access

- **Execution:** `python -m src.mystery_ai.main --theme "Your Theme"`
- **Output:** The generated JSON in `generated_mysteries/` must be complete, well-formed, and accurately reflect all Phase 2 enhancements. This includes thematically integrated attributes, dynamically generated names, and evidence items with categories and narrative function descriptions.
- **Testing:**
    - End-to-end testing with a variety of themes to ensure consistent performance and output quality.
    - Rigorous manual review of generated JSON outputs for data integrity, coherence, and completeness of all new fields.
    - Verification that `docs/data-models.md` accurately represents the final JSON structure.

## User Stories

---

### Story 8.1: Finalize Orchestration Flow for Phase 2 Features

- **User Story / Goal:** As a Developer, I want to ensure the `main_orchestrator.py` correctly and robustly sequences all agent calls and data handoffs for the new diversity and evidence crafting features.
- **Detailed Requirements:**
    - Review and refactor the orchestration logic in `main_orchestrator.py` that handles Epics 5, 6, and 7 functionalities.
    - Confirm correct data flow: master list loading, sub-list creation, `PreInitializationIdeationAgent` call, passing names and attribute options to `CaseInitializationAgent` and `SuspectGenerationAgent`, passing evidence category options to `EvidenceGenerationAgent`.
    - Implement or verify basic error handling around new agent calls.
- **Acceptance Criteria (ACs):**
    - AC1: Orchestrator executes all new and modified agent calls in the correct logical order.
    - AC2: Data (lists, selected items, options) is correctly passed between the orchestrator and relevant agents.
    - AC3: The orchestration is resilient to common, expected variations in agent outputs (e.g., an agent returning an empty list if it cannot fulfill a request under specific rare conditions, though this should be minimized by prompt design).
- **Dependencies:** Story 5.2, Story 5.3, Story 6.2, Story 6.3, Story 6.4, Story 7.3, Story 7.4.
- **Status:** To Do

---

### Story 8.2: Validate and Finalize Pydantic Data Models for Phase 2

- **User Story / Goal:** As a Developer, I want to ensure all Pydantic models impacted by Phase 2 changes are accurate, consistent, and well-documented, and that the main `CaseContext` schema is updated.
- **Detailed Requirements:**
    - Review all Pydantic models in `core/data_models.py` that were modified or added in Epics 5, 6, 7 (e.g., `VictimProfile`, `SuspectProfile`, `EvidenceItem`, any new models like `ThematicNameLists`).
    - Verify field types, descriptions, optionality, and default values.
    - Generate the final `CaseContext.model_json_schema()` and update `docs/data-models.md` with this new schema and explanations for any new fields or models.
- **Acceptance Criteria (ACs):**
    - AC1: All Phase 2 related Pydantic models are validated for correctness and consistency.
    - AC2: Descriptions for all new/modified fields are clear and accurate.
    - AC3: `docs/data-models.md` is updated to reflect the complete and final data structures for Phase 2, including the full `CaseContext` JSON schema.
- **Dependencies:** Story 5.4, Story 7.2.
- **Status:** To Do

---

### Story 8.3: Standardize Configuration and Master List Management

- **User Story / Goal:** As a Developer, I want to ensure that all master lists (attributes, evidence categories) and any new system configurations are stored and accessed in a consistent and maintainable way.
- **Detailed Requirements:**
    - Finalize the storage mechanism for master lists as JSON files in `MurderMysteryGen/config/master_lists/`.
    - Ensure the orchestrator loads these lists robustly.
    - Document how to update these master lists.
    - Confirm any configurable parameters (e.g., number of items in sub-lists) are clearly defined (e.g., as constants at the top of `main_orchestrator.py` or in a simple config file).
- **Acceptance Criteria (ACs):**
    - AC1: Master lists for attributes and evidence categories are stored in a finalized, easily editable location.
    - AC2: Loading mechanism for these lists in the orchestrator is robust.
    - AC3: Process for updating master lists is documented for the developer.
    - AC4: Any Phase 2 specific configurable parameters are clearly defined and accessible.
- **Dependencies:** Story 5.1, Story 7.1.
- **Status:** To Do

---

### Story 8.4: Comprehensive End-to-End Testing and Logging Review for Phase 2

- **User Story / Goal:** As a Developer, I want to perform comprehensive end-to-end testing of all Phase 2 features and review system logging to ensure clarity and completeness for debugging and monitoring.
- **Detailed Requirements:**
    - Execute the full mystery generation pipeline with a diverse set of at least 3-5 themes.
    - Manually review each generated JSON output for:
        - Correct integration of selected attributes (from static lists).
        - Use of thematically appropriate names (from dynamic lists).
        - Presence and correctness of `evidence_category` and `narrative_function_description` in all evidence items.
        - Overall coherence and data integrity.
    - Review console logs and any file logs to ensure new operations are adequately logged and error messages are clear.
- **Acceptance Criteria (ACs):**
    - AC1: System successfully generates complete mysteries incorporating all Phase 2 features for at least 3 diverse test themes without unhandled exceptions.
    - AC2: Manual review confirms data integrity and correct feature implementation in the JSON outputs.
    - AC3: System logging provides sufficient insight into the selection and generation processes introduced in Phase 2.
    - AC4: Any identified bugs or inconsistencies from testing are addressed and re-verified.
- **Dependencies:** Story 8.1, Story 8.2, Story 8.3.
- **Status:** To Do

--- 