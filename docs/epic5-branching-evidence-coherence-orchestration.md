# Epic 5: MVP Coherence & Orchestration

**Goal:** To implement the MVP version of the `MasterCoherenceAgent` for simplified validation of the generated mystery, and to orchestrate the full MVP agent pipeline (Epics 1-4) to produce a complete, albeit simply validated, `BranchingCaseContext`.

**Deployability:** This epic is the culmination of the MVP. It requires all previous agents (from Epics 1-4) to be implemented. It is deployable in that the full pipeline can be run, producing a `BranchingCaseContext` that has undergone basic validation for solvability by elimination.

## Epic-Specific Technical Context

- **Input Data:** A `BranchingCaseContext` object that has been fully processed by the `ClueWeavingAgent` (from Epic 4), containing all narrative, timeline, blueprint, and evidence item details.
- **Core Logic (`MasterCoherenceAgent`):**
    - Validate non-killer alibis based on `SUPPORTED` nuggets (i.e., assume fragments for a nugget are found, making the nugget `SUPPORTED`).
    - Verify the killer does not have a provable alibi through `SUPPORTED` nuggets.
    - Ensure no wasted fragments (all contribute to at least one nugget's `established_by_fragment_sets`).
    - Perform basic solvability check: Can the killer be identified by eliminating the other two suspects based *only* on their `SUPPORTED` alibi nuggets?
- **Orchestration:** A top-level script or function will be needed to invoke each agent in sequence: `NarrativeRefinementAgent` -> `TimelineOrchestratorAgent` -> `InformationBlueprintAgent` -> `ClueWeavingAgent` -> `MasterCoherenceAgent`.

## Local Testability & Command-Line Access

- **Local Development:**
    - Developers should be able to run a main script that takes a foundational `BranchingCaseContext` JSON and a map JSON, runs the entire MVP pipeline, and outputs the final, validated (by MVP `MasterCoherenceAgent`) `BranchingCaseContext`.
- **Command-Line Testing:**
    - A utility script (e.g., `python -m tools.run_full_mvp_pipeline --case_file path/to/initial_case.json --map_file path/to/map.json --output_file path/to/final_case.json`) should be provided.
- **Testing Prerequisites:**
    - Valid example JSON files for the foundational `BranchingCaseContext` and map data.
    - All individual agent utility scripts (from Epics 1-4) working correctly.

## Story List

### Story 5.1: Implement `MasterCoherenceAgent` (MVP - Simplified Validation)

- **User Story / Goal:** As a developer, I want to implement the `MasterCoherenceAgent` to perform simplified validation checks on a fully generated `BranchingCaseContext`, ensuring basic solvability by elimination for a 3-suspect mystery.
- **Detailed Requirements:**
    - Create an agent class/module for `MasterCoherenceAgent`.
    - The agent should accept a `BranchingCaseContext` object (output from `ClueWeavingAgent`).
    - **Validation Logic (MVP):**
        - **Assume Fragments Found:** For validation purposes, temporarily update the status of all `InformationNuggets` to `SUPPORTED` if all fragments in *any one* of their `established_by_fragment_sets` are considered "found" (i.e., the fragments exist as defined).
        - **Alibi Validation:** For each non-killer, check if their critical alibi nuggets (flagged `is_elimination_critical`) are now `SUPPORTED`. If so, they are considered to have a verifiable alibi for MVP.
        - **Killer Non-Alibi:** Check that the killer does *not* have a set of `SUPPORTED` nuggets that would constitute a verifiable alibi for the `critical_action_window_stages`.
        - **No Wasted Fragments:** Verify that every `InformationFragment` in `information_fragments` is part of at least one `InformationNugget.established_by_fragment_sets`.
        - **Solvability Check (Basic):** If both non-killers have verifiable alibis (based on `SUPPORTED` critical nuggets) and the killer does not, the mystery is considered solvable by elimination for MVP.
    - The agent should return a validation report (e.g., a dictionary or simple object: `{"is_coherent": True/False, "reason": "Details..."}`).
    - For MVP, the iteration loop based on feedback is out of scope; this agent performs a one-pass check.
- **Acceptance Criteria (ACs):**
    - AC1: Given a valid, fully populated `BranchingCaseContext`, the agent correctly identifies if non-killer alibis are supported by their respective nuggets.
    - AC2: The agent correctly identifies if the killer lacks a supported alibi.
    - AC3: The agent flags scenarios with wasted (unlinked) fragments.
    - AC4: The agent returns a coherent (True/False) validation result based on the MVP solvability logic.
    - AC5: The agent processes without error on a valid `BranchingCaseContext`.
- **Dependencies:** Epic 4.

---

### Story 5.2: Implement MVP Orchestration Pipeline

- **User Story / Goal:** As a developer, I want to create a main orchestration script/function that sequentially invokes all MVP agents (`NarrativeRefinementAgent`, `TimelineOrchestratorAgent`, `InformationBlueprintAgent`, `ClueWeavingAgent`, `MasterCoherenceAgent`) to process an initial `BranchingCaseContext` and map data, producing a final, validated (by MVP standards) `BranchingCaseContext`.
- **Detailed Requirements:**
    - Create a main script or function (e.g., in `tools/run_full_mvp_pipeline.py` or a core orchestration module).
    - The script will:
        1.  Load initial `BranchingCaseContext` from a JSON file.
        2.  Load map data using the function from Story 1.2 and add it to the context.
        3.  Instantiate and run `NarrativeRefinementAgent` (Story 1.3) with the context.
        4.  Instantiate and run `TimelineOrchestratorAgent` (Stories 2.1, 2.2) with the updated context.
        5.  Instantiate and run `InformationBlueprintAgent` (Story 3.1) with the updated context.
        6.  Instantiate and run `ClueWeavingAgent` (Story 4.1) with the updated context.
        7.  Instantiate and run `MasterCoherenceAgent` (Story 5.1) with the updated context.
        8.  Output the final `BranchingCaseContext` (e.g., to a JSON file) and the validation report from `MasterCoherenceAgent`.
    - Implement basic error handling for failures within an agent step.
- **Acceptance Criteria (ACs):**
    - AC1: The orchestration script successfully runs the full pipeline of MVP agents in the correct order.
    - AC2: The script correctly passes the `BranchingCaseContext` object between agents.
    - AC3: The script outputs a final `BranchingCaseContext` JSON file and the validation report.
    - AC4: The script handles and reports errors if an agent fails during processing.
- **Dependencies:** Story 1.2, 1.3, 2.1, 2.2, 3.1, 4.1, 5.1.

---

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
| Initial Draft | [Current Date] | 0.1 | First draft of Epic 5. | PM Agent | 