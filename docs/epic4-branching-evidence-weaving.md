# Epic 4: Evidence Weaving & Presentation

**Goal:** To implement the MVP version of the `ClueWeavingAgent` which will take the abstract information blueprint (fragments and nuggets from Epic 3) and instantiate them as concrete, narrative `BranchingEvidenceItem` objects. This involves crafting the actual textual content of clues and embedding the raw data for fragments.

**Deployability:** This epic builds on Epic 3. It requires a `BranchingCaseContext` with defined `information_nuggets` and partially defined `information_fragments` (containing `fragment_id` and `atomic_fact_derived`). It is deployable in that the `ClueWeavingAgent` can run to populate `evidence_items` and complete the `information_fragments` (adding `raw_data_from_evidence` and `source_evidence_item_id`), making the evidence layer of the `BranchingCaseContext` complete.

## Epic-Specific Technical Context

- **Input Data:** A `BranchingCaseContext` object processed by `InformationBlueprintAgent` (from Epic 3).
- **Core Logic:** The agent will group fragments into logical evidence items, generate the `raw_data_from_evidence` for each fragment (the actual text/observation in the clue), and compose the `full_description` for each evidence item. For MVP, this will focus on simpler concealment types.

## Local Testability & Command-Line Access

- **Local Development:**
    - Developers should be able to run a script that takes a `BranchingCaseContext` JSON (output from Epic 3), invokes the `ClueWeavingAgent`, and outputs the updated `BranchingCaseContext` with populated `evidence_items` and fully defined `information_fragments`.
- **Command-Line Testing:**
    - A utility script (e.g., `python -m tools.run_clue_weaving --input_case_file path/to/blueprinted_case.json --output_file path/to/woven_case.json`) should be provided.
- **Testing Prerequisites:**
    - Valid example `BranchingCaseContext` JSON files (output from a successful Epic 3 run).

## Story List

### Story 4.1: Implement `ClueWeavingAgent` (MVP) - Evidence Item Creation & Fragment Embedding

- **User Story / Goal:** As a developer, I want to implement the `ClueWeavingAgent` to create `BranchingEvidenceItem` objects, generate the `raw_data_from_evidence` for each `InformationFragment` (focusing on `DIRECT_QUOTE` or simple `IMPLIED_BY_CONTEXT`), compose the `full_description` for these items, and link fragments to their source evidence.
- **Detailed Requirements:**
    - Create an agent class/module for `ClueWeavingAgent`.
    - The agent should accept a `BranchingCaseContext` object (output from `InformationBlueprintAgent`).
    - **Create Evidence Items:**
        - Group related `InformationFragments` (e.g., 1-3 fragments per evidence item, or based on logical narrative connection) into `BranchingEvidenceItem` objects.
        - Assign an appropriate `category` (e.g., "Note", "Logbook Entry", "Photo Detail") and a unique `evidence_id` for each item.
    - **Generate Raw Data & Compose Descriptions:**
        - For each `InformationFragment` assigned to an evidence item:
            - Generate its `raw_data_from_evidence` – the actual text, observation, or detail as it would appear. This must logically lead to the fragment's `atomic_fact_derived`.
            - For MVP, primarily use `FragmentConcealmentType.DIRECT_QUOTE` or simple `IMPLIED_BY_CONTEXT`.
        - Craft the `full_description` for each `BranchingEvidenceItem`, skillfully embedding the `raw_data_from_evidence` of its constituent fragments. Generate `discovery_details` (can be simple/placeholder for MVP, e.g., "Found in the study").
    - **Link Fragments & Nuggets:**
        - Update each `InformationFragment` with its `raw_data_from_evidence`, its `source_evidence_item_id` (the ID of the `BranchingEvidenceItem` it's embedded in), and a `fragment_concealment_type`.
        - Populate `BranchingEvidenceItem.contains_nugget_ids` based on the nuggets established by the fragments embedded within it (this provides a quick lookup).
- **Acceptance Criteria (ACs):**
    - AC1: Given a valid input `BranchingCaseContext`, the agent populates the `evidence_items` list.
    - AC2: All `InformationFragment` objects in `information_fragments` are updated with `raw_data_from_evidence`, `source_evidence_item_id`, and `fragment_concealment_type`.
    - AC3: The `raw_data_from_evidence` for each fragment is logically consistent with its `atomic_fact_derived`.
    - AC4: Each `BranchingEvidenceItem.full_description` correctly embeds the raw data of its fragments.
    - AC5: `BranchingEvidenceItem.contains_nugget_ids` is correctly populated.
    - AC6: The output `BranchingCaseContext` is valid.
- **Dependencies:** Epic 3.

---

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
| Initial Draft | [Current Date] | 0.1 | First draft of Epic 4. | PM Agent | 