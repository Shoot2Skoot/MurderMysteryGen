# Epic 4.5: Player View Output Generation

**Goal:** To generate an additional, simplified output file (e.g., `_player_view.md`) alongside the main JSON. This file will present the core mystery elements in a more narrative, player-friendly format, with suspects and evidence items shuffled to obscure the solution and facilitate unbiased playtesting/review.

**Rationale:**
-   Provides a direct way to evaluate the "playability" and coherence of the generated mystery from an investigator's perspective.
-   Helps assess the strength and clarity of evidence and red herrings without the "author's view" of the full data structure.
-   Facilitates sharing the mystery with others for playtesting without revealing the solution.

**Deployability:** This epic adds a new output artifact. After completion, running the main generation script will produce both the detailed JSON and the player-facing Markdown file. This enhances the utility of the MVP for review and testing.

## Epic-Specific Technical Context

- **New Module:** `src/mystery_ai/core/player_view_generator.py` will be created to house the logic for this feature.
- **New Pydantic Model:** A `PlayerViewData` model (or similar) will be defined in `src/mystery_ai/core/data_models.py` to hold the subset of information for the player view.
- **Orchestration:** `main_orchestrator.py` will be updated to call the new player view generation function after the main JSON output is successfully written.
- **Output Format:** Markdown (`.md`) is preferred for readability and simple formatting.

## Local Testability & Command-Line Access

- **Execution:** The existing main script (`python -m src.mystery_ai.main --theme "Your Theme"`) will trigger this new functionality automatically at the end of a successful run.
- **Output:** A new Markdown file (e.g., `mystery_Your_Theme_timestamp_player_view.md`) will appear in the `generated_mysteries/` directory alongside the JSON file.
- **Verification:** Manually inspect the Markdown file to ensure:
    -   Only player-safe information is present (no MMOs, killer identity, evidence type/connections).
    -   Suspects are listed in a random order.
    -   Evidence descriptions are listed in a random order.
    -   The formatting is clear and readable.

## Story List

### Story 4.5.1: Define Player View Data Extraction Logic

- **User Story / Goal:** As a Developer, I want to create a function that takes the complete `CaseContext` and extracts only the information relevant for the initial player view, preparing it for formatted output.
- **Detailed Requirements:**
  - Function takes a `CaseContext` object.
  - Extracts:
    - Theme
    - Victim: Name, Occupation, Personality, Cause of Death
    - For each Suspect: Name, Description, Relationship to Victim (NO MMOs, NO `is_killer` flag)
    - For each Evidence Item: Description (NO `is_red_herring`, NO `points_to_mmo_element`, NO `connection_explanation` initially)
  - The function should return these extracted elements, ideally as a new Pydantic model (e.g., `PlayerViewData`).
- **Acceptance Criteria (ACs):**
  - AC1: `PlayerViewData` Pydantic model is defined in `core/data_models.py`.
  - AC2: Extraction function correctly populates `PlayerViewData` from `CaseContext`.
  - AC3: Sensitive/solution-revealing information is excluded from `PlayerViewData`.
- **Dependencies:** Epic 4 (specifically the final `CaseContext` structure).

---

### Story 4.5.2: Implement Shuffling for Suspects and Evidence in Player View Data

- **User Story / Goal:** As a Developer, I want the lists of suspects and evidence items within the `PlayerViewData` to be randomly shuffled before formatting.
- **Detailed Requirements:**
  - The function responsible for preparing `PlayerViewData` (or a subsequent function) should randomly shuffle the list of extracted suspect details.
  - The list of extracted evidence item descriptions should also be randomly shuffled.
  - Use Python's `random.shuffle()`.
- **Acceptance Criteria (ACs):**
  - AC1: The list of suspects in the prepared `PlayerViewData` object is in a random order compared to `CaseContext.suspects`.
  - AC2: The list of evidence descriptions in the prepared `PlayerViewData` object is in a random order compared to `CaseContext.evidence_items`.
- **Dependencies:** Story 4.5.1.

---

### Story 4.5.3: Implement Player View Text/Markdown Output File Generation

- **User Story / Goal:** As a Developer, I want to format the extracted and shuffled player view data into a human-readable Markdown file.
- **Detailed Requirements:**
  - Create a function that takes the prepared and shuffled `PlayerViewData` object.
  - Formats this data into a clear Markdown string with appropriate headings and lists (as per the example layout discussed previously).
  - The output string is written to a new file in the `generated_mysteries/` directory.
  - Filename should be `mystery_<theme>_<timestamp>_player_view.md`.
  - This function will be called by `main_orchestrator.py`.
- **Acceptance Criteria (ACs):**
  - AC1: A new `.md` file is created in `generated_mysteries/` with the correct naming convention.
  - AC2: The file content correctly represents the (shuffled) player view data in a readable Markdown format.
  - AC3: Orchestrator calls the player view generation successfully at the end of the pipeline.
- **Dependencies:** Story 4.5.1, Story 4.5.2.

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
|        |      | 0.1     | Initial draft of Epic 4.5 and its stories. | PM Agent | 