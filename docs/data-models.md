# Mystery.AI - Data Models (MVP)

This document defines the Pydantic data models used within the Mystery.AI system for structuring data passed between agents and for the final JSON output. These models are designed to be compatible with the OpenAI Agents SDK's structured output capabilities and adhere to OpenAI's constraints for `response_format`.

Reference: [OpenAI Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses)

## 1. Core Data Models (Foundational System)

The following Pydantic models will be defined in `src/mystery_ai/core/data_models.py`.

### 1.1. `VictimProfile`

Represents the details of the victim.

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class VictimProfile(BaseModel):
    """Represents the details of the victim."""
    name: str = Field(description="Full name of the victim.")
    occupation: str = Field(description="The victim's occupation or primary role.")
    personality: str = Field(description="A brief description of the victim's personality traits.")
    cause_of_death: str = Field(description="The determined or apparent cause of death.")
    # Fields from Story 5.4
    chosen_cause_of_death_category: Optional[str] = Field(
        default=None,
        description="The specific category of cause of death selected by the agent."
    )
    chosen_occupation_archetype: Optional[str] = Field(
        default=None,
        description="The specific occupation archetype selected by the agent for the victim."
    )
    chosen_personality_archetype: Optional[str] = Field(
        default=None,
        description="The specific personality archetype selected by the agent for the victim."
    )
```

### 1.2. `MMO` (Means, Motive, Opportunity)

Represents the Means, Motive, and Opportunity for a suspect.

```python
class MMO(BaseModel):
    """Represents the Means, Motive, and Opportunity for a suspect."""
    means: str = Field(description="How the suspect could have committed the crime.")
    motive: str = Field(description="Why the suspect might have wanted to commit the crime.")
    opportunity: str = Field(description="When and where the suspect could have committed the crime.")
```

### 1.3. `SuspectProfile`

Represents the profile of a suspect, distinct from their MMO.

```python
class SuspectProfile(BaseModel):
    """Defines the profile of a suspect, including their name, description, and relationship to the victim."""
    name: str = Field(description="Full name of the suspect.")
    description: str = Field(description="A brief description of the suspect.")
    relationship_to_victim: str = Field(description="The suspect's relationship to the victim.")
    # Fields from Story 5.4
    chosen_motive_category: Optional[str] = Field(
        default=None,
        description="The specific motive category selected by the agent for this suspect."
    )
    chosen_occupation_archetype: Optional[str] = Field(
        default=None,
        description="The specific occupation archetype selected by the agent for this suspect."
    )
    chosen_personality_archetype: Optional[str] = Field(
        default=None,
        description="The specific personality archetype selected by the agent for this suspect."
    )
```

### 1.4. `MMOElementType`

```python
class MMOElementType(str, Enum):
    """Enumeration for the types of MMO elements."""
    MEANS = "means"
    MOTIVE = "motive"
    OPPORTUNITY = "opportunity"
```

### 1.5. `ModifiedMMOElement`

Represents a single, modified MMO element for a non-killer suspect.

```python
class ModifiedMMOElement(BaseModel):
    """Represents a single, modified MMO element for a non-killer suspect."""
    element_type: MMOElementType = Field(description="Which MMO element was modified (means, motive, or opportunity).")
    original_element_description: str = Field(description="The original description of this MMO element before modification.")
    modified_element_description: str = Field(description="The new, weakened/invalidated description of this MMO element.")
    reason_for_modification: str = Field(description="Brief explanation of how or why this element makes them less likely the killer.")
```

### 1.6. `Suspect`

Represents a single suspect, including their profile, original MMO, and killer status.

```python
class Suspect(BaseModel):
    """Represents a single suspect, including their profile, original MMO, and killer status."""
    profile: SuspectProfile = Field(description="The suspect's profile information.")
    original_mmo: MMO = Field(description="The suspect's original, fully plausible Means, Motive, and Opportunity.")
    is_killer: bool = Field(default=False, description="True if this suspect is the designated killer, False otherwise.")
    modified_mmo_elements: List[ModifiedMMOElement] = Field(
        default_factory=list, 
        description="A list of MMO elements that were modified for this suspect if they are not the killer. Typically one element."
    )
```

### 1.7. `EvidenceItem`

Represents a single piece of evidence.

```python
class EvidenceItem(BaseModel):
    """Represents a single piece of evidence."""
    description: str = Field(description="A textual description of the evidence item.")
    related_suspect_name: str = Field(description="Name of the suspect this evidence primarily relates to.")
    points_to_mmo_element: MMOElementType = Field(description="Which MMO element of the suspect this evidence supports or alludes to.")
    is_red_herring: bool = Field(description="True if this evidence is intended to mislead, False if it supports the true killer's narrative.")
    connection_explanation: Optional[str] = Field(default=None, description="Brief explanation of how this evidence links to the suspect's MMO element.")
    # Fields from Story 7.2
    evidence_category: str = Field(description="The type or category of the evidence, e.g., 'Letter', 'Financial Record'.")
    narrative_function_description: str = Field(description="An explanation of the evidence's intended narrative role, subtlety, or how it functions as a clue or red herring.")
```

### 1.8. `CaseContext` (Root Model)

The main data model that encapsulates the entire generated mystery. This will be the structure of the final JSON output.
It now also includes `thematic_first_names: List[str]` and `thematic_last_names: List[str]` (from Epic 6).

```python
class CaseContext(BaseModel):
    """Main data model to hold all generated mystery elements, evolving per epic."""
    theme: str = Field(description="The overall theme or setting of the mystery.")
    # Fields from Epic 6
    thematic_first_names: List[str] = Field(
        default_factory=list,
        description="A list of thematically appropriate first names for the given theme.",
    )
    thematic_last_names: List[str] = Field(
        default_factory=list,
        description="A list of thematically appropriate last names for the given theme.",
    )
    victim: Optional[VictimProfile] = Field(default=None, description="Details of the victim.")
    suspects: List[Suspect] = Field(default_factory=list, description="A list of all suspects involved in the case.")
    evidence_items: List[EvidenceItem] = Field(default_factory=list, description="A list of all evidence items generated for the case.")
    author_notes: Optional[str] = Field(default=None, description="Internal notes or a brief summary of the solution for the author/designer.")

    def get_killer(self) -> Optional[Suspect]:
        if self.suspects:
            for suspect in self.suspects:
                if suspect.is_killer:
                    return suspect
        return None
```

## 2. Branching Evidence System Data Models

These Pydantic models are specific to the Branching Evidence System and will reside in `src/mystery_ai/core/data_models_branching.py`. They define the structure for timelines, locations, events, and the interconnected web of evidence fragments and nuggets.

These models are designed to be compatible with the OpenAI Agents SDK's structured output capabilities.

Models are based on `docs/branching-evidence-design.md` Section 2.2.

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

# Re-used or forward-referenced from mystery_ai.core.data_models
# Ensure these are compatible or define specific versions if needed for branching context.
# For MVP, we assume direct compatibility or that they will be loaded into BranchingCaseContext correctly.
# from ..core.data_models import VictimProfile, Suspect, MMOElementType # Example of potential import

# --- Foundational Enums (May be shared or redefined if specific variants needed) ---

class MMOElementType(Enum):
    MEANS = "means"
    MOTIVE = "motive"
    OPPORTUNITY = "opportunity"

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

class CharacterLocationStage(BaseModel):
    """Tracks the confirmed or inferred location of a character during a specific stage."""
    character_name: str = Field(description="Name of the character.")
    stage: int = Field(description="The stage number (1-indexed).")
    location_id: str = Field(description="The location ID where the character is during this stage.")
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

# --- Evidence Graph Component Enums & Models ---

class FragmentConcealmentType(Enum):
    """Describes how an information fragment is presented or obscured within an evidence item."""
    DIRECT_QUOTE = "direct_quote"
    IMPLIED_BY_CONTEXT = "implied_by_context"
    REDACTED_OR_DAMAGED = "redacted_or_damaged"
    CODED_LANGUAGE = "coded_language"
    VISUAL_DETAIL = "visual_detail"

class NuggetStatus(Enum):
    """Represents the current state of belief or confirmation for an Information Nugget."""
    UNKNOWN = "unknown"
    SUPPORTED = "supported"
    REFUTED = "refuted"
    CONTRADICTED = "contradicted"
    CORROBORATED = "corroborated"

class CorroborationCondition(BaseModel):
    """Defines a set of conditions that, if met, can elevate a SUPPORTED InformationNugget to CORROBORATED status."""
    required_supporting_nugget_ids: List[str] = Field(
        default_factory=list,
        description="List of other InformationNugget IDs that must be at least SUPPORTED."
    )
    required_linking_fragment_ids: List[str] = Field(
        default_factory=list,
        description="List of specific InformationFragment IDs that act as crucial links or additional minor confirmations."
    )
    condition_description: Optional[str] = Field(
        default=None,
        description="Optional: Explanation of how these combined elements achieve corroboration for the parent nugget."
    )

class InformationFragment(BaseModel):
    """Represents a fragment of information derived from raw data."""
    fragment_id: str = Field(description="Unique identifier for this fragment.")
    source_evidence_item_id: Optional[str] = Field(default=None, description="ID of the BranchingEvidenceItem this fragment is from.") # Added for completeness
    raw_data_from_evidence: str = Field(description="The raw data from which this fragment is derived.")
    atomic_fact_derived: str = Field(description="The atomic fact derived from the raw data.")
    fragment_concealment_type: Optional[FragmentConcealmentType] = Field(default=None, description="How this fragment is presented/obscured.") # Added
    interpretation_notes_for_ai: Optional[str] = Field(
        default=None,
        description="Optional notes for the generation AI or designer about the fragment's intended meaning or derivation."
    )

class InformationNugget(BaseModel):
    """Represents a core factual statement, inference, or piece of knowledge about the mystery."""
    nugget_id: str = Field(description="Unique identifier for this factual statement.")
    description: str = Field(description="The statement of fact this nugget represents.")
    established_by_fragment_sets: List[List[str]] = Field(
        description="Defines how this nugget is proven. A list of lists (sets) of required fragment_ids. Nugget status becomes SUPPORTED if all fragments in any single inner list are obtained."
    )
    conditions_for_corroboration: List[CorroborationCondition] = Field(
        default_factory=list,
        description="A list of conditions. If this nugget is SUPPORTED and ANY one of these CorroborationCondition is met, its status can be upgraded to CORROBORATED."
    )
    primary_source_evidence_item_id: Optional[str] = Field(
        default=None,
        description="Optional: The ID of the BranchingEvidenceItem that is the predominant source for the fragments establishing this nugget, if applicable."
    )
    requires_nuggets_for_context: List[str] = Field(
        default_factory=list,
        description="List of nugget_ids that must be known (i.e., status is SUPPORTED or CORROBORATED) for this nugget to be fully understood or relevant."
    )
    contradicts_nuggets: List[str] = Field(
        default_factory=list,
        description="List of nugget_ids that logically contradict this one."
    )
    status: NuggetStatus = Field(
        default=NuggetStatus.UNKNOWN,
        description="The current confirmation status of this nugget/fact."
    )
    related_mmo_element_type: Optional[MMOElementType] = Field(
        default=None,
        description="Optional: The MMO element type this nugget primarily relates to for a specific suspect."
    )
    related_mmo_suspect_name: Optional[str] = Field(
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

class BranchingEvidenceItem(BaseModel):
    """Extended evidence item acting as a container for Information Nuggets via its fragments."""
    evidence_id: str = Field(description="Unique identifier for this evidence item.")
    category: str = Field(description="The type or category (e.g., 'Logbook', 'Personal Letter').")
    full_description: str = Field(
        description="The complete textual or descriptive content of the evidence item as presented to the player."
    )
    discovery_details: Optional[str] = Field(
        default=None, 
        description="Optional details on how or where this item is found."
    )
    contains_nugget_ids: List[str] = Field(
        default_factory=list, # Corrected: was just description before
        description="List of nugget_ids primarily established or significantly contributed to by fragments within this evidence item."
    )
    is_initially_available: bool = Field(default=True, description="Can this be found from the start, or does it require unlocking?")
    unlocks_evidence_ids: List[str] = Field(
        default_factory=list, 
        description="List of evidence_ids that become discoverable after finding this item."
    )
    required_evidence_ids: List[str] = Field(
        default_factory=list, 
        description="List of evidence_ids that must be found *before* this item can be discovered/accessed."
    )

# --- Branching Case Context (Root Model for Branching Evidence System) ---

# Forward-declare VictimProfile and Suspect if they are indeed imported from the other module
# For this document, we assume they are available for type hinting.
# If they need to be different for BranchingCaseContext, they should be defined here.
class VictimProfile(BaseModel): # Placeholder for type hinting if not imported
    name: Optional[str] = None
    # ... other fields as in original VictimProfile ...

class Suspect(BaseModel): # Placeholder for type hinting if not imported
    name: Optional[str] = None
    is_killer: Optional[bool] = False
    # ... other fields as in original Suspect ...

class BranchingCaseContext(BaseModel):
    """Top-level container for a mystery generated with branching evidence."""
    theme: str = Field(description="The overall theme or setting of the mystery.")
    victim: Optional[VictimProfile] = Field(default=None, description="Details of the victim. Assumed compatible with foundational VictimProfile.")
    suspects: List[Suspect] = Field(default_factory=list, description="A list of all suspects involved. Assumed compatible with foundational Suspect model.")
    timeline: MysteryTimeline = Field(description="The structured timeline of the mystery.")
    
    evidence_items: List[BranchingEvidenceItem] = Field(
        default_factory=list, 
        description="List of all evidence items (e.g., documents, objects) that players can find."
    )
    information_fragments: List[InformationFragment] = Field(
        default_factory=list, 
        description="List of all atomic facts/observations derived directly from single evidence items."
    )
    information_nuggets: List[InformationNugget] = Field(
        default_factory=list, 
        description="List of all core factual statements or synthesized inferences about the mystery."
    )
    
    core_murder_action_description: Optional[str] = Field(default=None, description="Description of the specific lethal action.")
    core_murder_action_stage_window: Optional[List[int]] = Field(default=None, description="Stage window when lethal action occurred.")

    model_config = {"extra": "ignore"}

## 3. `BranchingCaseContext` JSON Schema

This is the JSON schema for the `BranchingCaseContext` Pydantic model, which defines the structure of the output JSON file from the Branching Evidence System.
It can be generated by `BranchingCaseContext.model_json_schema()`.

**(Note: The JSON schema below should be generated and pasted here after the models are finalized in `src/mystery_ai/core/data_models_branching.py`)**

```json
{
  // Schema to be generated and pasted here
}
```

## 4. Adherence to OpenAI Structured Output Constraints

All models defined above use only supported Pydantic field types for structured outputs:
- Primitives: `str`, `bool`
- `Enum` (e.g., `MMOElementType`)
- `List` of primitives or `List` of nested Pydantic models.
- Nested Pydantic models (e.g., `VictimProfile` within `CaseContext`, `SuspectProfile` and `MMO` within `Suspect`).
- `Optional` fields are used appropriately.

Direct `dict` types or complex `Union` types that are problematic for LLM structured output have been avoided in favor of nested Pydantic models or more specific typing. 