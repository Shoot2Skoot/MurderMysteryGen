# Epic 4.5: Player View Output Generation

**Goal:** To generate an additional, simplified output file (e.g., `_player_view.md`) alongside the main JSON. This file will present the core mystery elements in a more narrative, player-friendly format, with suspects and evidence items shuffled to obscure the solution and facilitate unbiased playtesting/review.

**Deployability:** This epic adds a new output artifact (`_player_view.md`) to the existing generation pipeline. The main script now produces both the detailed JSON and this player-focused Markdown file. This enhances the usability of the generated content for review and testing purposes.

## Epic-Specific Technical Context

- **New Module:** `src/mystery_ai/core/player_view_generator.py` created, containing logic for data extraction, shuffling, and Markdown formatting.
- **New Pydantic Models:** `PlayerViewSuspect` and `PlayerViewData` defined in `src/mystery_ai/core/player_view_generator.py` to structure data specifically for the player view.
- **Orchestration Update:** `main_orchestrator.py` now calls `generate_player_view_file` from the new module after the main JSON output is written.
- **Output File:** A new Markdown file (e.g., `mystery_THEME_TIMESTAMP_player_view.md`) is saved in the `generated_mysteries/` directory.

## Local Testability & Command-Line Access

- **Execution:** Run `python -m src.mystery_ai.main --theme "Your Theme"`.
- **Verification:** Check the `generated_mysteries/` folder for both the `.json` file and the new `_player_view.md` file. Review the Markdown file for correct content (theme, victim, shuffled suspect profiles, shuffled evidence descriptions) and exclusion of solution-revealing details.

## Story List

### Story 4.5.1: Define Player View Data Extraction Logic

- **User Story / Goal:** As a Developer, I want to create a function that takes the complete `CaseContext` and extracts only the information relevant for the initial player view, preparing it for formatted output.
- **Detailed Requirements:** Implemented in `player_view_generator.py` with `extract_player_view_data` function and `PlayerViewData`/`PlayerViewSuspect` models.
- **Acceptance Criteria (ACs):**
  - AC1: Function correctly extracts the specified fields from `CaseContext`. **(COMPLETED)**
  - AC2: Sensitive/solution-revealing information (MMOs, killer status, evidence classification) is excluded. **(COMPLETED)**
- **Dependencies:** Epic 4 (specifically the fully populated `CaseContext`).
- **Status:** COMPLETED

---

### Story 4.5.2: Implement Shuffling for Suspects and Evidence

- **User Story / Goal:** As a Developer, I want to ensure that the lists of suspects and evidence items presented in the player view are randomly shuffled.
- **Detailed Requirements:** Implemented within `generate_player_view_file` in `player_view_generator.py` using `random.shuffle()`.
- **Acceptance Criteria (ACs):**
  - AC1: Given the same `CaseContext`, multiple calls to the player view generation process (or inspection of multiple output files from different runs) result in different orderings of suspects. **(COMPLETED)**
  - AC2: Given the same `CaseContext`, multiple calls result in different orderings of evidence items. **(COMPLETED)**
- **Dependencies:** Story 4.5.1.
- **Status:** COMPLETED

---

### Story 4.5.3: Implement Player View Text/Markdown Output

- **User Story / Goal:** As a Developer, I want to format the extracted and shuffled player view data into a human-readable plain text or Markdown file.
- **Detailed Requirements:** Implemented in `player_view_generator.py` with `format_player_view_markdown` and file writing logic in `generate_player_view_file`.
- **Acceptance Criteria (ACs):**
  - AC1: A new `.md` file is created alongside the main JSON output. **(COMPLETED)**
  - AC2: The file contains the specified information in a readable, structured Markdown format. **(COMPLETED)**
  - AC3: Suspects and evidence are presented in a shuffled order in the file. **(COMPLETED)**
- **Dependencies:** Story 4.5.1, Story 4.5.2.
- **Status:** COMPLETED

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
|        |      | 1.0     | Initial draft of Epic 4.5 and stories. | PM Agent |
|        |      | 1.1     | Marked stories 4.5.1, 4.5.2, 4.5.3 COMPLETED after successful implementation and test. | Dev Agent | 