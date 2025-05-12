# Epic 5: Static List Integration for Core Attributes

**Goal:** Implement the selection of Cause of Death, Motive Category, Occupation Archetype, and Personality Archetype from predefined lists and their thematic integration into victim/suspect profiles, enhancing foundational diversity.

**Deployability:** This epic builds upon the completed MVP (Epics 1-4). After this epic, the system will produce mysteries where core victim (and potentially suspect) attributes are chosen from a curated set of options, leading to more varied outputs. The `CaseContext` JSON will reflect these explicitly chosen attributes or their thematic integration. Testability involves running the main script and verifying that generated profiles incorporate elements from these new lists coherently.

## Epic-Specific Technical Context

- **New Master Lists:** Simple configuration files (JSON) will be created in `MurderMysteryGen/config/master_lists/` to store master lists for:
    - Cause of Death (user-provided initial list).
    - Motive Categories (e.g., Revenge, Financial Gain, Passion, Fear, Ideology).
    - Generic Occupation Archetypes (e.g., Executive, Laborer, Artisan, Scholar, Performer, Service Worker, Unemployed, Retired).
    - Personality Archetypes/Core Traits (e.g., Ambitious, Greedy, Resentful, Fearful, Idealistic, Deceptive, Loyal, Introverted, Extroverted).
- **Orchestration Logic (`main_orchestrator.py`):**
    - Logic to load these master lists.
    - Logic to randomly select a small subset (e.g., 2-3 items) from each master list at the start of a generation run.
    - Pass these selected sub-lists as input to the `CaseInitializationAgent` (and `SuspectGenerationAgent` if suspect attributes are also chosen this way).
- **Agent Modifications:**
    - `CaseInitializationAgent` (in `agents/case_initializer.py`):
        - Instructions updated to accept parameters for Cause of Death options, Motive Category options, Occupation options, and Personality options.
        - Logic to select one item from each provided option list.
        - Prompts enhanced to ensure thematic integration of the *selected* items into the victim's `name`, `occupation`, `personality`, and `cause_of_death` fields.
    - `SuspectGenerationAgent` (in `agents/suspect_generator.py`) (Potentially): If it's decided that suspects also get occupations/personalities from lists, this agent would undergo similar modifications.
- **Pydantic Model Updates (`core/data_models.py`):**
    - `VictimProfile`: May need new optional fields like `chosen_cause_of_death_category: Optional[str]`, `chosen_motive_category: Optional[str]`, `chosen_occupation_archetype: Optional[str]`, `chosen_personality_archetype: Optional[str]` if explicit tracking of the *selected category* is desired in the output, in addition to its thematic integration into existing fields.
    - `SuspectProfile`: Similar fields if applicable.
    - Input models for agents might be introduced or existing dicts structured to pass these option lists clearly.

## Local Testability & Command-Line Access

- **Execution:** `python -m src.mystery_ai.main --theme "Your Theme"`
- **Output:** The generated JSON in `generated_mysteries/` should show victim profiles whose attributes (cause of death, occupation, personality, and the implied motive for the crime against them) are clearly influenced by and consistent with items selected from the new master lists. If explicit tracking fields are added to models, these should be populated.
- **Testing:** Manual review of outputs against master lists and theme for coherence. Logs should indicate which sub-lists were provided to agents and which specific items were chosen (if feasible to log).

## User Stories

---

### Story 5.1: Define and Store Master Attribute Lists

- **User Story / Goal:** As a Developer, I want to define and store master lists for Cause of Death, Motive Categories, Occupation Archetypes, and Personality Archetypes so they can be used by the generation system.
- **Detailed Requirements:**
    - Create easily editable JSON files in `MurderMysteryGen/config/master_lists/` for each master list.
    - Populate with initial sets of diverse options (Cause of Death list is user-provided; others to be defined).
    - Ensure these lists can be loaded by the orchestrator.
- **Acceptance Criteria (ACs):**
    - AC1: Master list file/module exists for Cause of Death.
    - AC2: Master list file/module exists for Motive Categories (min 5 diverse categories).
    - AC3: Master list file/module exists for Occupation Archetypes (min 10 diverse archetypes).
    - AC4: Master list file/module exists for Personality Archetypes (min 10 diverse archetypes).
    - AC5: Orchestrator includes placeholder logic to load these lists (actual loading can be part of story 5.2).
- **Dependencies:** None.
- **Status:** COMPLETED

---

### Story 5.2: Orchestrator - Attribute Sub-list Selection

- **User Story / Goal:** As a Developer, I want the orchestrator to load the master attribute lists, randomly select a small sub-list (e.g., 2-3 items) from each, and prepare them for input to the `CaseInitializationAgent`.
- **Detailed Requirements:**
    - Implement logic in `main_orchestrator.py` to load all master lists defined in Story 5.1.
    - Implement logic to randomly select N (configurable, default 3) items from each master list.
    - Structure these sub-lists into a format suitable for passing to `CaseInitializationAgent` (e.g., within its input dictionary).
- **Acceptance Criteria (ACs):**
    - AC1: Orchestrator successfully loads all master attribute lists.
    - AC2: Orchestrator creates sub-lists of the configured size for each attribute type.
    - AC3: The selection process is random (or pseudo-random).
    - AC4: The sub-lists are correctly passed or prepared for the `CaseInitializationAgent`.
- **Dependencies:** Story 5.1.
- **Status:** COMPLETED

---

### Story 5.3: `CaseInitializationAgent` - Integrate Selected Attributes

- **User Story / Goal:** As a Developer, I want to modify the `CaseInitializationAgent` to accept sub-lists of attribute options (Cause of Death, Motive Category, Occupation, Personality), select one from each, and thematically integrate the selected options into the generated `VictimProfile`.
- **Detailed Requirements:**
    - Update `CaseInitializationAgent`'s input handling to receive the attribute option sub-lists from the orchestrator.
    - Modify the agent's internal logic/prompt to first select one item from each provided sub-list.
    - Crucially, update the agent's prompt to ensure it *thematically integrates* the chosen items into the victim's existing `name`, `occupation`, `personality`, and `cause_of_death` fields, rather than just appending them. The theme remains paramount.
    - The agent should still output a `VictimProfile` object.
- **Acceptance Criteria (ACs):**
    - AC1: `CaseInitializationAgent` accepts new input parameters for attribute option sub-lists.
    - AC2: Agent successfully selects one option from each provided sub-list.
    - AC3: The agent's output `VictimProfile` thematically reflects the selected Cause of Death in its `cause_of_death` field.
    - AC4: The agent's output `VictimProfile` thematically reflects the selected Occupation Archetype in its `occupation` field.
    - AC5: The agent's output `VictimProfile` thematically reflects the selected Personality Archetype in its `personality` field.
    - AC6: The agent's output `VictimProfile` (and the scenario implied by it) thematically reflects the selected Motive Category for the crime against the victim.
    - AC7: The integration of selected attributes appears natural and consistent with the overall theme.
- **Dependencies:** Story 5.2.
- **Status:** COMPLETED

---

### Story 5.4: Data Model Updates for Attribute Tracking (Optional)

- **User Story / Goal:** As a Developer, I want to update the `VictimProfile` (and `SuspectProfile` if applicable) Pydantic models to include optional fields for explicitly storing the *category* of the chosen attributes, if deemed necessary for downstream processing or debugging.
- **Detailed Requirements:**
    - Discuss and decide if explicit tracking fields (e.g., `chosen_motive_category: str`) are needed in `VictimProfile` / `SuspectProfile` beyond the thematic integration into existing descriptive fields.
    - If yes, add these optional fields to the relevant Pydantic models in `core/data_models.py`.
    - Update `CaseInitializationAgent` (and `SuspectGenerationAgent`) to populate these fields with the chosen category name.
- **Acceptance Criteria (ACs):**
    - AC1: Decision on necessity of explicit tracking fields is made and documented.
    - AC2: (If yes) `VictimProfile` (and `SuspectProfile`) models are updated with new optional fields for chosen attribute categories.
    - AC3: (If yes) Relevant agent(s) correctly populate these new fields in their output.
    - AC4: (If yes) The final JSON output reflects these new fields when populated.
- **Dependencies:** Story 5.3.
- **Status:** COMPLETED

--- 