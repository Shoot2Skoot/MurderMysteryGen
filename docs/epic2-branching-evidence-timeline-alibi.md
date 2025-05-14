# Epic 2: Timeline & Alibi Construction

**Goal:** To implement the MVP version of the `TimelineOrchestratorAgent` which will construct the detailed, stage-by-stage timeline of events and character movements, ensuring consistency with the narrative defined in Epic 1, the killer's actions, robust alibis for innocents, and the defined temporal ambiguity.

**Deployability:** This epic builds directly on Epic 1. It requires the `BranchingCaseContext` to be populated with core Pydantic models, map data, and initial narrative/timeline settings. It is deployable in that the `TimelineOrchestratorAgent` can be run to populate the timeline aspects of the `BranchingCaseContext`, which can then be validated.

## Epic-Specific Technical Context

- **Input Data:** A `BranchingCaseContext` object that has been processed by the `NarrativeRefinementAgent` (from Epic 1), containing:
    - Populated `timeline.settings` (num_stages, critical_action_window_stages, etc.).
    - Populated `timeline.locations`.
    - Killer designation and `core_murder_action_description`.
- **Core Logic:** The agent will need to make decisions about character locations per stage and what key events occur to support alibis and the killer's narrative.

## Local Testability & Command-Line Access

- **Local Development:**
    - Developers should be able to run a script that takes a `BranchingCaseContext` JSON (output from Epic 1), invokes the `TimelineOrchestratorAgent`, and outputs the updated `BranchingCaseContext` with populated `timeline.events` and `timeline.character_movements`.
- **Command-Line Testing:**
    - A utility script (e.g., `python -m tools.run_timeline_orchestrator --input_case_file path/to/narrative_refined_case.json --output_file path/to/timeline_orchestrated_case.json`) should be provided.
- **Testing Prerequisites:**
    - Valid example `BranchingCaseContext` JSON files (output from a successful Epic 1 run).
    - Python environment with all necessary dependencies.

## Story List

### Story 2.1: Implement `TimelineOrchestratorAgent` (MVP) - Character Movements & Alibis

- **User Story / Goal:** As a developer, I want to implement the core logic of the `TimelineOrchestratorAgent` to plot the killer's path, establish verifiable alibis for 2 non-killers across the `critical_action_window_stages`, and detail all 3 suspects' locations (`CharacterLocationStage`) for each `TimeStage` in the mystery.
- **Detailed Requirements:**
    - Create an agent class/module for `TimelineOrchestratorAgent`.
    - The agent should accept a `BranchingCaseContext` object (output from `NarrativeRefinementAgent`).
    - **Killer's Path:**
        - Determine the killer's location for each stage, ensuring their movements are logical and consistent with the `core_murder_action_description` occurring within the `core_murder_action_stage_window`.
    - **Non-Killer Alibis:**
        - For each of the 2 non-killer suspects:
            - For each `TimeStage` within the `critical_action_window_stages`, assign the suspect to a `Location` that verifiably prevents them from committing the `core_murder_action`.
            - Ensure these alibi locations can be supported by plausible (though not yet explicitly generated as evidence) activity.
    - **Character Movements (`CharacterLocationStage`):**
        - For all 3 suspects, populate the `timeline.character_movements` list by creating a `CharacterLocationStage` object for each suspect for *every* `TimeStage` in the mystery.
        - Movement between stages should be logical given the map layout (`timeline.locations`).
        - `confirmation_source_description` can be minimal or placeholder for MVP (e.g., "Agent determined").
- **Acceptance Criteria (ACs):**
    - AC1: Given a valid input `BranchingCaseContext`, the agent populates `timeline.character_movements` for all suspects for all stages.
    - AC2: The killer's recorded movements are consistent with performing the core murder action within the specified window.
    - AC3: Each non-killer has a sequence of locations during the `critical_action_window_stages` that constitutes a plausible alibi (i.e., they are not at the scene of the crime or have no means/opportunity from their alibi location).
    - AC4: All character movements between consecutive stages are plausible given the map's `connected_location_ids` (e.g., not teleporting across unconnected areas).
    - AC5: The output `BranchingCaseContext` (with added `character_movements`) is valid.
- **Dependencies:** Epic 1 (requires fully populated `BranchingCaseContext` from `NarrativeRefinementAgent`, including map and timeline settings).

---

### Story 2.2: Implement `TimelineOrchestratorAgent` (MVP) - Key Timeline Events

- **User Story / Goal:** As a developer, I want to extend the `TimelineOrchestratorAgent` to generate a few critical `TimelineEvent` objects that directly support established alibis or the killer's necessary actions, adding context to the timeline.
- **Detailed Requirements:**
    - Extend the `TimelineOrchestratorAgent` from Story 2.1.
    - Based on the character movements and alibis defined:
        - Generate 1-2 `TimelineEvent` objects per non-killer that would plausibly occur at their alibi location during a critical stage, providing a reason for them to be there or be witnessed (e.g., "Heard arguing with X in the Kitchen", "Seen reading in the Library").
        - Generate 1-2 `TimelineEvent` objects relevant to the killer's path or actions if necessary (e.g., "Loud thud heard from the Study" when killer is there, or an event that explains their presence in a certain location).
    - Each `TimelineEvent` should be populated with:
        - `event_id` (unique).
        - `stage`.
        - `description`.
        - `location_ids` (where the event occurs or is observed from).
        - `involved_character_names`.
- **Acceptance Criteria (ACs):**
    - AC1: The agent generates at least one `TimelineEvent` supporting each non-killer's alibi during the `critical_action_window_stages`.
    - AC2: Any generated `TimelineEvent` for the killer is consistent with their path and the core murder action.
    - AC3: All generated `TimelineEvent` objects are valid according to the Pydantic model and correctly added to `timeline.events`.
    - AC4: Event details (locations, involved characters, stage) are consistent with `character_movements`.
- **Dependencies:** Story 2.1.

---

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
| Initial Draft | [Current Date] | 0.1 | First draft of Epic 2. | PM Agent | 