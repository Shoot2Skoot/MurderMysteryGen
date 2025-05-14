# Branching Evidence Architecture & Design

## 1. Introduction & Design Philosophy

This document outlines the proposed architecture and data model design for implementing a branching evidence system within Mystery.AI. This phase builds upon the existing MMO generation capabilities (MVP and Phase 2) to create a more complex, interconnected web of evidence suitable for an elimination-focused mystery game.

The goal is not simply to link evidence to MMO components, but to simulate an intricate investigative process where players must synthesize information from multiple sources to definitively rule out innocent suspects, ultimately revealing the killer by process of elimination.

Based on analysis of the desired game mechanics and previous design iterations (`ref/mmo_tree_example.mermaid`, `ref/mmo_tree_explanation.md`, and user input), the following core principles guide this design:

### 1.1. Blended Generation Approach

Neither a purely MMO-first nor a purely Timeline-first approach fully captures the desired complexity. We will adopt a **Blended Approach**:

1.  **Phase A: Narrative Foundation (MMO-Influenced):** Generate initial plausible MMOs for all suspects, select a killer, and define the *core murder action(s)* (what, where, when) including the *source of temporal ambiguity*.
2.  **Phase B: Timeline Construction & Ambiguity Mapping:** Detail the critical paths for the killer and victim around the core action(s) within defined **Time Stages**. Establish alibis for non-killers *across the relevant time window(s)*. Map events/clues that create or explain the temporal ambiguity.
3.  **Phase C: MMO Refinement & Weakening:** Validate the killer's MMO against the timeline. Weaken non-killer MMOs by explicitly linking the weakened element to timeline-based alibis or contradictions established in Phase B.
4.  **Phase D: Information-Centric Evidence Generation:** Deconstruct the timeline and refined MMOs into **Factual Propositions**. Generate atomic **Information Nuggets** required to prove/disprove these propositions. Strategically distribute these nuggets into narratively plausible **Evidence Item** containers, ensuring high interconnectivity, corroboration, and the need for player synthesis.

### 1.2. Winning by Elimination

The core game mechanic is elimination, not direct proof. Players must gather sufficient evidence to *conclusively disprove* the possibility of guilt for *each* innocent suspect. The killer is the one left standing. **Note:** This principle guides the *design* of the mystery's evidence structure to ensure elimination is the only logical path to a solution; it is not necessarily an explicit rule enforced on the player via the game interface. This requires:
*   Robust alibis for non-killers, supported by corroborated evidence.
*   Subtle confirmation of the killer's path, without obvious "smoking gun" clues.

### 1.3. Discrete Time Stages

The mystery's timeline will be broken into a defined number of discrete **Time Stages** (e.g., 3-7, typically 4-5). Each stage represents a unit of time relevant to the narrative (e.g., 15 minutes, 1 hour).
*   Character locations and key actions are tracked relative to these stages.
*   The number of stages influences complexity and map requirements.
*   Players implicitly reconstruct a "Character-Location-Stage" understanding.

### 1.4. Temporal Ambiguity

The precise moment of the core murder action(s) or time of death should be intentionally obscured within a plausible *window* spanning one or more stages. This prevents players from solving the mystery by simply focusing on a single time slot. Alibis must hold across the entire relevant window.

### 1.5. Information Nuggets & Synthesis

*   Evidence is composed of atomic **Information Nuggets**.
*   An **Evidence Item** (e.g., a letter, a logbook) acts as a container for one or more nuggets.
*   Nuggets often relate to different suspects or propositions, even within the same Evidence Item.
*   Solving requires **Information Synthesis**: players must combine multiple nuggets (often from different Evidence Items) to confirm or refute key Factual Propositions. Single nuggets should rarely solve a major point alone. Dependencies between nuggets (A must be known to understand B) should be designed in.

### 1.6. No Wasted Evidence & High Interconnectivity

Every Evidence Item, and ideally every Information Nugget within it, must serve a purpose towards the elimination process (supporting alibis, refuting claims, establishing necessary context, subtly pointing towards the killer, creating valid red herrings). Evidence should be highly interconnected, with nuggets corroborating each other across different items and suspects.

---

With this philosophy established, the following sections will detail the proposed data models and agent responsibilities designed to enable this approach. 

## 2. Data Model Specifications

### 2.1 Location & Map Design Principles

Generating compelling and logically sound maps for murder mysteries is a significant challenge. The map directly influences the plausibility of timelines, alibis, and witnessed events. While the `Location` data model (defined below) includes fields for connections (`connected_location_ids`, `can_be_seen_from_ids`, `within_earshot_from_ids`), automatically populating these fields to create a high-quality, playable map via AI is complex and potentially requires dedicated development and testing outside the initial scope of this branching evidence system.

Key considerations for effective map design include:

*   **Size and Scope:** Typically 10-20 distinct, named locations are suitable, depending on the number of suspects and desired complexity.
*   **Connectivity:** Avoid excessive choke points (single corridors connecting large areas) which can overly simplify movement tracking. Ensure logical flow (e.g., bedrooms don't all interconnect directly).
*   **Uniqueness:** Rooms should have distinct features or purposes to aid player navigation and provide unique settings for clues.
*   **Sensory Connections:** Define sightlines (windows, doorways) and hearing ranges realistically to support witness accounts or overheard conversations.
*   **Traversal Time:** Implicitly or explicitly consider the time required to move between locations, influencing the feasibility of alibis.

**Implementation Note:** For the initial phases of implementing this branching evidence design, map generation may rely on simpler heuristics, pre-defined templates, or manual configuration rather than fully autonomous AI generation. Advanced, validated AI map generation can be considered a future enhancement.

### 2.2 Pydantic Models

This section defines the core Pydantic models required to represent the structure of the mystery, including the timeline, locations, events, and the foundation for the branching evidence graph. These models will likely reside in `src/mystery_ai/core/data_models.py` or a dedicated submodule for branching structures.

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

# --- Reused/Existing Models (Assume defined elsewhere) ---
# from .existing_models import VictimProfile, Suspect, MMOElementType 

# --- Timeline and Setting Models ---

class TimelineSettings(BaseModel):
    """Defines the overall parameters of the mystery's timeline."""
    num_stages: int = Field(
        description="The total number of discrete time stages in the mystery (e.g., 3-7)."
    )
    stage_duration_description: str = Field(
        description="A human-readable description of what each stage represents (e.g., 'Approx. 30 minutes', 'Between dinner courses')."
    )
    temporal_ambiguity_source: str = Field(
        description="Explanation of how the exact timing of the core murder action is obscured (e.g., 'Delayed poison effect', 'Conflicting witness reports about the gunshot', 'Victim found long after estimated time of death')."
    )
    critical_action_window_stages: List[int] = Field(
        description="List of stage numbers (1-indexed) during which the core lethal action *could* have occurred."
    )

class Location(BaseModel):
    """Represents a distinct location within the mystery setting."""
    location_id: str = Field(
        description="Unique identifier for the location (e.g., 'loc_library', 'loc_garden')."
    )
    name: str = Field(description="Human-readable name of the location (e.g., 'Library', 'Walled Garden').")
    description: Optional[str] = Field(
        default=None,
        description="Optional description of the location, potentially including features relevant to clues (e.g., 'Dusty, with shelves reaching the ceiling', 'Has a single window overlooking the courtyard')."
    )
    # New fields for spatial relationships
    connected_location_ids: List[str] = Field(
        default_factory=list,
        description="List of location IDs directly connected via normal paths (e.g., doors, hallways). Assumed to be two-way unless specified otherwise by game logic."
    )
    secret_connections: Optional[List[Dict[str, str]]] = Field(
        default=None,
        description="Optional list of secret connections, each a dict with 'to_location_id' and 'description' (e.g., {'to_location_id': 'loc_cellar', 'description': 'Hidden trapdoor under rug'})."
    )
    can_be_seen_from_ids: List[str] = Field(
        default_factory=list,
        description="List of location IDs from which *this* location (self) can be seen (e.g., if 'loc_hallway' is in 'loc_kitchen.can_be_seen_from_ids', then from the hallway you can see into the kitchen)."
    )
    can_be_heard_from_ids: List[str] = Field(
        default_factory=list,
        description="List of location IDs from which sounds occurring in *this* location (self) might be heard (e.g., if 'loc_study' is in 'loc_library.can_be_heard_from_ids', sounds in the library can be heard in the study)."
    )

class TimelineEvent(BaseModel):
    """Represents a key event happening at a specific stage."""
    event_id: str = Field(description="Unique identifier for the event.")
    stage: int = Field(description="The stage number (1-indexed) during which this event occurs.")
    description: str = Field(description="Description of the event (e.g., 'Loud crash heard from upstairs', 'Power flickers momentarily', 'Argument between Character A and B').")
    location_ids: List[str] = Field(
        default_factory=list, 
        description="List of location IDs where this event happens or is observable from."
    )
    involved_character_names: List[str] = Field(
        default_factory=list, 
        description="List of names of characters directly involved or witnessing the event."
    )
    # Link to propositions this event might support/refute? TBD later.

class CharacterLocationStage(BaseModel):
    """Tracks the confirmed or inferred location of a character during a specific stage."""
    character_name: str = Field(description="Name of the character.")
    stage: int = Field(description="The stage number (1-indexed).")
    location_id: str = Field(description="The location ID where the character is during this stage.")
    # Optional: How is this known? Via which nugget/evidence? TBD later.
    confirmation_source_description: Optional[str] = Field(
        default=None, 
        description="Brief note on how this location is known (e.g., 'Seen by Witness X', 'Logbook entry', 'Self-reported')."
    )

class MysteryTimeline(BaseModel):
    """Encapsulates the entire timeline structure of the mystery."""
    settings: TimelineSettings = Field(description="Global timeline parameters.")
    locations: List[Location] = Field(description="List of all defined locations in the setting.")
    events: List[TimelineEvent] = Field(description="List of key events occurring during the timeline.")
    character_movements: List[CharacterLocationStage] = Field(
        description="List tracking character locations across stages, forming the implicit timeline grid."
    )

# --- Core Branching Context (Extends or Replaces CaseContext) ---

class BranchingCaseContext(BaseModel):
    """Top-level container for a mystery generated with branching evidence."""
    # Inherited/Reused Fields from original CaseContext
    theme: str = Field(description="The overall theme or setting of the mystery.")
    victim: Optional['VictimProfile'] = Field(default=None, description="Details of the victim.")
    suspects: List['Suspect'] = Field(default_factory=list, description="A list of all suspects involved.")
    timeline: 'MysteryTimeline' = Field(description="The structured timeline of the mystery.")
    
    # Evidence Graph Components
    evidence_items: List['BranchingEvidenceItem'] = Field(
        default_factory=list, 
        description="List of all evidence items (e.g., documents, objects) that players can find. These items contain the raw data from which fragments are derived."
    )
    information_fragments: List['InformationFragment'] = Field(
        default_factory=list, 
        description="List of all atomic facts/observations (each with raw_data_from_evidence and atomic_fact_derived) derived directly from single evidence items. These are the building blocks for nuggets."
    )
    information_nuggets: List['InformationNugget'] = Field(
        default_factory=list, 
        description="List of all core factual statements or synthesized inferences about the mystery. Their status (e.g., UNKNOWN, SUPPORTED, CORROBORATED) is tracked, and they are established by fragments and corroborated by a wider context of other nuggets and linking fragments."
    )
    
    # Optional: Maybe add fields for the core murder action details?
    core_murder_action_description: Optional[str] = Field(default=None, description="Description of the specific lethal action.")
    core_murder_action_stage_window: Optional[List[int]] = Field(default=None, description="Stage window when lethal action occurred.")

    # Ensure compatibility with OpenAI Agents SDK structured outputs
    model_config = {"extra": "ignore"}

# --- Evidence Graph Components ---

class FragmentConcealmentType(Enum):
    """Describes how an information fragment is presented or obscured within an evidence item."""
    DIRECT_QUOTE = "direct_quote" # Fragment is a direct textual quote.
    IMPLIED_BY_CONTEXT = "implied_by_context" # Fragment is not directly stated but heavily implied by surrounding text/imagery.
    REDACTED_OR_DAMAGED = "redacted_or_damaged" # Fragment is partially obscured (e.g., torn page, blacked-out text, corrupted file).
    CODED_LANGUAGE = "coded_language" # Fragment is present but uses code, jargon, or metaphor requiring interpretation.
    VISUAL_DETAIL = "visual_detail" # Fragment is an observable detail in an image, map, or physical object description.

class NuggetStatus(Enum):
    """Represents the current state of belief or confirmation for an Information Nugget."""
    UNKNOWN = "unknown"         # Not enough information yet.
    SUPPORTED = "supported"     # At least one set of required fragments is known, suggesting true.
    REFUTED = "refuted"         # Contradicted by a corroborated nugget or strong evidence.
    CONTRADICTED = "contradicted" # Supporting fragments exist, but conflicts with other SUPPORTED nuggets. Needs resolution.
    CORROBORATED = "corroborated" # Supported and consistent with related nuggets, considered a reliable fact.

class CorroborationCondition(BaseModel):
    """Defines a set of conditions that, if met, can elevate a SUPPORTED InformationNugget to CORROBORATED status."""
    # All nuggets in this list must have a status of SUPPORTED or CORROBORATED.
    required_supporting_nugget_ids: List[str] = Field(
        default_factory=list,
        description="List of other InformationNugget IDs that must be at least SUPPORTED."
    )
    # All fragments in this list must be known (i.e., their atomic_fact_derived is considered true because their source EvidenceItem is found).
    required_linking_fragment_ids: List[str] = Field(
        default_factory=list,
        description="List of specific InformationFragment IDs that act as crucial links or additional minor confirmations."
    )
    # Optional: A human-readable description of why this set of conditions leads to corroboration.
    condition_description: Optional[str] = Field(
        default=None,
        description="Optional: Explanation of how these combined elements achieve corroboration for the parent nugget."
    )

class InformationFragment(BaseModel):
    """Represents a fragment of information derived from raw data."""
    fragment_id: str = Field(description="Unique identifier for this fragment.")
    raw_data_from_evidence: str = Field(description="The raw data from which this fragment is derived.")
    atomic_fact_derived: str = Field(description="The atomic fact derived from the raw data.")

class InformationNugget(BaseModel):
    """Represents a core factual statement, inference, or piece of knowledge about the mystery.
    Its truth is established by synthesizing one or more InformationFragments."""
    nugget_id: str = Field(description="Unique identifier for this factual statement (e.g., 'nug_roma_in_arcade_p2', 'nug_amber_location_yoga_p2').")
    # This description IS the statement of fact itself.
    description: str = Field(
        description="The statement of fact this nugget represents (e.g., 'Amber was in the Yoga Studio during Phase 2.', 'Roma screamed out of joy during Phase 2.')."
    )
    # How this nugget/fact is established: List of sets of fragment IDs.
    # The nugget is SUPPORTED if ALL fragments in ANY *one* of these inner lists are known.
    established_by_fragment_sets: List[List[str]] = Field(
        description="Defines how this nugget is proven. A list of lists (sets) of required fragment_ids. Nugget status becomes SUPPORTED if all fragments in any single inner list are obtained."
    )
    # New field: Defines how this nugget, once SUPPORTED, can become CORROBORATED.
    conditions_for_corroboration: List[CorroborationCondition] = Field(
        default_factory=list,
        description="A list of conditions. If this nugget is SUPPORTED and ANY one of these CorroborationCondition is met, its status can be upgraded to CORROBORATED."
    )
    # Optional: Link to primary source if heavily tied to one item
    primary_source_evidence_item_id: Optional[str] = Field(
        default=None,
        description="Optional: The ID of the BranchingEvidenceItem that is the predominant source for the fragments establishing this nugget, if applicable."
    )
    # Relationships between nuggets
    requires_nuggets_for_context: List[str] = Field(
        default_factory=list,
        description="List of nugget_ids that must be known (i.e., status is SUPPORTED or CORROBORATED) for this nugget to be fully understood or relevant."
    )
    contradicts_nuggets: List[str] = Field(
        default_factory=list,
        description="List of nugget_ids that logically contradict this one. If both are SUPPORTED, their status might become CONTRADICTED."
    )
    # Tracking the state of this fact
    status: NuggetStatus = Field(
        default=NuggetStatus.UNKNOWN,
        description="The current confirmation status of this nugget/fact."
    )
    # Link back to MMO (useful for generation & validation)
    related_mmo_element_type: Optional[MMOElementType] = Field( # Re-introduce link if needed
        default=None,
        description="Optional: The MMO element type (means, motive, opportunity) this nugget primarily relates to for a specific suspect."
    )
    related_mmo_suspect_name: Optional[str] = Field( # Re-introduce link if needed
        default=None,
        description="Optional: The name of the suspect whose MMO this nugget relates to."
    )
    is_elimination_critical: bool = Field(
        default=False,
        description="True if corroborating or refuting this nugget is essential for eliminating at least one specific suspect."
    )
    is_killer_path_critical: bool = Field(
        default=False,
        description="True if corroborating this nugget is essential for confirming the killer's true path (use sparingly)."
    )
    interpretation_notes_for_ai: Optional[str] = Field( # Renamed for clarity
        default=None,
        description="Optional notes for the generation AI or designer about the fragment's intended meaning, subtlety, or how its atomic_fact_derived is obtained from raw_data_from_evidence."
    )

class BranchingEvidenceItem(BaseModel):
    """Extended evidence item acting as a container for Information Nuggets."""
    evidence_id: str = Field(description="Unique identifier for this evidence item (e.g., 'evi_library_logbook').")
    # Inherited/Reused fields from original EvidenceItem (adjust as needed)
    category: str = Field(description="The type or category (e.g., 'Logbook', 'Personal Letter', 'Security Footage Snippet').")
    full_description: str = Field(
        description="The complete textual or descriptive content of the evidence item as presented to the player (may contain multiple nuggets)."
    )
    discovery_details: Optional[str] = Field(
        default=None, 
        description="Optional details on how or where this item is found (e.g., 'Found under loose floorboard in study', 'Requires solving puzzle box')."
    )
    
    # Links to the atomic information contained within
    contains_nugget_ids: List[str] = Field(
        description="List of nugget_ids embedded within this evidence item's description."
    )

    # --- Potentially Redundant / Handled by Nuggets ---
    # related_suspect_name: Optional[str] = Field(default=None, description="Primary suspect association (now potentially on Nugget).")
    # points_to_mmo_element: Optional[MMOElementType] = Field(default=None, description="Direct MMO link (now potentially on Nugget).")
    # is_red_herring: Optional[bool] = Field(default=None, description="Emerges from nugget relationships and contradictions.")

    # --- Narrative/Gameplay Aspects ---
    is_initially_available: bool = Field(default=True, description="Can this be found from the start, or does it require unlocking?")
    unlocks_evidence_ids: List[str] = Field(
        default_factory=list, 
        description="List of evidence_ids that become discoverable after finding this item."
    )
    required_evidence_ids: List[str] = Field(
        default_factory=list, 
        description="List of evidence_ids that must be found *before* this item can be discovered/accessed."
    )

### 2.3 Example: Fragment, Nugget, and Corroboration Flow

To illustrate how these models interact to build complexity and handle corroboration, let's revisit the scenario involving Amber, Roma, the scream, and their locations, using the refined model structure:

**Revisiting the Role of Nuggets and Corroboration:**

*   **InformationFragment:** Remains the atomic piece derived from a single `BranchingEvidenceItem` (e.g., F1: "Games - Arcade", F6: "Amber - Marble"). Its `atomic_fact_derived` is the simple interpretation (e.g., "The map shows games are in the arcade", "Amber observed marble floors").
*   **InformationNugget:** Represents a significant factual statement or inference (e.g., N1: "Roma was in the Arcade during P2", N2: "Amber was in the Yoga Studio during P2").
    *   It becomes `SUPPORTED` when one of its `established_by_fragment_sets` is fulfilled (e.g., N1 is `SUPPORTED` when F4 "Roma - Games" and F1 "Games - Arcade" are found).
    *   It transitions to `CORROBORATED` when one of its `conditions_for_corroboration` is met.
*   **CorroborationCondition:** This is where the synthesis happens. It defines the wider context needed to lock in a `SUPPORTED` nugget. Crucially, it can require:
    *   Other specific nuggets to be at least `SUPPORTED`.
    *   Specific linking fragments that might not have formed their own nuggets because their primary purpose is to connect other pieces.

**Applying this to the Example (Focusing on Corroboration):**

Let's define the fragments first (assuming they are derived from Map, Roma's Notes, Amber's Notes evidence items):
*   `F1`: (Evidence: Map) `raw_data`: "Arcade: Features classic games..." `atomic_fact`: "The Arcade has games."
*   `F2`: (Evidence: Map) `raw_data`: "Yoga Studio: Polished marble floors..." `atomic_fact`: "The Yoga Studio has marble floors."
*   `F3`: (Evidence: Map) `raw_data`: "Floor Plan: Yoga Studio is across the hall from the Arcade." `atomic_fact`: "The Yoga Studio is across the hall from the Arcade."
*   `F4`: (Evidence: Roma's Notes - P2) `raw_data`: "Top 10 score!..." `atomic_fact`: "Roma mentioned achieving a high score (implying game playing)."
*   `F5`: (Evidence: Roma's Notes - P2) `raw_data`: "...I could scream! I will! Lol that felt awesome." `atomic_fact`: "Roma screamed out of joy/excitement."
*   `F6`: (Evidence: Amber's Notes - P1) `raw_data`: "I guess the marble floors are beautiful." `atomic_fact`: "Amber observed marble floors."
*   `F7`: (Evidence: Amber's Notes - P2) `raw_data`: "Did someone just scream? Across the hall...sounded like Roma." `atomic_fact`: "Amber heard a scream, likely Roma's, from across the hall."

Now, let's define the Nuggets and their Corroboration Conditions:

*   **N1:** `nugget_id`: "nug_roma_arcade_p2", `description`: "Roma was in the Arcade during Phase 2."
    *   `established_by_fragment_sets`: \[ \["F4_id", "F1_id"] ]
    *   `conditions_for_corroboration`: \[
        *   `CorroborationCondition(`
            *   `required_supporting_nugget_ids`: \["nug_amber_yoga_p2"],
            *   `required_linking_fragment_ids`: \["F3_id", "F5_id", "F7_id"],
            *   `condition_description`: "Roma's presence in the arcade is corroborated when Amber's location is established, the map confirms proximity, and their respective accounts of the scream align."
        *   `)`
        *]
    *   `is_elimination_critical`: True # Assuming this is key for Roma's alibi.

*   **N2:** `nugget_id`: "nug_amber_yoga_p2", `description`: "Amber was in the Yoga Studio during Phase 2."
    *   `established_by_fragment_sets`: \[ \["F6_id", "F2_id"] ]
    *   `conditions_for_corroboration`: \[
        *   `CorroborationCondition(`
            *   `required_supporting_nugget_ids`: \["nug_roma_arcade_p2"],
            *   `required_linking_fragment_ids`: \["F3_id", "F5_id", "F7_id"],
            *   `condition_description`: "Amber's presence in the yoga studio is corroborated when Roma's location is established, the map confirms proximity, and their respective accounts of the scream align."
        *   `)`
        *]
    *   `is_elimination_critical`: True # Assuming this is key for Amber's alibi.

**Why this works and addresses the nuances:**

*   **"The scream is not important [on its own]... The scream just helps corroborate it."**
    *   Exactly! In this setup, the fragments F5 ("Roma Screams") and F7 ("Amber Hears Scream Across Hall") don't need to form their own independent "Scream Event Nugget". Their crucial role is defined within the `required_linking_fragment_ids` of the `CorroborationCondition` for the location nuggets (N1 and N2). They act as the "glue" or connecting tissue.
*   **Distinguishing Important Facts:**
    *   The *importance* of a nugget (like N1 and N2 being key location facts) can be flagged using the `is_elimination_critical` or `is_killer_path_critical` boolean fields on the `InformationNugget` itself.
    *   The "scream fragments" (F5, F7), while vital for the act of corroboration, might not directly establish facts marked as critical on their own.
*   **Hierarchy and Flow:**
    1.  **Fragments** are derived directly from `BranchingEvidenceItems`.
    2.  Specific sets of **Fragments** establish **Nuggets** (status becomes `SUPPORTED`).
    3.  A broader context, defined by the **CorroborationCondition** (requiring other `SUPPORTED` **Nuggets** + specific linking **Fragments**), allows the status of key **Nuggets** to be upgraded to `CORROBORATED`.

This structure allows for the representation of complex, multi-faceted evidence relationships where individual pieces gain significance only in combination with others, directly supporting the goal of an elimination-focused puzzle.

## 3. Agent Logic & Responsibilities

This section outlines the proposed AI agents (or distinct agentic roles) responsible for generating the branching evidence mystery. These agents operate sequentially, each building upon the `BranchingCaseContext` data object. The orchestration should support iterative refinement based on validation checks, particularly from the `MasterCoherenceAgent`.

### 3.1. NarrativeRefinementAgent

*   **Purpose:** To take a foundational case (with a selected killer and basic MMOs) and enrich/refine the narrative elements specifically to support a complex, branching evidence structure suitable for elimination-based gameplay.
*   **Inputs:**
    *   Initial `BranchingCaseContext` (potentially from a prior MMO generation phase, including `theme`, `victim`, `suspects` with initial MMOs, and a designated `killer_name`).
*   **Core Processing:**
    1.  **Deepen Killer's Narrative:** Reviews the designated killer's MMO (Means, Motive, Opportunity). Expands and details these elements to provide rich source material for nuanced clues. Ensures the killer's actual path and actions are plausible and can be subtly hinted at.
    2.  **Refine Non-Killer MMOs:** For each non-killer suspect, reviews and potentially refines their MMOs to serve as effective red herrings. This might involve adding details that *seem* incriminating but can be definitively disproven by alibis or other evidence generated later. The goal is to make their elimination a satisfying part of the puzzle.
    3.  **Define Core Murder Action & Temporal Ambiguity:**
        *   Clearly defines the `core_murder_action_description` (e.g., "Victim was poisoned with X via their evening drink").
        *   Establishes the `core_murder_action_stage_window` (the list of `TimeStage` numbers during which the lethal action *could* have plausibly occurred).
        *   Defines the `timeline.settings.temporal_ambiguity_source` (e.g., "Delayed poison effect, symptoms manifested 1-2 stages later," or "Conflicting accounts of a gunshot blur the exact time between Stage 2 and Stage 3").
*   **Outputs:**
    *   Updates to `suspects` list in `BranchingCaseContext` (with refined MMO descriptions).
    *   Populated `core_murder_action_description` and `core_murder_action_stage_window` in `BranchingCaseContext`.
    *   Populated `timeline.settings.temporal_ambiguity_source`, `timeline.settings.num_stages`, `timeline.settings.stage_duration_description`, and `timeline.settings.critical_action_window_stages` in `BranchingCaseContext`.

### 3.2. (Optional) MapGeneratorAgent

*   **Purpose:** To generate or select the physical layout (map) of the mystery setting, defining all locations and their spatial relationships. As noted in Section 2.1, this might initially be a simpler utility, a process of selecting from templates, or involve manual configuration.
*   **Inputs:**
    *   `theme` from `BranchingCaseContext`.
    *   Desired complexity, number of suspects (to gauge map size).
*   **Core Processing:**
    1.  Creates a list of `Location` objects.
    2.  For each `Location`, defines its `name`, `description`, and critically, its relationships with other locations: `connected_location_ids` (standard paths), `secret_connections` (if any), `can_be_seen_from_ids`, and `can_be_heard_from_ids`.
*   **Outputs:**
    *   Populates `timeline.locations` in `BranchingCaseContext` with the list of `Location` objects.

### 3.3. TimelineOrchestratorAgent

*   **Purpose:** To construct the detailed, stage-by-stage timeline of events and character movements, ensuring it's consistent with the narrative, the killer's actions, robust alibis for innocents, and the defined temporal ambiguity.
*   **Inputs:**
    *   `BranchingCaseContext` (containing outputs from `NarrativeRefinementAgent` and `MapGeneratorAgent`, especially refined MMOs, killer's core actions, temporal ambiguity parameters, and the complete `timeline.locations` list).
*   **Core Processing:**
    1.  **Plot Killer's Path:** Maps the killer's movements and key actions across the `TimeStage`s, ensuring consistency with their MMO and the `core_murder_action_description` occurring within the `core_murder_action_stage_window`.
    2.  **Establish Non-Killer Alibis:** For each non-killer, constructs a verifiable alibi for the *entire duration* of the `critical_action_window_stages`. These alibis should be strong enough to eventually lead to their elimination when proven.
    3.  **Detail Character Movements:** For all characters (killer and non-killers), determines their location (`CharacterLocationStage`) for each `TimeStage` in the mystery. These movements should be logical given the map and narrative.
    4.  **Generate Key Timeline Events:** Creates `TimelineEvent` objects for significant occurrences (e.g., arguments, discoveries, sounds heard, power outages) that support the plot, alibis, red herrings, or contribute to the temporal ambiguity. These events are tied to specific stages and locations.
*   **Outputs:**
    *   Populates `timeline.events` (list of `TimelineEvent`) in `BranchingCaseContext`.
    *   Populates `timeline.character_movements` (list of `CharacterLocationStage`) in `BranchingCaseContext`.

### 3.4. InformationBlueprintAgent

*   **Purpose:** To translate the narrative, timeline, and alibi requirements into a logical "blueprint" of information that players must uncover. This involves designing the core facts (`InformationNuggets`), the atomic pieces of data that form them (`InformationFragments`), and the conditions for their corroboration. This agent is the primary designer of the "puzzle" aspect.
*   **Inputs:**
    *   `BranchingCaseContext` (with complete outputs from `NarrativeRefinementAgent`, `MapGeneratorAgent`, and `TimelineOrchestratorAgent` – essentially the full story and timeline).
*   **Core Processing:**
    1.  **Identify Critical Nuggets:** Based on the timeline, alibis, and killer's path, defines the set of `InformationNugget` objects representing key facts. These include:
        *   Nuggets that confirm parts of the killer's means, motive, or opportunity (subtly).
        *   Nuggets that establish irrefutable parts of each non-killer's alibi.
        *   Nuggets that provide essential context or form believable red herrings.
    2.  **Design Fragments:** For each `InformationNugget`, determines the set(s) of `InformationFragment` objects whose `atomic_fact_derived` values, when combined, will establish that nugget.
    3.  **Define Establishment Logic:** Populates `InformationNugget.established_by_fragment_sets` for each nugget.
    4.  **Design Corroboration:** For key `InformationNuggets` (especially those critical for elimination or understanding the killer's path), designs `CorroborationCondition` objects. This involves specifying which other *nuggets* must be `SUPPORTED` and which *linking fragments* are needed to elevate a nugget's status to `CORROBORATED`.
    5.  **Flag Importance:** Sets `is_elimination_critical` and `is_killer_path_critical` flags on `InformationNugget` objects as appropriate.
    6.  **Initial Status:** Sets all `InformationNugget.status` to `UNKNOWN`.
*   **Outputs:**
    *   Populates `information_nuggets` (list of `InformationNugget` objects) in `BranchingCaseContext`.
    *   Populates `information_fragments` (list of `InformationFragment` objects, with `fragment_id` and `atomic_fact_derived` defined, but `raw_data_from_evidence` and `source_evidence_item_id` will be filled by the `ClueWeavingAgent`) in `BranchingCaseContext`.

### 3.5. ClueWeavingAgent

*   **Purpose:** To take the abstract information blueprint (fragments and nuggets) and instantiate them as concrete, narrative `BranchingEvidenceItem` objects. This agent crafts the actual textual and descriptive content of the clues.
*   **Inputs:**
    *   `BranchingCaseContext` (with complete outputs from `InformationBlueprintAgent`, including the lists of defined `information_nuggets` and `information_fragments`).
*   **Core Processing:**
    1.  **Create Evidence Items:** For logical groupings of `InformationFragments` (often those that would naturally appear together), creates `BranchingEvidenceItem` objects. Determines an appropriate `category` for each item.
    2.  **Generate Raw Data for Fragments:** For each `InformationFragment` that will be part of an evidence item, generates its `raw_data_from_evidence` – the actual text, observation, or detail as it would appear in the evidence item. This `raw_data` must logically lead to the fragment's `atomic_fact_derived`.
    3.  **Compose Evidence Descriptions:** Crafts the `full_description` for each `BranchingEvidenceItem`, skillfully embedding the `raw_data_from_evidence` of its constituent fragments. Also generates `discovery_details` if applicable.
    4.  **Assign Fragment Details:** Sets the `fragment_concealment_type` for each fragment. Provides `interpretation_notes_for_ai` if needed. Links each `InformationFragment` to its `source_evidence_item_id`.
    5.  **Link Evidence to Nuggets:** Populates `BranchingEvidenceItem.contains_nugget_ids` based on the fragments embedded within it. (Though a nugget is established by fragments, this provides a quick lookup from evidence to the high-level facts it contains/contributes to).
*   **Outputs:**
    *   Populates `evidence_items` (list of `BranchingEvidenceItem` objects) in `BranchingCaseContext`.
    *   Completes all fields for `information_fragments` in `BranchingCaseContext` (notably `raw_data_from_evidence` and `source_evidence_item_id`).

### 3.6. EvidenceDistributionAgent

*   **Purpose:** To determine how evidence items become available to the player, managing prerequisites or staged reveals.
*   **Inputs:**
    *   `BranchingCaseContext` (with fully defined `evidence_items`).
*   **Core Processing (MVP):**
    1.  Sets `is_initially_available = True` for all `BranchingEvidenceItem` objects.
    2.  Ensures `unlocks_evidence_ids` and `required_evidence_ids` lists are empty for all items.
*   **Core Processing (Future Enhancements):**
    1.  Strategically sets `is_initially_available` for a subset of evidence.
    2.  Populates `unlocks_evidence_ids` and `required_evidence_ids` to create dependencies and a staged discovery flow, ensuring no dead-ends are created that block access to critical evidence.
*   **Outputs:**
    *   Updates `is_initially_available`, `unlocks_evidence_ids`, and `required_evidence_ids` fields for all `BranchingEvidenceItem` objects in `BranchingCaseContext`.

### 3.7. MasterCoherenceAgent

*   **Purpose:** To perform a final, holistic validation of the entire generated mystery, ensuring logical consistency, solvability according to the design principles, and overall quality.
*   **Inputs:**
    *   The complete `BranchingCaseContext` after all previous agents have run.
*   **Core Processing:**
    1.  **Solvability Check:** Verifies that the mystery is solvable *only* through the process of elimination, guided by corroborated nuggets. Confirms there isn't an overly obvious "smoking gun" for the killer.
    2.  **Alibi Validation:** Ensures that for every non-killer, their alibi (as supported by `CORROBORATED` nuggets) is sound for the entire `critical_action_window_stages` and effectively refutes their MMO.
    3.  **Killer's Path Confirmation:** Checks that the killer's true path and actions are subtly supported by a chain of `CORROBORATED` nuggets.
    4.  **Temporal Ambiguity Maintenance:** Ensures the evidence and timeline maintain the intended temporal ambiguity around the core murder action.
    5.  **No Wasted Evidence/Fragments:** Confirms that all generated `BranchingEvidenceItems` and `InformationFragments` contribute meaningfully to at least one `InformationNugget` or a `CorroborationCondition`.
    6.  **Logical Consistency:** Checks for unintentional contradictions between `CORROBORATED` nuggets.
    7.  **Interconnectivity:** Assesses the degree of interconnectivity between evidence items and nuggets.
*   **Outputs:**
    *   A validation report detailing its findings.
    *   If critical errors or inconsistencies are found, the report should provide actionable feedback to help guide an iteration or re-run of specific preceding agents with modified parameters or constraints.

This concludes the initial draft for Section 3.

## 4. Orchestration Flow

(Section to be developed)

## 5. Core Algorithms & Heuristics (Conceptual)

(Section to be developed)

## 6. Risk & Mitigation Analysis

(Section to be developed) 