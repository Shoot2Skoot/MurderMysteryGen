# API Reference (MVP)

This document provides a reference for the key application programming interfaces (APIs) and command-line interfaces (CLIs) for the Mystery.AI system, with a focus on the Branching Evidence System MVP.

## 1. Command-Line Interfaces (CLI)

These scripts provide command-line access for running parts of or the entire Branching Evidence System generation pipeline. They are typically located in `MurderMysteryGen/tools/branching_evidence_runners/` or a main orchestration script in `MurderMysteryGen/src/mystery_ai/orchestration/`.

### 1.1. Full Branching Evidence MVP Pipeline Runner

-   **Script (Example):** `python -m src.mystery_ai.orchestration.run_full_branching_pipeline --case_file path/to/initial_case.json --map_file path/to/map.json --output_file path/to/final_branching_case.json`
    -   (Actual script name and location to be finalized as per `project-structure.md` update for Epic 5, Story 5.2).
-   **Description:** Executes the complete MVP pipeline for the Branching Evidence System.
-   **Arguments:**
    -   `--case_file` (str, required): Path to the input JSON file containing the foundational `BranchingCaseContext` (theme, victim, 3 suspects with MMOs, killer designated).
    -   `--map_file` (str, required): Path to the JSON file containing the map data (e.g., `maps/Villa.json`).
    -   `--output_file` (str, required): Path where the final `BranchingCaseContext` (with branching evidence) will be saved as a JSON file.
    -   `--debug` (flag, optional): Enables more verbose logging.

### 1.2. Individual Epic/Agent Test Runners (MVP)

These scripts are primarily for development and testing of individual agent capabilities as outlined in their respective Epics.

#### 1.2.1. Narrative Refinement Agent Runner (Epic 1)

-   **Script (Example):** `python -m tools.branching_evidence_runners.run_narrative_refinement_mvp --case_file path/to/initial_case.json --map_file path/to/map.json --output_file path/to/narrative_refined_case.json`
-   **Description:** Runs the MVP version of the `NarrativeRefinementAgent`.
-   **Arguments:**
    -   `--case_file` (str, required): Path to the input JSON file (foundational `BranchingCaseContext`).
    -   `--map_file` (str, required): Path to the map JSON file.
    -   `--output_file` (str, required): Path to save the `BranchingCaseContext` after narrative refinement.

#### 1.2.2. Timeline Orchestrator Agent Runner (Epic 2)

-   **Script (Example):** `python -m tools.branching_evidence_runners.run_timeline_orchestrator_mvp --input_case_file path/to/narrative_refined_case.json --output_file path/to/timeline_orchestrated_case.json`
-   **Description:** Runs the MVP version of the `TimelineOrchestratorAgent`.
-   **Arguments:**
    -   `--input_case_file` (str, required): Path to the `BranchingCaseContext` JSON (output from narrative refinement).
    -   `--output_file` (str, required): Path to save the `BranchingCaseContext` after timeline orchestration.

#### 1.2.3. Information Blueprint Agent Runner (Epic 3)

-   **Script (Example):** `python -m tools.branching_evidence_runners.run_information_blueprint_mvp --input_case_file path/to/timeline_orchestrated_case.json --output_file path/to/blueprinted_case.json`
-   **Description:** Runs the MVP version of the `InformationBlueprintAgent`.
-   **Arguments:**
    -   `--input_case_file` (str, required): Path to the `BranchingCaseContext` JSON (output from timeline orchestration).
    -   `--output_file` (str, required): Path to save the `BranchingCaseContext` after information blueprinting.

#### 1.2.4. Clue Weaving Agent Runner (Epic 4)

-   **Script (Example):** `python -m tools.branching_evidence_runners.run_clue_weaving_mvp --input_case_file path/to/blueprinted_case.json --output_file path/to/woven_case.json`
-   **Description:** Runs the MVP version of the `ClueWeavingAgent`.
-   **Arguments:**
    -   `--input_case_file` (str, required): Path to the `BranchingCaseContext` JSON (output from information blueprinting).
    -   `--output_file` (str, required): Path to save the `BranchingCaseContext` after clue weaving.

*(Note: The MasterCoherenceAgent is part of the full pipeline runner and might not have a standalone CLI runner for MVP if its primary role is validation at the end of the sequence.)*

## 2. Agent Programmatic Interfaces (High-Level for Branching Evidence MVP)

The Branching Evidence System agents are designed to be orchestrated sequentially, each taking a `BranchingCaseContext` object (or relevant parts of it, along with map data where applicable) and returning an updated `BranchingCaseContext`.

They are implemented as instances of `agents.Agent` from the OpenAI Agents SDK.

### 2.1. General Interaction Pattern

```python
from agents import Agent, Runner
from mystery_ai.core.data_models_branching import BranchingCaseContext # Assuming this path
from mystery_ai.core.data_models import Location # Assuming this path for Location if separate

# Assume 'initial_context' is a BranchingCaseContext instance
# Assume 'map_locations' is a List[Location]

# Example with NarrativeRefinementAgent (conceptual)
# narrative_refinement_agent = Agent(...) # Agent definition

# Input for the agent typically includes the current context and potentially specific parts
# For agents like NarrativeRefinementAgent, the input to the LLM might be a dict derived from the context.
agent_input_data = {
    "theme": initial_context.theme,
    "victim_name": initial_context.victim.name if initial_context.victim else None,
    "suspects": [
        {"name": s.name, "mmo_means": s.mmo.means, ...} for s in initial_context.suspects
    ],
    "killer_name": initial_context.get_killer().name if initial_context.get_killer() else None,
    "map_summary": f"{len(map_locations)} locations available."
}

# updated_context_fields = Runner.run_sync(narrative_refinement_agent, input=agent_input_data)
# initial_context.timeline.settings = updated_context_fields.timeline_settings # Example update
# initial_context.core_murder_action_description = updated_context_fields.core_murder_action_description
```

**Note:** The exact structure of the `input` dictionary/Pydantic model passed to each agent's `Runner.run_sync()` method will depend on the agent's specific `instructions` and what data it needs to perform its task. The primary output is the modification of the `BranchingCaseContext` object, or specific new data structures that get integrated into it.

### 2.2. Key Agents & Their Role (Branching Evidence MVP)

Refer to `docs/architecture.md` (Branching Evidence section) and `docs/branching-evidence-design.md` (Section 3) for detailed agent responsibilities.

-   **`NarrativeRefinementAgent`**
    -   **Input:** Initial `BranchingCaseContext` (theme, victim, suspects with basic MMOs, designated killer), `List[Location]`.
    -   **Output:** Updates `BranchingCaseContext` with `core_murder_action_description`, `core_murder_action_stage_window`, and `timeline.settings` (`temporal_ambiguity_source`, `num_stages`, `stage_duration_description`, `critical_action_window_stages`).

-   **`TimelineOrchestratorAgent`**
    -   **Input:** `BranchingCaseContext` (with narrative refinements and locations).
    -   **Output:** Updates `BranchingCaseContext` by populating `timeline.events` and `timeline.character_movements`.

-   **`InformationBlueprintAgent`**
    -   **Input:** `BranchingCaseContext` (with timeline and character movements).
    -   **Output:** Updates `BranchingCaseContext` by populating `information_nuggets` (with `description`, `established_by_fragment_sets`, `status=UNKNOWN`, critical flags) and `information_fragments` (with `fragment_id`, `atomic_fact_derived`).

-   **`ClueWeavingAgent`**
    -   **Input:** `BranchingCaseContext` (with information blueprint).
    -   **Output:** Updates `BranchingCaseContext` by populating `evidence_items` (with `evidence_id`, `category`, `full_description`, `contains_nugget_ids`) and completing `information_fragments` (with `raw_data_from_evidence`, `source_evidence_item_id`, `fragment_concealment_type`).

-   **`EvidenceDistributionAgent`**
    -   **Input:** `BranchingCaseContext` (with all evidence items defined).
    -   **Output:** Updates `BranchingCaseContext` by setting `is_initially_available = True` on all `BranchingEvidenceItem` objects for MVP.

-   **`MasterCoherenceAgent`**
    -   **Input:** Complete `BranchingCaseContext`.
    -   **Output:** A validation report (e.g., dictionary: `{"is_coherent": True/False, "reason": "Details..."}`). Does not directly modify the `BranchingCaseContext` itself.

This API reference provides a high-level overview. For detailed Pydantic model structures, refer to `docs/data-models.md` (Branching Evidence section). 