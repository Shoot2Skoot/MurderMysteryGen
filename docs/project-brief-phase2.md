# Project Brief: Mystery.AI - Phase 2: Enhanced Foundational Diversity & Richer Individual Evidence

## Introduction / Problem Statement

The current Mystery.AI MVP successfully generates core mystery elements. This phase focuses on two key improvements:
1.  Injecting greater diversity into foundational narrative components (victim, suspects) using structured, "forced diversity" through curated and dynamically generated lists, moving away from unreliable model tuning or vague prompting.
2.  Enhancing the richness and strategic value of individual evidence items, making them more varied in type and narrative function, as a precursor to more complex evidence structures.

## Vision & Goals

- **Vision:** To evolve Mystery.AI into a system that produces a richer tapestry of distinct mystery scenarios by systematically incorporating diverse creative elements for characters and situations, and by generating more varied and nuanced individual pieces of evidence.
- **Primary Goals:**
    1.  **Goal 1 (Static List Integration - Core Victim/Suspect Attributes):** Implement a mechanism for the `CaseInitializationAgent` to select key victim attributes (e.g., `Cause of Death`, `Motive Category` leading to the crime, `Occupation Archetype`, `Personality Archetype`) from provided lists of 2-3 options (randomly selected from master lists) and integrate them thematically.
    2.  **Goal 2 (Dynamic List Generation - Thematic Names):** Design and implement a "Pre-Initialization Ideation Agent" that, given a theme, generates lists of plausible `First Names` and `Last Names` (e.g., 50 each) consistent with that theme. Modify relevant agents to utilize these lists for victim and suspect naming.
    3.  **Goal 3 (System-Wide Orchestration & Data Model Update for Diversity Features):** Update the main orchestration logic to incorporate the new list generation and selection steps for attributes and names, ensuring data flows correctly. Update `CaseContext` and relevant Pydantic models as needed.
    4.  **Goal 4 (Advanced Individual Evidence Generation):** Enhance the `EvidenceGenerationAgent` and `EvidenceItem` data model to produce more varied and strategically nuanced evidence. This includes:
        *   Introducing a master list of **Evidence Categories/Types** (e.g., "Personal Correspondence," "Official Document," "Physical Object," "Witness Snippet") for the agent to select from.
        *   Tasking the agent to generate evidence with varying degrees of **Directness/Subtlety** or narrative function.
        *   Updating the `EvidenceItem` model to store these new attributes (e.g., `evidence_category: str`, `narrative_function_description: str`).
- **Success Metrics:**
    -   The system successfully incorporates selected items from static lists (Cause of Death, Motive Category, Occupation, Personality) into >90% of generated victim/suspect profiles, maintaining thematic coherence.
    -   The Pre-Initialization Ideation Agent generates thematically relevant name lists with >80% of items deemed plausible by human review for 3 diverse themes.
    -   Generated `EvidenceItem` instances consistently include `evidence_category` and a `narrative_function_description` in >90% of cases.
    -   A human reviewer, comparing 10 outputs from the previous MVP with 10 outputs from this new version (using the same themes), perceives a notable increase in the variety of core victim/suspect attributes, names, and the descriptive richness of individual evidence items.

## Target Audience / Users

Remains the human author/designer (yourself), aiming to provide them with more varied, surprising, and narratively rich starting points for their mysteries.

## Key Features / Scope (High-Level Ideas for these Epics)

- **Feature 1 (Corresponds to Goal 1): Static List Selection Mechanism (Victim/Suspect Attributes):**
    -   Develop/Curate master lists for: Cause of Death, Motive Categories, Generic Occupation Archetypes, Personality Archetypes.
    -   Modify orchestrator to randomly select 2-3 items from each master list.
    -   Modify `CaseInitializationAgent` (and potentially `SuspectGenerationAgent`) to accept these smaller lists, select one item from each, and weave it into the profiles thematically.
- **Feature 2 (Corresponds to Goal 2): Dynamic Thematic List Generation (Names):**
    -   Create `PreInitializationIdeationAgent` (Input: Theme; Output: Structured lists of first/last names).
    -   Integrate this agent into the orchestration flow before victim/suspect generation.
    -   Modify relevant agents to use these generated name lists.
- **Feature 3 (Corresponds to Goal 3): Data Model & Orchestration Updates for Diversity:**
    -   Update `CaseContext`, `VictimProfile`, `SuspectProfile`, etc., to handle/store new selected attributes.
    -   Refine the main orchestrator for new agent calls and data flow.
- **Feature 4 (Corresponds to Goal 4): Enhanced Individual Evidence Generation:**
    -   Develop/Curate a master list of Evidence Categories/Types.
    -   Update `EvidenceGenerationAgent` instructions to:
        -   Accept and select from a sub-list of Evidence Categories.
        -   Generate a `narrative_function_description` reflecting intended subtlety or directness.
    -   Extend `EvidenceItem` Pydantic model in `core/data_models.py` with `evidence_category: str` and `narrative_function_description: str`.
    -   Update orchestration to provide category sub-lists to the `EvidenceGenerationAgent`.

## Known Technical Constraints or Preferences

- **Constraints:** Same as MVP (OpenAI Agents SDK, Python 3.12.3, target LLMs).
- **Focus:** Avoid model tuning and generic "be more diverse" prompting.
- **Preferences:** Modular agent design. Clear structured inputs.
- **Risks:**
    -   Generating high-quality, *thematically appropriate* lists (especially names) dynamically.
    -   Ensuring agents *meaningfully integrate* selected list items.
    -   Static master lists needing curation.
    -   `EvidenceGenerationAgent` might struggle with consistent quality for "narrative function" without very careful prompting.

## Relevant Research (Optional)

The existing `docs/deep-research-report-BA.md` is relevant. For Evidence Categories and narrative functions, insights from professional mystery writing on clue types and misdirection will be valuable.

## PM Prompt

"You are an expert Product Manager AI. We have successfully completed the MVP for Mystery.AI (Epics 1-4). This new phase, **Phase 2: Enhanced Foundational Diversity & Richer Individual Evidence**, aims to significantly improve the variety and richness of generated mysteries by:
1.  Implementing 'forced diversity' for core victim/suspect attributes using curated and dynamically generated lists.
2.  Enhancing the strategic value and narrative function of individual evidence items.

**Core Task:** Based on the updated 'Project Brief: Mystery.AI - Phase 2,' develop a detailed Product Requirements Document (PRD) and 3-4 initial draft Epics.

**Focus for PRD & Epics:**
1.  **Static List Integration (Goal 1):** Requirements for creating/integrating master lists for Cause of Death, Motive Categories, Occupation Archetypes, Personality Archetypes. Detail orchestrator selection of sub-lists and agent integration into `VictimProfile`/`SuspectProfile`.
2.  **Dynamic Thematic List Generation (Goal 2):** Requirements for `PreInitializationIdeationAgent` (generating thematic First/Last Names) and its integration for victim/suspect naming.
3.  **System & Data Model Updates for Diversity (Goal 3):** Requirements for `CaseContext` and other data model changes, plus orchestration flow modifications for these diversity features.
4.  **Advanced Individual Evidence Generation (Goal 4):** Requirements for:
    *   Master list of Evidence Categories/Types.
    *   Modifications to `EvidenceGenerationAgent` to select categories and describe the evidence's narrative function/subtlety.
    *   Updates to the `EvidenceItem` Pydantic model (add `evidence_category`, `narrative_function_description`).
    *   Orchestration changes to support this.

**Key Considerations:**
*   **Forced Diversity & Thematic Integration:** Agents must choose from provided options and integrate them naturally.
*   **Maintainability of Lists:** How will master lists be managed?
*   **Richer Evidence Building Blocks:** Goal 4 aims to improve individual evidence items as a step towards more complex future evidence structures.

**Deliverables:**
1.  `prd-phase2.md` covering the scope of these four goals.
2.  Initial draft Epic markdown files (e.g., `epic5-StaticListIntegration.md`, `epic6-DynamicNameGeneration.md`, `epic7-AdvancedEvidenceItems.md`, `epic8-SystemUpdatesForPhase2.md` – names illustrative) outlining user stories and acceptance criteria." 