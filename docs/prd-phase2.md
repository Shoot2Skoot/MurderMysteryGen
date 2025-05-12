# Mystery.AI - Product Requirements Document (PRD) - Phase 2

## Intro

This document outlines the product requirements for Phase 2 of "Mystery.AI," titled "Enhanced Foundational Diversity & Richer Individual Evidence." Building upon the successful MVP (Epics 1-4), this phase aims to significantly improve the variety and narrative richness of generated mysteries. It focuses on two main thrusts: 
1. Implementing 'forced diversity' for core victim/suspect attributes using curated and dynamically generated lists, moving away from reliance on model tuning or generic prompting for variety.
2. Enhancing the strategic value and narrative function of individual evidence items, making them more varied and nuanced as a precursor to more complex evidence structures in future phases.

This PRD is informed by `docs/project-brief-phase2.md`.

## Goals and Context (Phase 2)

- **Project Objectives (Phase 2):**
    - To integrate mechanisms for selecting core victim/suspect attributes (Cause of Death, Motive Category, Occupation Archetype, Personality Archetype) from predefined master lists, ensuring thematic integration.
    - To develop a new agent capable of dynamically generating thematically appropriate lists of First Names and Last Names for use in victim and suspect profiling.
    - To enhance the `EvidenceGenerationAgent` and `EvidenceItem` data model to support a wider variety of evidence types (categories) and to articulate the narrative function (e.g., subtlety, directness) of each piece of evidence.
    - To update the overall system orchestration and core data models (`CaseContext`, `VictimProfile`, `SuspectProfile`, `EvidenceItem`) to seamlessly incorporate these new diversity and evidence richness features.

- **Measurable Outcomes (Phase 2):**
    - Successful incorporation of list-selected attributes into >90% of generated victim/suspect profiles while maintaining thematic coherence.
    - Generation of thematically relevant name lists by the `PreInitializationIdeationAgent` with >80% of items deemed plausible by human review across at least 3 diverse themes.
    - `EvidenceItem` instances consistently include `evidence_category` and `narrative_function_description` in >90% of generated evidence.
    - Qualitative assessment by the primary user indicates a notable increase in the variety of core victim/suspect attributes, names, and the descriptive richness of individual evidence items when comparing Phase 2 outputs to MVP outputs using identical themes.

- **Success Criteria (Phase 2):**
    - All four primary goals of Phase 2 (Static List Integration, Dynamic Name Generation, System Orchestration Updates for Diversity, Advanced Individual Evidence Generation) are implemented and demonstrable.
    - The system generates mysteries that are perceivably more varied in their foundational elements and evidence descriptions than the MVP.
    - Data models are cleanly extended, and orchestration logic remains robust and understandable.

- **Key Performance Indicators (KPIs) (Phase 2):**
    - **Attribute Integration Rate:** Percentage of victim/suspect profiles correctly using attributes selected from the provided lists.
    - **Thematic Name Plausibility Score (Manual):** Average rating (1-5) by primary user for thematic appropriateness of generated name lists.
    - **Evidence Richness Completion Rate:** Percentage of `EvidenceItem` objects that include the new `evidence_category` and `narrative_function_description` fields.
    - **Perceived Variety Improvement (Qualitative):** User assessment of increased diversity in outputs.

## Scope and Requirements (Phase 2)

### Functional Requirements (High-Level)

- **FR1: Static List Integration for Victim/Suspect Attributes:**
    - System must allow for definition and storage of master lists as JSON files in `MurderMysteryGen/config/master_lists/` for: Cause of Death, Motive Categories, Generic Occupation Archetypes, Personality Archetypes.
    - Orchestrator must be able to randomly select a subset (e.g., 2-3 items) from each master list to provide as input to relevant agents.
    - `CaseInitializationAgent` (and potentially `SuspectGenerationAgent`) must be modified to:
        - Accept these lists of attribute options.
        - Select one option from each list.
        - Thematically integrate the selected attributes into the `VictimProfile` (and `SuspectProfile` if applicable).
- **FR2: Dynamic Thematic List Generation for Names:**
    - A new `PreInitializationIdeationAgent` must be created.
        - Input: Theme string.
        - Task: Generate lists of N (e.g., 50) thematically appropriate First Names and N (e.g., 50) Last Names.
        - Output: Structured lists of names (e.g., `List[str]`).
    - This agent must be integrated into the orchestration flow before victim/suspect generation agents are called.
    - `CaseInitializationAgent` (and `SuspectGenerationAgent`) must be modified to accept and utilize these generated name lists for populating victim and suspect names.
- **FR3: Advanced Individual Evidence Generation:**
    - System must allow for definition and storage of a master list of Evidence Categories/Types as a JSON file in `MurderMysteryGen/config/master_lists/` (e.g., "Personal Correspondence," "Official Document," "Physical Object," "Witness Snippet").
    - `EvidenceGenerationAgent` must be modified to:
        - Accept a sub-list of Evidence Categories as input.
        - Select an appropriate category for the evidence being generated.
        - Generate a `narrative_function_description` text field explaining the intended subtlety, directness, or role of the evidence item within the narrative (e.g., "Directly implicates if fact X is known," "Misleading unless detail Y is noticed").
    - Orchestrator must provide the sub-list of Evidence Categories to the `EvidenceGenerationAgent`.
- **FR4: System & Data Model Updates for Phase 2 Features:**
    - `VictimProfile` and `SuspectProfile` Pydantic models must be updated (if necessary) to store the explicitly selected attributes (e.g., chosen motive category, chosen occupation).
    - `EvidenceItem` Pydantic model must be extended to include `evidence_category: str` and `narrative_function_description: str`.
    - `CaseContext` may require updates if new intermediate data (e.g., generated name lists, selected attribute sub-lists) needs to be passed between agents via the context.
    - The main orchestration script (`main_orchestrator.py`) must be updated to manage the new agent calls, data transformations, and data flow for all Phase 2 features.

### Non-Functional Requirements (NFRs) - Phase 2

- **Performance:** Introduction of new agents/list processing should not excessively degrade overall generation time compared to MVP (e.g., aim for <10-15% increase per new feature set if possible).
- **Maintainability:**
    - Master lists for attributes and evidence categories should be easily updatable, stored as JSON files in `MurderMysteryGen/config/master_lists/`.
    - New agent logic should be modular and well-documented.
- **Usability (Developer):** Clear logging for new selection processes and agent activities.
- **Reliability:** New features should maintain or improve the overall reliability of the generation process.

### User Experience (UX) Requirements (Developer - Primary User)

- **Configuration:** Developer should be able_to easily view and modify the master lists for attributes and evidence categories.
- **Output Inspection:** The impact of new diversity features should be clearly observable in the final JSON output (e.g., presence of selected occupation, evidence category in items).

### Integration Requirements

- All new agents and logic must integrate seamlessly with the existing OpenAI Agents SDK-based framework.
- Data model changes must remain compatible with Pydantic and the SDK's structured output mechanisms.

### Testing Requirements (Phase 2)

- **Manual Review:** For verifying thematic coherence of integrated attributes, plausibility of generated names, and appropriateness of evidence categories/narrative functions.
- **Unit Tests:** For any new helper functions (e.g., list selection logic, data transformation utilities).
- **Integration Tests:** For verifying the correct data flow through the modified orchestration chain, especially the passing of lists and selected items to/from agents.
- **Schema Validation:** Ensure updated JSON output validates against the modified `CaseContext` schema.

## Epic Overview (Phase 2)

- **Epic 5: Static List Integration for Core Attributes**
    - **Goal:** Implement the selection of Cause of Death, Motive Category, Occupation Archetype, and Personality Archetype from predefined lists and their thematic integration into victim/suspect profiles.
- **Epic 6: Dynamic Thematic Name Generation**
    - **Goal:** Develop the `PreInitializationIdeationAgent` to generate theme-specific first and last names and integrate their usage.
- **Epic 7: Advanced Individual Evidence Crafting**
    - **Goal:** Enhance `EvidenceGenerationAgent` and the `EvidenceItem` model to include Evidence Categories and Narrative Function Descriptions.
- **Epic 8: System Orchestration & Data Model Finalization for Phase 2**
    - **Goal:** Ensure all Phase 2 features are correctly orchestrated, data models are updated, and the system functions cohesively.

## Key Reference Documents

- `docs/project-brief-phase2.md`
- `docs/data-models.md` (to be updated for Phase 2 changes)
- `docs/architecture.md` (general architecture remains, agent roles expand)
- `docs/epic5.md` (To be created)
- `docs/epic6.md` (To be created)
- `docs/epic7.md` (To be created)
- `docs/epic8.md` (To be created)

## Post-Phase 2 / Future Enhancements

- **Branching Evidence Architecture & Design (Phase 3):** The immediate next step, as outlined in `docs/project-brief-phase3.md`.
- Deep Narrative & Storytelling elements.
- Sophisticated Coherence & Logic Checking agents.
- (Other items from original PRD's Post-MVP list)

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
|        |      | 2.0     | Initial PRD draft for Phase 2 | PM Agent |

## Initial Architect Prompt (Phase 2 Focus)

This section provides a summary of technical considerations for the Architect related to Phase 2 enhancements. The core architecture (Python, OpenAI Agents SDK) remains, but new agents and data handling for lists are introduced, and existing models/agents are modified.

### Technical Infrastructure Considerations:

- **Master List Management:** Master lists will be stored as JSON configuration files in `MurderMysteryGen/config/master_lists/`. This allows for ease of update by the developer.
- **Data Model Extensions:** Review proposed changes to `VictimProfile`, `SuspectProfile`, and `EvidenceItem` in `core/data_models.py`. Ensure they are efficient and align with Pydantic best practices and SDK compatibility.
    - `EvidenceItem` will add `evidence_category: str` and `narrative_function_description: str`.
    - `VictimProfile` (and potentially `SuspectProfile`) might need fields to store the *chosen* attribute if this needs to be explicitly tracked beyond its integration into descriptive fields (e.g., `chosen_motive_category: str`).
- **New Agent (`PreInitializationIdeationAgent`):** Design considerations for its inputs (theme), outputs (structured name lists), and instructions to ensure thematic relevance and list diversity.
- **Modifications to Existing Agents:**
    - `CaseInitializationAgent`: Will need to accept lists of attribute options, select one, and integrate it. Will also use generated name lists.
    - `SuspectGenerationAgent` (Potentially): May also need to integrate selected attributes if these are determined at the suspect level rather than just victim.
    - `EvidenceGenerationAgent`: Will need to accept a sub-list of Evidence Categories, select one, and also generate the new `narrative_function_description` field.
- **Orchestration Logic (`main_orchestrator.py`):** Detail the updated flow:
    1. Call `PreInitializationIdeationAgent` (for names).
    2. Prepare sub-lists of attribute options from master lists.
    3. Call `CaseInitializationAgent` with theme, name lists, and attribute option sub-lists.
    4. (Suspect generation continues, potentially using attribute sub-lists and name lists).
    5. Prepare sub-lists of Evidence Categories.
    6. Call `EvidenceGenerationAgent` with context including Evidence Category sub-lists.
- **Configuration:** How will the number of items selected from master lists (e.g., 2-3 options) or the number of names generated (e.g., 50) be configured if not hardcoded?

### Testing Considerations:

- Ensure new Pydantic model fields are covered by schema validation.
- Consider how to test the "thematic integration" aspect of list-selected items (likely manual review, but agent prompts should emphasize this).
- Logging for list selection and agent choices will be important for debugging.

This phase focuses on enriching the inputs and outputs of existing agent structures to achieve diversity, rather than fundamentally altering the core pipeline logic of MMO generation itself. The main architectural challenge is the clean integration of these new data sources and choices into the existing flow. 