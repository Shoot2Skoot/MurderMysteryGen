# Epic 7: (Advanced PoC) Generative Augmentation & Feedback Loops for Enhanced Uniqueness

**Goal:** To explore and implement Proof-of-Concept (PoC) advanced generative techniques or feedback loops designed to further enhance the uniqueness and creativity of generated mystery scenarios, particularly in ensuring that multiple runs with the same theme yield significantly different core plot structures and character roles.

**Rationale:** While prompt engineering (Epic 5) and parameter tuning (Epic 6) can improve diversity, some level of repetition or adherence to common patterns may persist. This epic explores more structural or process-oriented changes to the generation pipeline to break out of these patterns and achieve a higher degree of originality and "surprise" in the generated mysteries. This is more experimental and focused on PoCs rather than full integration into the main product for Phase 2 unless a PoC is highly successful and simple to integrate.

**Key Performance Indicators (KPIs) for this Epic:**
-   Successful implementation and demonstration of at least one PoC advanced augmentation technique.
-   Qualitative assessment showing that the PoC technique leads to demonstrably more unique or unexpected mystery elements compared to baseline from Epics 5 & 6.
-   Documentation of the PoC's design, implementation, results, and potential for future integration.

## Stories (Examples - to be refined based on PoC choices)

### Story 7.1: PoC - "Thematic Aspect Deconstruction" Agent

-   **Goal:** As a Developer, I want to create a PoC for a `ThematicAspectDeconstructionAgent` that, given a broad theme, generates a list of diverse and specific sub-elements (e.g., unique locations, character archetypes, conflict types, unusual objects/technologies) relevant to that theme, which can then be used to seed or constrain downstream generation agents.
-   **Example:** Theme "Cyberpunk City." Agent might output: ["Corrupt AI Politician", "Black Market Organ Scavenger", "Memory Wipe Drug", "Abandoned Subway Network Hideout", "Digital Ghost Uprising"].
-   **Detailed Requirements:** (To be further detailed if this PoC is prioritized)
    -   Define the `ThematicAspectDeconstructionAgent` and its prompt to break down a theme into 5-7 diverse, concrete elements.
    -   Develop a strategy for how these generated sub-elements would be incorporated as more specific inputs or constraints for the `CaseInitializationAgent` or `SuspectGenerationAgent`.
    -   Implement a test script to run this agent with 2-3 themes and analyze the output for diversity and usefulness.
-   **Acceptance Criteria:**
    -   AC1: The agent generates a list of at least 5 distinct, thematically relevant sub-elements for 3 different test themes.
    -   AC2: A clear written plan or a small code prototype demonstrates how at least one generated sub-element could be used to influence victim or suspect generation.
    -   AC3: Qualitative assessment suggests the generated sub-elements have the potential to increase scenario uniqueness.
-   **Dependencies:** Understanding of content from Epics 5 & 6 (to know what needs further diversification).
-   **Status:** To Do

---

### Story 7.2: PoC - Simple "Cliché Avoidance" Post-Processing Step

-   **Goal:** As a Developer, I want to create a PoC for a simple post-processing step that reviews a generated `CaseContext` for one or two predefined clichés (e.g., "victim is a school teacher in a suburban theme," "cause of death is simple poisoning with arsenic") and, if found, flags it or attempts a targeted re-generation of that specific element with a negative constraint.
-   **Detailed Requirements:** (To be further detailed if this PoC is prioritized)
    -   Identify 1-2 common clichés observed from MVP and Epic 5/6 testing.
    -   Develop a Python function (or a very simple, non-LLM rule-based agent) to detect these specific clichés in a `CaseContext` object.
    -   If a cliché is detected, implement a basic re-run of the relevant agent (e.g., `CaseInitializationAgent` for victim-related clichés) with a modified input that includes an explicit instruction to avoid the detected cliché (e.g., adding "The victim should NOT be a school teacher" to the input prompt for the re-run).
    -   Compare the original and re-generated outputs.
-   **Acceptance Criteria:**
    -   AC1: The PoC can reliably detect at least one predefined cliché in a sample `CaseContext` where it exists.
    -   AC2: If a cliché is detected, the PoC attempts a re-generation of the affected part, and the new output successfully avoids that specific cliché while maintaining overall coherence.
-   **Dependencies:** Results and observations from Epics 5 & 6.
-   **Status:** To Do

---

### Story 7.3: PoC - Introducing Controlled Randomness from Curated Lists

-   **Goal:** As a Developer, I want to experiment with a PoC where, for a specific element like "Means" or "Unusual Object integral to the plot," the system first randomly selects an item from a small, curated, thematically-tagged list, and then tasks an LLM agent to build a narrative component (e.g., a Means, a piece of Evidence) around that selected item.
-   **Example:** For a "Victorian London" theme, a curated list of "Unusual Thematic Objects" might include ["Clockwork automaton servant", "Phial of an experimental ether", "Stolen Egyptian artifact with a supposed curse"]. The system picks one, then asks `EvidenceGenerationAgent` or `MMOGenerationAgent` to incorporate it meaningfully.
-   **Detailed Requirements:** (To be further detailed if this PoC is prioritized)
    -   Create 2-3 small example curated lists (e.g., 5-10 items per list) of specific elements (like unusual murder weapons, unique locations, or MacGuffins) for 2 different themes.
    -   Modify an existing agent's workflow (or create a wrapper) to first randomly select an item from an appropriate curated list.
    -   Update the agent's prompt to explicitly instruct it to incorporate the selected item centrally into its generation task (e.g., "Generate a Means for this suspect that *must involve* a 'clockwork automaton servant'.").
-   **Acceptance Criteria:**
    -   AC1: The PoC demonstrates an agent using a pre-selected item from a curated list as a core constraint for its generation task.
    -   AC2: The LLM successfully incorporates the randomly selected item into a coherent and plausible output (e.g., a Means or EvidenceItem description).
    -   AC3: Qualitative assessment suggests this approach can lead to more unique and thematically specific story elements.
-   **Dependencies:** Epics 5 & 6.
-   **Status:** To Do

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
|        |      | 1.0     | Initial draft of Epic 7 and PoC story ideas. | PM Agent | 