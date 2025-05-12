# Epic 7: Advanced Individual Evidence Crafting

**Goal:** Enhance `EvidenceGenerationAgent` and the `EvidenceItem` data model to include Evidence Categories and Narrative Function Descriptions, making individual pieces of evidence richer, more varied, and more strategically nuanced.

**Deployability:** This epic builds upon the foundational diversity introduced in Epics 5 & 6. After this epic, generated evidence items will not only describe the evidence but also classify its type (e.g., "Letter," "Financial Record," "Witness Statement") and articulate its intended narrative function (e.g., "Directly implicates if X is known," "Subtle clue requiring Y to understand," "Red herring appearing to support Z"). This provides richer building blocks for future complex evidence structures and more nuanced mystery designs. The `CaseContext` JSON output will reflect these new fields within each `EvidenceItem`.

## Epic-Specific Technical Context

- **New Master List (`MurderMysteryGen/config/master_lists/`):**
    - A master list (JSON file) of **Evidence Categories/Types** (e.g., "Personal Correspondence," "Official Document," "Financial Record," "Physical Object Description," "Witness Testimony Snippet," "Digital Footprint," "News Clipping," "Forensic Report Snippet").
- **Orchestration Logic (`main_orchestrator.py`):**
    - Logic to load the master list of Evidence Categories.
    - When preparing to call `EvidenceGenerationAgent` for each suspect, the orchestrator will select a subset of these categories (e.g., 3-5 varied types, or all of them) to provide as options to the agent. This ensures the agent doesn't always pick from the same small set or generate only one type of evidence.
- **Agent Modifications (`EvidenceGenerationAgent` in `agents/evidence_generator.py`):
    - **Input Handling:** Updated to accept a list of allowed `Evidence Categories`.
    - **Internal Logic/Prompt:**
        - Tasked to select an appropriate `evidence_category` from the provided list for each piece of evidence it generates.
        - Tasked to generate a new `narrative_function_description` text field. This field should explain the intended role or subtlety of the evidence (e.g., "This is a direct piece of evidence pointing to motive," "This clue is subtle and requires connecting A to B," "This is a red herring designed to make the player suspect Y because of Z").
        - Prompts will need careful crafting to guide the LLM in generating meaningful descriptions for both these new fields, consistent with the evidence itself and the suspect's situation (killer vs. red herring).
    - **Output:** Will still produce a list of `EvidenceItem` objects, but each object will now be populated with the new fields.
- **Pydantic Model Updates (`core/data_models.py`):
    - `EvidenceItem` model will be extended with two new fields:
        - `evidence_category: str = Field(description="The type or category of the evidence, e.g., 'Letter', 'Financial Record'.")`
        - `narrative_function_description: str = Field(description="An explanation of the evidence's intended narrative role, subtlety, or how it functions as a clue or red herring.")`

## Local Testability & Command-Line Access

- **Execution:** `python -m src.mystery_ai.main --theme "Your Theme"`
- **Output:** The `evidence_items` array in the generated JSON should now contain objects where each `EvidenceItem` has the new `evidence_category` and `narrative_function_description` fields populated.
- **Testing:**
    - Manually review generated evidence to ensure the chosen `evidence_category` is appropriate for the evidence `description`.
    - Evaluate the `narrative_function_description` for clarity, coherence with the evidence, and its usefulness in understanding the clue's role.
    - Verify that a variety of evidence categories are used across a full case generation.
    - Logging should indicate the list of categories provided to the agent and the category selected for each item.

## User Stories

---

### Story 7.1: Define Master List of Evidence Categories

- **User Story / Goal:** As a Developer, I want to define a master list of diverse Evidence Categories/Types so that the system can generate a wider variety of evidence items.
- **Detailed Requirements:**
    - Create an easily editable JSON file in `MurderMysteryGen/config/master_lists/` for the master list of evidence categories.
    - Populate with an initial set of at least 10-15 diverse and commonly found evidence types in mysteries.
- **Acceptance Criteria (ACs):**
    - AC1: Master list file/module for Evidence Categories exists.
    - AC2: The list contains at least 10 distinct and relevant evidence categories.
    - AC3: The list is loadable by the orchestrator.
- **Dependencies:** None.
- **Status:** To Do

---

### Story 7.2: Update `EvidenceItem` Data Model

- **User Story / Goal:** As a Developer, I want to extend the `EvidenceItem` Pydantic model to include fields for `evidence_category` and `narrative_function_description`.
- **Detailed Requirements:**
    - Add `evidence_category: str` to the `EvidenceItem` model in `core/data_models.py`.
    - Add `narrative_function_description: str` to the `EvidenceItem` model.
    - Update any associated documentation or schemas (e.g., `docs/data-models.md` will eventually need to reflect this).
- **Acceptance Criteria (ACs):**
    - AC1: `EvidenceItem.evidence_category` field is defined correctly with a description.
    - AC2: `EvidenceItem.narrative_function_description` field is defined correctly with a description.
    - AC3: The `EvidenceItem` model remains valid and serializable.
- **Dependencies:** None.
- **Status:** To Do

---

### Story 7.3: Enhance `EvidenceGenerationAgent` for Richer Evidence

- **User Story / Goal:** As a Developer, I want to modify the `EvidenceGenerationAgent` to select an evidence category, generate a narrative function description, and populate these new fields in the `EvidenceItem`.
- **Detailed Requirements:**
    - Update the agent's input handling to accept a list of allowed `Evidence Categories` from the orchestrator.
    - Modify the agent's internal logic/prompt to:
        - Select an appropriate `evidence_category` from the provided options for each piece of evidence.
        - Generate a meaningful `narrative_function_description` that explains the evidence's role, subtlety, or connection logic.
        - Populate these new fields in each outputted `EvidenceItem` object.
- **Acceptance Criteria (ACs):**
    - AC1: `EvidenceGenerationAgent` accepts a list of evidence category options as input.
    - AC2: Agent successfully selects a category for each generated `EvidenceItem` from the provided options.
    - AC3: Agent generates a `narrative_function_description` for each `EvidenceItem`.
    - AC4: Both new fields are correctly populated in all `EvidenceItem` objects returned by the agent.
    - AC5: The chosen category and narrative function description are coherent with the evidence's main `description` and its role (true clue vs. red herring).
- **Dependencies:** Story 7.1, Story 7.2.
- **Status:** To Do

---

### Story 7.4: Orchestrator - Provide Evidence Category Options to Agent

- **User Story / Goal:** As a Developer, I want the orchestrator to load the master list of Evidence Categories and provide a relevant sub-list of these categories as input to the `EvidenceGenerationAgent`.
- **Detailed Requirements:**
    - Implement logic in `main_orchestrator.py` to load the master list of Evidence Categories.
    - Before calling `EvidenceGenerationAgent` for a suspect, prepare a sub-list of evidence categories (e.g., select 3-5 diverse options, or pass all). This strategy can be refined.
    - Pass this sub-list to the `EvidenceGenerationAgent` as part of its input.
- **Acceptance Criteria (ACs):**
    - AC1: Orchestrator successfully loads the master list of Evidence Categories.
    - AC2: Orchestrator provides a sub-list of evidence categories as input to `EvidenceGenerationAgent`.
    - AC3: The method of selecting the sub-list ensures a reasonable variety of options are presented to the agent over time or for different evidence items.
- **Dependencies:** Story 7.1, Story 7.3.
- **Status:** To Do

--- 