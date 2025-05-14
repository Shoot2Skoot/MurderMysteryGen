# Mystery.AI: Branching Evidence System Product Requirements Document (PRD)

## Intro

This document outlines the product requirements for the Minimum Viable Product (MVP) of the Branching Evidence System for Mystery.AI. This system aims to enhance the existing mystery generation capabilities by creating a more complex, interconnected web of evidence. The goal is to enable an elimination-focused mystery game where players must synthesize information from multiple sources to identify the killer. This PRD is based on the detailed "Branching Evidence Architecture & Design Document" (`docs/branching-evidence-design.md`).

The MVP will focus on implementing the core agent pipeline (Narrative Refinement, Timeline Orchestration, Information Blueprint, Clue Weaving, and a simplified Master Coherence Agent) to generate a solvable mystery with 3 suspects, utilizing pre-defined map data and making all evidence available upfront.

## Goals and Context

- **Project Objectives:**
    - To implement a foundational version of the branching evidence generation pipeline.
    - To produce mysteries where the solution requires players to synthesize multiple pieces of evidence.
    - To enable the elimination of innocent suspects based on logically sound alibis supported by evidence.
    - To lay the groundwork for more advanced evidence linking and corroboration features in future iterations.
- **Measurable Outcomes:**
    - Successful generation of 5 complete mystery scenarios using the MVP pipeline that are deemed solvable by elimination by internal review.
    - Average time to generate a complete mystery scenario (including branching evidence) within a target range (e.g., under X minutes - TBD based on initial performance testing).
- **Success Criteria:**
    - The MVP system consistently generates mysteries for 3 suspects where:
        - Each non-killer has a verifiable alibi supported by discoverable evidence fragments leading to `SUPPORTED` nuggets.
        - The killer can be uniquely identified by eliminating the other suspects.
        - All generated evidence fragments contribute to at least one information nugget.
    - The generated `BranchingCaseContext` object is complete and valid according to the defined Pydantic models.
    - The system integrates with pre-loaded map data for location information.
- **Key Performance Indicators (KPIs):**
    - Number of successfully generated and validated mystery scenarios per week during testing.
    - Percentage of generated scenarios passing `MasterCoherenceAgent` (MVP version) validation on the first attempt.
    - Qualitative feedback score from internal testers on puzzle coherence and solvability.

## Scope and Requirements (MVP / Current Version)

### Functional Requirements (High-Level)

- **FR1: Pydantic Model Implementation:** Implement all Pydantic models as defined in `docs/branching-evidence-design.md` Section 2.2.
- **FR2: Map Data Ingestion:** Ingest pre-defined map data (e.g., from `maps/Villa.json`) into the `BranchingCaseContext.timeline.locations` structure.
- **FR3: `NarrativeRefinementAgent` (MVP):**
    - Define core murder action details and timeline settings (`temporal_ambiguity_source`, `num_stages`, etc.).
    - Minimally refine existing MMOs for 3 suspects.
- **FR4: `TimelineOrchestratorAgent` (MVP):**
    - Plot killer's path and construct verifiable alibis for 2 non-killers within the `critical_action_window_stages`.
    - Generate `CharacterLocationStage` entries and critical `TimelineEvent` objects.
- **FR5: `InformationBlueprintAgent` (MVP):**
    - Define essential `InformationNugget` objects for alibis and subtle killer path support.
    - Define 1-2 `InformationFragment` objects per nugget for establishment.
    - Populate `InformationNugget.established_by_fragment_sets`.
    - Defer complex `CorroborationCondition` logic (structure present but not used for `CORROBORATED` status in MVP).
- **FR6: `ClueWeavingAgent` (MVP):**
    - Create `BranchingEvidenceItem` objects.
    - Generate `raw_data_from_evidence` for fragments (focus on `DIRECT_QUOTE` or simple `IMPLIED_BY_CONTEXT`).
    - Compose `full_description` for evidence items.
- **FR7: `MasterCoherenceAgent` (MVP - Simplified Validation):**
    - Validate non-killer alibis based on `SUPPORTED` nuggets.
    - Verify the killer does not have a provable alibi.
    - Ensure no wasted fragments.
    - Perform basic solvability check (elimination via `SUPPORTED` alibi nuggets).
- **FR8: Orchestration Flow (MVP):** Execute the agent pipeline (FR3-FR7) sequentially to produce a complete `BranchingCaseContext`.

### Non-Functional Requirements (NFRs)

- **Performance:**
    - Aim for mystery generation within a reasonable timeframe for development and testing (initial target TBD, e.g., < 5 minutes per scenario).
- **Scalability:**
    - MVP designed for 3 suspects. Future scalability will be a consideration for later versions.
- **Reliability/Availability:**
    - The generation process should be robust enough to complete without crashing for valid inputs.
    - Clear error handling for misconfigurations or unexpected data issues.
- **Security:**
    - Not a primary focus for this internal generation tool beyond standard good practices for code and dependency management.
- **Maintainability:**
    - Code should be well-structured, with clear separation of concerns between agents.
    - Pydantic models ensure data integrity.
    - Adherence to Python best practices and linting.
- **Usability/Accessibility:**
    - N/A for system-level backend components. Output `BranchingCaseContext` is for system consumption.
- **Other Constraints:**
    - Must use Python, Pydantic, and OpenAI Agents SDK.
    - Initial development assumes a pre-existing foundational mystery generation pipeline provides the starting `BranchingCaseContext`.

### User Experience (UX) Requirements (High-Level)

- N/A (Backend system)

### Integration Requirements (High-Level)

- **Integration Point 1:** Input `BranchingCaseContext` from a foundational mystery generation system (assumed to be available and compatible).
- **Integration Point 2:** Input map data from JSON files (e.g., `maps/Villa.json`).

### Testing Requirements (High-Level)

- Unit tests for individual agent logic and helper functions.
- Integration tests for the agent pipeline, verifying the output `BranchingCaseContext` against expected structures and simplified coherence rules.
- Generation and manual review of multiple mystery scenarios to assess solvability and coherence.
- _(See `docs/templates/testing-strategy.md` for more detailed planning if needed)_

## Epic Overview (MVP / Current Version)

- **Epic 1: Core Data Models & Narrative Foundation** - Goal: Implement all Pydantic models, map ingestion, and the MVP `NarrativeRefinementAgent`.
- **Epic 2: Timeline & Alibi Construction** - Goal: Implement the MVP `TimelineOrchestratorAgent` to build character movements, alibis, and key events.
- **Epic 3: Evidence Blueprinting (Basic)** - Goal: Implement the MVP `InformationBlueprintAgent` to define nuggets and their basic fragment-based establishment.
- **Epic 4: Evidence Weaving & Presentation** - Goal: Implement the MVP `ClueWeavingAgent` to create evidence items containing the raw data for fragments.
- **Epic 5: MVP Coherence & Orchestration** - Goal: Implement the MVP `MasterCoherenceAgent` for simplified validation and orchestrate the full MVP agent pipeline.

## Key Reference Documents

- `docs/branching-evidence-design.md`
- `docs/templates/project-brief.md` (For overall project context, though this PRD is more specific)
- `MurderMysteryGen/maps/Villa.json` (Example of map data to be ingested)
- `docs/epic1-branching-evidence.md`, `docs/epic2-branching-evidence.md`, ... (To be created)

## Post-MVP / Future Enhancements

- **"Should Have" from MVP Scope:**
    - `InformationBlueprintAgent` with basic `CorroborationCondition` logic.
    - `MasterCoherenceAgent` with enhanced basic validation (smoking guns, basic contradictions).
    - `ClueWeavingAgent` with more `FragmentConcealmentType` variety.
- **"Could Have" from MVP Scope:**
    - Full `CorroborationCondition` logic.
    - Advanced `MasterCoherenceAgent` (sophisticated validation, targeted feedback).
    - `EvidenceDistributionAgent` (staged reveals).
    - `MapGeneratorAgent`.
    - Complex Red Herrings.
- Refined iteration loop between `MasterCoherenceAgent` and other agents.
- Performance optimizations for larger-scale generation.

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
| Initial Draft | [Current Date] | 0.1 | First draft based on design doc and MVP scope. | PM Agent |

## Initial Architect Prompt

### Technical Infrastructure

- **Starter Project/Template:** Assume this builds upon the existing Mystery.AI Python codebase and conventions.
- **Hosting/Cloud Provider:** N/A for MVP (local execution assumed).
- **Frontend Platform:** N/A.
- **Backend Platform:** Python 3.12+, Pydantic, OpenAI Agents SDK.
- **Database Requirements:** N/A (data stored in `BranchingCaseContext` object, map data from JSON files).

### Technical Constraints

- Must adhere to Pydantic models defined in `docs/branching-evidence-design.md`.
- Must be ableto ingest map data from a JSON file format compatible with the `Location` model.
- The orchestration of agents should be sequential as outlined in the design document for MVP.
- Initial implementation should be robust for 3 suspects.

### Deployment Considerations

- N/A for MVP (focus on local execution and testing of the generation library). CI/CD for testing and linting is advisable.

### Local Development & Testing Requirements

- Standard Python virtual environment setup.
- Scripts or utilities to trigger the generation pipeline with specified inputs (e.g., path to foundational `BranchingCaseContext` JSON, path to map JSON).
- Utilities to serialize the output `BranchingCaseContext` to JSON for inspection.
- Clear logging from each agent to trace the generation process.

### Other Technical Considerations

- **Modularity:** Design agents and their internal logic to be as modular as possible to facilitate future enhancements and individual testing.
- **Error Handling:** Implement robust error handling within agents and the orchestration flow to manage issues like invalid input data or unexpected LLM responses.
- **Configuration:** Consider how parameters (e.g., number of stages, specific LLM models per agent if varied) might be configured, even if hardcoded for MVP. 