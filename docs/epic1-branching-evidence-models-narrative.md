# Epic 1: Core Data Models & Narrative Foundation

**Goal:** To establish the foundational data structures (Pydantic models) for the Branching Evidence System, implement the capability to ingest pre-defined map data, and create the MVP version of the `NarrativeRefinementAgent` to initialize the narrative and timeline parameters for a mystery.

**Deployability:** This epic is the first step and establishes the core data schema and initial narrative context. It is independently deployable in the sense that the data models can be validated and the `NarrativeRefinementAgent` can produce its defined output. All subsequent epics will build upon the `BranchingCaseContext` structure and initial narrative parameters established here.

## Epic-Specific Technical Context

- **Project Scaffolding:** Assumes the existing Mystery.AI Python project structure.
- **Pydantic Models:** All models defined in `docs/branching-evidence-design.md` (Section 2.2) need to be implemented in Python files (e.g., within `src/mystery_ai/core/data_models_branching.py` or a similar appropriate location).
- **Input Data:**
    - A foundational `BranchingCaseContext` JSON object (structure to be compatible with the new models, likely a simplified version from a preceding system, focusing on `theme`, `victim`, and `suspects` with basic MMOs for 3 suspects, and a designated killer).
    - A map JSON file (e.g., `maps/Villa.json`) containing location data.

## Local Testability & Command-Line Access

- **Local Development:**
    - Developers should be able to run a script that takes a path to a foundational `BranchingCaseContext` JSON and a map JSON file, invokes the `NarrativeRefinementAgent` (once developed in Story 1.3), and outputs the updated `BranchingCaseContext` (e.g., to console or a new JSON file).
- **Command-Line Testing:**
    - A utility script (e.g., `python -m tools.run_narrative_refinement --case_file path/to/case.json --map_file path/to/map.json --output_file path/to/output_case.json`) should be provided.
- **Testing Prerequisites:**
    - Valid example JSON files for the foundational `BranchingCaseContext` and map data.
    - Python environment with all necessary dependencies (Pydantic, etc.).

## Story List

### Story 1.1: Implement Core Pydantic Data Models

- **User Story / Goal:** As a developer, I want to implement all Pydantic data models as defined in `docs/branching-evidence-design.md` Section 2.2, so that the Branching Evidence System has a strongly-typed and validated data structure for all its components.
- **Detailed Requirements:**
    - Create/update Python files (e.g., `src/mystery_ai/core/data_models_branching.py`) to include all Pydantic models:
        - `MMOElementType` (Enum)
        - `VictimProfile` (ensure compatibility if existing, or define as placeholder if purely for branching context)
        - `Suspect` (ensure compatibility if existing, or define as placeholder)
        - `TimelineSettings`
        - `Location`
        - `TimelineEvent`
        - `CharacterLocationStage`
        - `MysteryTimeline`
        - `BranchingCaseContext`
        - `FragmentConcealmentType` (Enum)
        - `NuggetStatus` (Enum)
        - `CorroborationCondition`
        - `InformationFragment`
        - `InformationNugget`
        - `BranchingEvidenceItem`
    - Ensure all fields, types, descriptions, and default values match the design document.
    - Include `model_config = {"extra": "ignore"}` where appropriate, especially for `BranchingCaseContext`.
- **Acceptance Criteria (ACs):**
    - AC1: All Pydantic models from Section 2.2 of `docs/branching-evidence-design.md` are implemented in Python code.
    - AC2: The models correctly serialize to and deserialize from JSON that matches the defined structure.
    - AC3: Attempting to create model instances with invalid data types raises Pydantic validation errors.
    - AC4: Default values are correctly applied when optional fields are omitted during instantiation.
- **Dependencies:** None.

---

### Story 1.2: Implement Map Data Ingestion

- **User Story / Goal:** As a developer, I want to create a mechanism to load location data from a pre-defined JSON file (e.g., `maps/Villa.json`) and populate the `BranchingCaseContext.timeline.locations` list with `Location` model instances, so that the system can use a structured representation of the mystery setting.
- **Detailed Requirements:**
    - Create a utility function or method that accepts a file path to a map JSON file.
    - The function should read the JSON file, parse its content (assuming a list of location objects or a structure that can be mapped to it).
    - For each location entry in the JSON, instantiate a `Location` Pydantic model.
    - Ensure the JSON structure for the map file is defined and documented (e.g., a list of dictionaries, where each dictionary has keys corresponding to `Location` model fields like `location_id`, `name`, `description`, `connected_location_ids`, etc.).
    - The function should return a list of `Location` model instances.
- **Acceptance Criteria (ACs):**
    - AC1: A function successfully reads a compliant map JSON file (e.g., a test `Villa.json`).
    - AC2: The function returns a list of `Location` Pydantic model instances, correctly populated from the JSON data.
    - AC3: The function raises an appropriate error if the map file is not found or is malformed.
    - AC4: The `BranchingCaseContext` can be updated with the list of `Location` objects returned by this function.
- **Dependencies:** Story 1.1 (requires `Location` and `BranchingCaseContext` models).

---

### Story 1.3: Implement `NarrativeRefinementAgent` (MVP)

- **User Story / Goal:** As a developer, I want to implement the MVP version of the `NarrativeRefinementAgent` that takes a foundational `BranchingCaseContext` (with 3 suspects) and map data, then defines and populates the core murder action details and timeline settings (`temporal_ambiguity_source`, `num_stages`, etc.), so that the mystery has a basic narrative framework for subsequent agents to build upon.
- **Detailed Requirements:**
    - Create an agent class/module for `NarrativeRefinementAgent`.
    - The agent should accept an initial `BranchingCaseContext` object (populated with theme, victim, 3 suspects with basic MMOs and a designated killer) and a list of `Location` objects (from Story 1.2).
    - The agent logic should:
        - Define the `core_murder_action_description` (e.g., a placeholder or simple LLM call based on killer MMO).
        - Define the `core_murder_action_stage_window` (e.g., a fixed window like `[2, 3]`).
        - Define `timeline.settings.temporal_ambiguity_source` (e.g., a placeholder or simple LLM call).
        - Define `timeline.settings.num_stages` (e.g., a fixed number like 4 or 5).
        - Define `timeline.settings.stage_duration_description` (e.g., "Approx. 30 minutes").
        - Define `timeline.settings.critical_action_window_stages` (derived from `core_murder_action_stage_window`).
        - For MVP, minimal or no actual refinement of suspect MMO descriptions is required; focus is on populating the timeline and murder action fields.
    - The agent should return the updated `BranchingCaseContext` object.
- **Acceptance Criteria (ACs):**
    - AC1: Given a valid initial `BranchingCaseContext` and map locations, the agent successfully populates `core_murder_action_description`, `core_murder_action_stage_window` in the `BranchingCaseContext`.
    - AC2: The agent successfully populates `timeline.settings` with `temporal_ambiguity_source`, `num_stages`, `stage_duration_description`, and `critical_action_window_stages`.
    - AC3: The output `BranchingCaseContext` is valid according to the Pydantic model.
    - AC4: Agent handles missing expected inputs gracefully (e.g., if killer not designated in input suspects list).
- **Dependencies:** Story 1.1, Story 1.2.

---

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
| Initial Draft | [Current Date] | 0.1 | First draft of Epic 1. | PM Agent | 