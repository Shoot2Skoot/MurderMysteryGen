# Epic 4: Structured Data Output & Orchestration Finalization

**Goal:** Ensure all generated mystery components (victim, suspects with original/modified MMOs, killer, evidence) are correctly aggregated and formatted into a final, well-structured JSON output. Finalize and test the end-to-end agent orchestration for a complete generation run.

**Deployability:** This epic represents the culmination of the MVP's core generation pipeline. It ensures that all data generated in previous epics is correctly assembled into the final `CaseContext` and output in the specified JSON format. The deliverable is a runnable end-to-end script that produces a complete mystery data file, which is the primary output of the MVP.

## Epic-Specific Technical Context

- **Final Pydantic Model (`CaseContext`):** Ensure the `CaseContext` Pydantic model fully encompasses all data elements: theme, victim profile, list of suspects (each with profile, original MMO, killer status, modified MMO if applicable), and list of evidence items.
- **JSON Serialization:** Implement logic to serialize the final `CaseContext` object into a well-formatted JSON string and write it to a file.
- **End-to-End Script:** Develop a main script that orchestrates the execution of all agent sequences from Epic 1 through Epic 3, and finally performs the data aggregation and JSON output.
- **Schema Documentation:** Formally document the schema of the output JSON (likely derived from Pydantic models) in `docs/data-models.md`.

## Local Testability & Command-Line Access

- **Local Development:** Developers can run the main end-to-end script.
- **Command-Line Testing:** The main script should accept the initial theme as a CLI argument (e.g., `python run_mystery_generation.py --theme "Sci-Fi Space Station"`).
- **Output:** The script will produce a uniquely named JSON file (e.g., based on theme and timestamp) containing the full mystery data.
- **Verification:** The JSON output can be manually inspected for completeness and correctness against the Pydantic models and also programmatically validated against a JSON schema.

## Story List

### Story 4.1: Finalize `CaseContext` Pydantic Model & Aggregation Logic

- **User Story / Goal:** As a Developer, I need to ensure the main `CaseContext` Pydantic model accurately reflects all data elements generated throughout the pipeline and that there's clear logic for aggregating all components into this final model.
- **Detailed Requirements:** Implemented and reviewed.
- **Acceptance Criteria (ACs):**
  - AC1: The `CaseContext` Pydantic model is complete and accurately represents the full mystery data structure. **(COMPLETED)**
  - AC2: The orchestration logic correctly populates a single `CaseContext` instance with all generated data from previous steps. **(COMPLETED)**
  - AC3: All sub-models (`VictimProfile`, `Suspect`, `MMO`, `EvidenceItem`) are correctly nested or referenced within `CaseContext`. **(COMPLETED)**
- **Dependencies:** Story 1.5, Story 2.3, Story 3.3.
- **Status:** COMPLETED

---

### Story 4.2: Implement JSON Output Generation

- **User Story / Goal:** As a Developer, I want the system to serialize the final `CaseContext` object into a well-formatted JSON string and save it to a file, so that the generated mystery can be easily reviewed and used.
- **Detailed Requirements:** Implemented in `main_orchestrator.py`.
- **Acceptance Criteria (ACs):**
  - AC1: A JSON file is created upon successful completion of a generation run. **(COMPLETED)**
  - AC2: The content of the JSON file is a valid JSON representation of the `CaseContext` object. **(COMPLETED)**
  - AC3: The JSON is well-formatted (indented) for human readability. **(COMPLETED)**
  - AC4: Filename includes theme (sanitized) and a timestamp or unique ID. **(COMPLETED)**
- **Dependencies:** Story 4.1.
- **Status:** COMPLETED

---

### Story 4.3: Document Output Schema in `data-models.md`

- **User Story / Goal:** As a Developer, I need to document the schema of the output JSON file in `docs/data-models.md`, so that users and other systems understand the data structure.
- **Detailed Requirements:**
  - Create/update `docs/data-models.md`.
  - Include a section for the `CaseContext` JSON schema.
  - This can be generated programmatically from the Pydantic models (e.g., using `CaseContext.model_json_schema()`) and then formatted for readability in the markdown file.
  - Clearly describe each field, its type, and its purpose.
- **Acceptance Criteria (ACs):**
  - AC1: `docs/data-models.md` is created and contains a section for the output JSON schema.
  - AC2: The documented schema accurately reflects the structure of the `CaseContext` Pydantic model.
  - AC3: Descriptions for key fields are provided.
- **Dependencies:** Story 4.1.

---

### Story 4.4: Implement End-to-End Orchestration Script & Testing

- **User Story / Goal:** As a Developer, I want a main script that runs the entire mystery generation pipeline from theme input to JSON file output, allowing for end-to-end testing of the MVP.
- **Detailed Requirements:**
  - Create/finalize a main Python script (e.g., `run_mystery_generation.py`) that serves as the primary entry point.
  - This script should orchestrate the calls to:
    1.  `CaseInitializationAgent` (Epic 1)
    2.  `SuspectGenerationAgent` & `MMOGenerationAgent` (Epic 2)
    3.  `KillerSelectionAgent`, `MMOModificationAgent`, `EvidenceGenerationAgent` (Epic 3)
    4.  Final `CaseContext` aggregation and JSON output logic (Story 4.1, 4.2).
  - The script must accept a `--theme` CLI argument.
  - Implement basic logging throughout the script to indicate major stages and any critical errors.
- **Acceptance Criteria (ACs):**
  - AC1: A single script can be executed to run the entire generation pipeline.
  - AC2: The script accepts a theme via CLI argument.
  - AC3: Upon successful execution, a JSON output file is created as per Story 4.2.
  - AC4: The script runs without unhandled exceptions for valid inputs and successful LLM calls.
  - AC5: Basic console logs indicate the progress through the main stages of generation.
- **Dependencies:** Story 1.6, Story 2.4, Story 3.4, Story 4.2.

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
|        |      | 0.1     | Initial draft of Epic 4 | PM Agent | 