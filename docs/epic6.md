# Epic 6: Dynamic Thematic Name Generation

**Goal:** Develop the `PreInitializationIdeationAgent` to generate theme-specific first and last names and integrate their usage into victim and suspect profiling, further enhancing diversity and thematic consistency.

**Deployability:** This epic builds upon Epic 5 (where core attributes are diversified). After this epic, the system will generate victim and suspect names that are dynamically created based on the specific theme of the mystery, rather than relying on the LLM to invent them from whole cloth during profile generation. This should lead to more thematically consistent and varied naming. The `CaseContext` JSON will reflect these names.

## Epic-Specific Technical Context

- **New Agent (`PreInitializationIdeationAgent`):**
    - Defined in a new file, e.g., `agents/pre_initialization_ideation_agent.py`.
    - **Input:** Theme string.
    - **Task:** Generate two lists: one of N (e.g., 50) thematically plausible First Names, and one of N (e.g., 50) thematically plausible Last Names.
    - **Output:** A structured output (e.g., a Pydantic model or a dictionary) containing these two lists of strings.
    - **Instructions:** Prompts for this agent will be critical to ensure it understands how to generate names appropriate to diverse themes (e.g., "Cyberpunk" vs. "Medieval Fantasy" vs. "1920s Noir").
- **Orchestration Logic (`main_orchestrator.py`):**
    - The `PreInitializationIdeationAgent` will be called early in the orchestration, right after the theme is established, and before `CaseInitializationAgent`.
    - The generated lists of names will be extracted from the agent's output and passed as input to `CaseInitializationAgent` (and subsequently to `SuspectGenerationAgent`, possibly via the evolving `CaseContext`).
- **Agent Modifications:**
    - `CaseInitializationAgent` (in `agents/case_initializer.py`):
        - Updated to accept parameters for the list of first names and list of last names.
        - Modified to select names from these lists when generating the `VictimProfile.name`.
        - Prompts adjusted to use these provided names as the basis for the victim's full name.
    - `SuspectGenerationAgent` (in `agents/suspect_generator.py`):
        - Similarly updated to accept name lists (likely passed via `CaseContext` or through its direct inputs from the orchestrator).
        - Modified to select names from these lists when generating `SuspectProfile.name` for each suspect.
- **Pydantic Model Updates (`core/data_models.py`):**
    - A new Pydantic model might be created for the output of `PreInitializationIdeationAgent` (e.g., `ThematicNameLists(first_names: List[str], last_names: List[str])`).
    - `CaseContext`: May be updated to temporarily store these generated name lists if they need to be passed through multiple subsequent agents not directly involved in naming.
    - Input models for `CaseInitializationAgent` and `SuspectGenerationAgent` will be adapted if they use specific input schemas.

## Local Testability & Command-Line Access

- **Execution:** `python -m src.mystery_ai.main --theme "Your Theme"`
- **Output:** The victim and suspect names in the generated JSON should be drawn from the lists produced by the `PreInitializationIdeationAgent` and should be thematically appropriate.
- **Testing:**
    - Manually review the generated name lists from `PreInitializationIdeationAgent` for thematic consistency and variety across several different themes.
    - Verify that victim and suspect names in the final output are indeed from these lists.
    - Logging should show the generated lists and the names selected for characters.

## User Stories

---

### Story 6.1: Design and Implement `PreInitializationIdeationAgent` for Names

- **User Story / Goal:** As a Developer, I want to create a `PreInitializationIdeationAgent` that can generate lists of thematically appropriate first and last names based on an input theme.
- **Detailed Requirements:**
    - Create the agent definition in `agents/pre_initialization_ideation_agent.py`.
    - Develop robust instructions and prompts for the agent to generate N (e.g., 50) first names and N last names that are plausible and fitting for a given theme.
    - Define an output Pydantic model (e.g., `ThematicNameLists`) for the agent to return the lists.
- **Acceptance Criteria (ACs):**
    - AC1: `PreInitializationIdeationAgent` class and file exist.
    - AC2: Agent accepts a theme string as input.
    - AC3: Agent outputs a structured object containing a list of first names and a list of last names.
    - AC4: For at least 3 diverse test themes (e.g., "Cyberpunk Dystopia", "Victorian London", "Wild West Outpost"), the generated name lists are >80% plausible and thematically appropriate upon manual review.
    - AC5: Generated lists demonstrate reasonable variety within each theme.
- **Dependencies:** None.
- **Status:** To Do

---

### Story 6.2: Orchestrate `PreInitializationIdeationAgent` Call

- **User Story / Goal:** As a Developer, I want to integrate the `PreInitializationIdeationAgent` into the main orchestration flow so that thematic name lists are generated early in the process.
- **Detailed Requirements:**
    - In `main_orchestrator.py`, add logic to instantiate and run the `PreInitializationIdeationAgent` after the theme is known.
    - Retrieve the generated name lists from the agent's output.
    - Store or prepare these lists for subsequent use by `CaseInitializationAgent` and `SuspectGenerationAgent` (e.g., by adding them to an input dictionary or updating `CaseContext`).
- **Acceptance Criteria (ACs):**
    - AC1: Orchestrator successfully calls `PreInitializationIdeationAgent` with the current theme.
    - AC2: Orchestrator correctly extracts the first name list and last name list from the agent's response.
    - AC3: The extracted lists are made available for subsequent agent calls.
- **Dependencies:** Story 6.1.
- **Status:** To Do

---

### Story 6.3: Integrate Generated Names into `CaseInitializationAgent`

- **User Story / Goal:** As a Developer, I want to modify `CaseInitializationAgent` to use the dynamically generated thematic name lists for creating the victim's name.
- **Detailed Requirements:**
    - Update `CaseInitializationAgent` input handling to accept the lists of first names and last names.
    - Modify its internal logic/prompt to select a first name and a last name from these provided lists to form the `VictimProfile.name`.
    - Ensure the agent still outputs a complete `VictimProfile`.
- **Acceptance Criteria (ACs):**
    - AC1: `CaseInitializationAgent` accepts new input parameters for first name and last name lists.
    - AC2: Agent successfully selects one first name and one last name from the provided lists.
    - AC3: The `VictimProfile.name` field in the agent's output is populated using names from these lists.
    - AC4: The chosen name combination is plausible.
- **Dependencies:** Story 6.2.
- **Status:** To Do

---

### Story 6.4: Integrate Generated Names into `SuspectGenerationAgent`

- **User Story / Goal:** As a Developer, I want to modify `SuspectGenerationAgent` to use the dynamically generated thematic name lists for creating suspect names.
- **Detailed Requirements:**
    - Update `SuspectGenerationAgent` input handling to accept the lists of first names and last names.
    - Modify its internal logic/prompt to select unique first and last names from these lists for each suspect's `SuspectProfile.name`.
    - Ensure the agent handles generating multiple unique suspects, avoiding name collisions if possible from the provided lists or having a fallback.
- **Acceptance Criteria (ACs):**
    - AC1: `SuspectGenerationAgent` accepts new input parameters for first name and last name lists.
    - AC2: Agent successfully populates `SuspectProfile.name` for each generated suspect using names from the lists.
    - AC3: Generated suspect names are unique from each other and the victim, where feasible given list sizes.
- **Dependencies:** Story 6.2.
- **Status:** To Do

--- 