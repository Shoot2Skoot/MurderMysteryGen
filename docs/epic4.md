# Epic 4: Structured Data Output & Orchestration Finalization

**Goal:** Ensure all generated mystery components (victim, suspects with original/modified MMOs, killer, evidence) are correctly aggregated and formatted into a final, well-structured JSON output. Finalize and test the end-to-end agent orchestration for a complete generation run.

**Deployability:** This epic represents the culmination of the MVP's core generation pipeline. It ensures that all data generated in previous epics is correctly assembled into the final `CaseContext` and output in the specified JSON format. The deliverable is a runnable end-to-end script that produces a complete mystery data file, which is the primary output of the MVP.

## Epic-Specific Technical Context

- **Final Pydantic Model (`CaseContext`):** Reviewed and finalized.
- **JSON Serialization:** Implemented using `model_dump_json(indent=2)` and file writing in `main_orchestrator.py`.
- **End-to-End Script:** `src/mystery_ai/main.py` calls `src/mystery_ai/orchestration/main_orchestrator.py` for full pipeline execution.
- **Schema Documentation:** `docs/data-models.md` updated with the generated JSON schema for `CaseContext`.

## Local Testability & Command-Line Access

- **Local Development:** Developers run `python -m src.mystery_ai.main --theme "Your Theme"`.
- **Output:** Script produces a uniquely named JSON file in `generated_mysteries/`.
- **Verification:** JSON output can be manually inspected and programmatically validated against the schema in `data-models.md`.

## Story List

### Story 4.1: Finalize `CaseContext` Pydantic Model & Aggregation Logic

- **User Story / Goal:** As a Developer, I need to ensure the main `CaseContext` Pydantic model accurately reflects all data elements generated throughout the pipeline and that there's clear logic for aggregating all components into this final model.
- **Detailed Requirements:** Implemented and reviewed through Epics 1-3 integration.
- **Acceptance Criteria (ACs):**
  - AC1: The `CaseContext` Pydantic model is complete and accurately represents the full mystery data structure. **(COMPLETED)**
  - AC2: The orchestration logic correctly populates a single `CaseContext` instance. **(COMPLETED)**
  - AC3: All sub-models are correctly nested or referenced. **(COMPLETED)**
- **Dependencies:** Story 1.5, Story 2.3, Story 3.3.
- **Status:** COMPLETED

---

### Story 4.2: Implement JSON Output Generation

- **User Story / Goal:** As a Developer, I want the system to serialize the final `CaseContext` object into a well-formatted JSON string and save it to a file.
- **Detailed Requirements:** Implemented in `main_orchestrator.py`.
- **Acceptance Criteria (ACs):**
  - AC1: A JSON file is created in `generated_mysteries/`. **(COMPLETED)**
  - AC2: The content is a valid JSON representation of `CaseContext`. **(COMPLETED)**
  - AC3: The JSON is well-formatted (indented). **(COMPLETED)**
  - AC4: Filename includes theme and timestamp. **(COMPLETED)**
- **Dependencies:** Story 4.1.
- **Status:** COMPLETED

---

### Story 4.3: Document Output Schema in `data-models.md`

- **User Story / Goal:** As a Developer, I need to document the schema of the output JSON file in `docs/data-models.md`.
- **Detailed Requirements:** `tools/generate_schema.py` created and used to update `data-models.md`.
- **Acceptance Criteria (ACs):**
  - AC1: `docs/data-models.md` contains the `CaseContext` JSON schema. **(COMPLETED)**
  - AC2: The documented schema accurately reflects the `CaseContext` Pydantic model. **(COMPLETED)**
  - AC3: Descriptions for key fields are provided via schema generation. **(COMPLETED)**
- **Dependencies:** Story 4.1.
- **Status:** COMPLETED

---

### Story 4.4: Implement End-to-End Orchestration Script & Testing

- **User Story / Goal:** As a Developer, I want a main script that runs the entire mystery generation pipeline from theme input to JSON file output, allowing for end-to-end testing of the MVP.
- **Detailed Requirements:** `src/mystery_ai/main.py` and `src/mystery_ai/orchestration/main_orchestrator.py` provide this functionality.
- **Acceptance Criteria (ACs):**
  - AC1: A single script (`python -m src.mystery_ai.main`) runs the entire pipeline. **(COMPLETED)**
  - AC2: The script accepts a theme via CLI argument. **(COMPLETED)**
  - AC3: Upon successful execution, a JSON output file is created. **(COMPLETED)**
  - AC4: The script runs without unhandled exceptions for valid inputs. **(COMPLETED)**
  - AC5: Console logs indicate progress through major stages. **(COMPLETED)**
- **Dependencies:** Story 1.6, Story 2.4, Story 3.4, Story 4.2.
- **Status:** COMPLETED

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
|        |      | 0.1     | Initial draft of Epic 4 | PM Agent |
|        |      | 0.2     | Stories 4.1-4.4 completed. MVP generation pipeline is functional. | Dev Agent | 