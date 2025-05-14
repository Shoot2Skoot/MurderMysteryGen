# Epic 3: Evidence Blueprinting (Basic)

**Goal:** To implement the MVP version of the `InformationBlueprintAgent` which will translate the narrative and timeline (from Epics 1 & 2) into a logical blueprint of information. This involves designing essential `InformationNugget` objects (for alibis and killer path support) and defining the `InformationFragment` objects that establish these nuggets (basic establishment logic, deferring complex corroboration).

**Deployability:** This epic builds on Epics 1 and 2. It requires a `BranchingCaseContext` populated with narrative settings, map data, character movements, and timeline events. It is deployable in that the `InformationBlueprintAgent` can run to populate the `information_nuggets` and `information_fragments` (with `atomic_fact_derived`) in the `BranchingCaseContext`, which can then be validated.

## Epic-Specific Technical Context

- **Input Data:** A `BranchingCaseContext` object processed by `TimelineOrchestratorAgent` (from Epic 2).
- **Core Logic:** The agent will analyze the timeline, alibis, and killer's path to determine what facts (nuggets) need to be discoverable and what atomic pieces of information (fragments) will prove them for the MVP.
- **Simplification:** For MVP, `CorroborationCondition` structures will be present in the models but not actively used by this agent to define complex corroboration paths. Nugget status will primarily move from `UNKNOWN` to `SUPPORTED` based on `established_by_fragment_sets`.

## Local Testability & Command-Line Access

- **Local Development:**
    - Developers should be able to run a script that takes a `BranchingCaseContext` JSON (output from Epic 2), invokes the `InformationBlueprintAgent`, and outputs the updated `BranchingCaseContext` with populated `information_nuggets` and `information_fragments`.
- **Command-Line Testing:**
    - A utility script (e.g., `python -m tools.run_information_blueprint --input_case_file path/to/timeline_orchestrated_case.json --output_file path/to/blueprinted_case.json`) should be provided.
- **Testing Prerequisites:**
    - Valid example `BranchingCaseContext` JSON files (output from a successful Epic 2 run).

## Story List

### Story 3.1: Implement `InformationBlueprintAgent` (MVP) - Nugget & Fragment Definition

- **User Story / Goal:** As a developer, I want to implement the `InformationBlueprintAgent` to identify essential `InformationNugget` objects (for alibis of 2 non-killers and subtle support of the killer's path) and define the 1-2 `InformationFragment` objects (with their `atomic_fact_derived`) required to establish each of these nuggets for a 3-suspect mystery.
- **Detailed Requirements:**
    - Create an agent class/module for `InformationBlueprintAgent`.
    - The agent should accept a `BranchingCaseContext` object (output from `TimelineOrchestratorAgent`).
    - **Identify Critical Nuggets:**
        - For each of the 2 non-killers: Analyze their alibi (`CharacterLocationStage` and supporting `TimelineEvents` during `critical_action_window_stages`). Define `InformationNugget` objects essential to prove their alibi for these critical stages (e.g., "Suspect A was in Location X during Stage Y").
        - For the killer: Review their path. Define 1-2 subtle `InformationNugget` objects consistent with their actions but not direct giveaways (e.g., "A specific item was observed in Location Z where killer was").
    - **Design Fragments & Establishment Logic:**
        - For each defined `InformationNugget`:
            - Determine 1-2 `InformationFragment` objects whose `atomic_fact_derived` values, when combined, will establish that nugget.
            - Populate `InformationNugget.description` (the statement of fact).
            - Populate `InformationNugget.established_by_fragment_sets` with the list(s) of `fragment_id`s required (for MVP, likely one list per nugget, containing 1-2 fragment IDs).
            - Assign unique `nugget_id` and `fragment_id` values.
    - **Flag Importance & Status:**
        - Set `InformationNugget.is_elimination_critical = True` for nuggets crucial to a non-killer's alibi.
        - Initialize `InformationNugget.status = NuggetStatus.UNKNOWN` for all nuggets.
        - For MVP, `conditions_for_corroboration` list can be empty or minimally populated but not used for status changes.
    - `information_fragments` will have `fragment_id` and `atomic_fact_derived` populated. `raw_data_from_evidence` and `source_evidence_item_id` will be populated by `ClueWeavingAgent` (Epic 4).
- **Acceptance Criteria (ACs):**
    - AC1: Given a valid input `BranchingCaseContext`, the agent populates `information_nuggets` and `information_fragments` lists.
    - AC2: Each non-killer has at least one `is_elimination_critical = True` nugget associated with their alibi for each stage in the `critical_action_window_stages`.
    - AC3: Each `InformationNugget` has its `established_by_fragment_sets` populated with relevant `fragment_id`s.
    - AC4: Each `InformationFragment` has its `atomic_fact_derived` defined.
    - AC5: All nugget statuses are initialized to `UNKNOWN`.
    - AC6: The output `BranchingCaseContext` is valid.
- **Dependencies:** Epic 2.

---

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
| Initial Draft | [Current Date] | 0.1 | First draft of Epic 3. | PM Agent | 