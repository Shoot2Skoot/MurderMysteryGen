# Mystery.AI - Data Models (MVP)

This document defines the Pydantic data models used within the Mystery.AI system for structuring data passed between agents and for the final JSON output. These models are designed to be compatible with the OpenAI Agents SDK's structured output capabilities and adhere to OpenAI's constraints for `response_format`.

Reference: [OpenAI Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses)

## 1. Core Data Models

The following Pydantic models will be defined in `src/mystery_ai/core/data_models.py`.

### 1.1. `VictimProfile`

Represents the details of the victim.

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class VictimProfile(BaseModel):
    name: str = Field(description="Full name of the victim.")
    occupation: str = Field(description="The victim's occupation or primary role.")
    personality: str = Field(description="A brief description of the victim's personality traits.")
    cause_of_death: str = Field(description="The determined or apparent cause of death.")
```

### 1.2. `MMO` (Means, Motive, Opportunity)

Represents the Means, Motive, and Opportunity for a suspect.

```python
class MMO(BaseModel):
    means: str = Field(description="How the suspect could have committed the crime.")
    motive: str = Field(description="Why the suspect might have wanted to commit the crime.")
    opportunity: str = Field(description="When and where the suspect could have committed the crime.")
```

### 1.3. `SuspectProfile`

Represents the profile of a suspect, distinct from their MMO.

```python
class SuspectProfile(BaseModel):
    name: str = Field(description="Full name of the suspect.")
    description: str = Field(description="A brief description of the suspect (e.g., archetype, key characteristics).")
    relationship_to_victim: str = Field(description="The suspect's relationship to the victim.")
```

### 1.4. `ModifiedMMOElement` (Optional - for storing modified MMO)

Represents a single, modified MMO element for a non-killer suspect.
This is one way to represent the modification; an alternative could be separate optional fields on the `Suspect` model. This nested model approach is cleaner if modifications become more complex.

```python
from enum import Enum

class MMOElementType(str, Enum):
    MEANS = "means"
    MOTIVE = "motive"
    OPPORTUNITY = "opportunity"

class ModifiedMMOElement(BaseModel):
    element_type: MMOElementType = Field(description="Which MMO element was modified (means, motive, or opportunity).")
    original_element_description: str = Field(description="The original description of this MMO element before modification.")
    modified_element_description: str = Field(description="The new, weakened/invalidated description of this MMO element.")
    reason_for_modification: str = Field(description="Brief explanation of how or why this element makes them less likely the killer.")
```

### 1.5. `Suspect`

Represents a single suspect, including their profile, original MMO, killer status, and any modifications to their MMO.

```python
class Suspect(BaseModel):
    profile: SuspectProfile = Field(description="The suspect's profile information.")
    original_mmo: MMO = Field(description="The suspect's original, fully plausible Means, Motive, and Opportunity.")
    is_killer: bool = Field(default=False, description="True if this suspect is the designated killer, False otherwise.")
    modified_mmo_elements: Optional[List[ModifiedMMOElement]] = Field(
        default_factory=list, # Use default_factory for mutable default
        description="A list of MMO elements that were modified for this suspect if they are not the killer. Typically one element."
    )
    # Alternative to ModifiedMMOElement list:
    # modified_means: Optional[str] = Field(default=None, description="Weakened/invalidated means, if applicable.")
    # modified_motive: Optional[str] = Field(default=None, description="Weakened/invalidated motive, if applicable.")
    # modified_opportunity: Optional[str] = Field(default=None, description="Weakened/invalidated opportunity, if applicable.")
```
*Architect Note: Decided to go with `List[ModifiedMMOElement]` for now as it's more structured for potentially multiple modifications or richer modification details in the future, though for MVP only one element is modified. Using `default_factory=list` for the optional list.*

### 1.6. `EvidenceItem`

Represents a single piece of evidence.

```python
class EvidenceItem(BaseModel):
    description: str = Field(description="A textual description of the evidence item.")
    related_suspect_name: str = Field(description="Name of the suspect this evidence primarily relates to.")
    points_to_mmo_element: MMOElementType = Field(description="Which MMO element of the suspect this evidence supports or alludes to.")
    is_red_herring: bool = Field(description="True if this evidence is intended to mislead (typically for non-killers), False if it supports the true killer's narrative.")
    # Optional: How it connects to the MMO element
    connection_explanation: Optional[str] = Field(default=None, description="Brief explanation of how this evidence links to the suspect's MMO element.")
```

### 1.7. `CaseContext` (Root Model)

The main data model that encapsulates the entire generated mystery. This will be the structure of the final JSON output.

```python
class CaseContext(BaseModel):
    theme: str = Field(description="The overall theme or setting of the mystery (e.g., 'Cyberpunk', 'Pirate Ship').")
    victim: VictimProfile = Field(description="Details of the victim.")
    suspects: List[Suspect] = Field(description="A list of all suspects involved in the case.")
    evidence_items: List[EvidenceItem] = Field(description="A list of all evidence items generated for the case.")
    # Optional: Overall case summary or solution notes for the author
    author_notes: Optional[str] = Field(default=None, description="Internal notes or a brief summary of the solution for the author/designer.")

    # It's good practice to provide a method to get the actual killer
    def get_killer(self) -> Optional[Suspect]:
        for suspect in self.suspects:
            if suspect.is_killer:
                return suspect
        return None
```

## 2. JSON Schema Generation

The JSON schema for the `CaseContext` model can be generated programmatically using Pydantic's built-in capabilities:

```python
# In a utility script or for documentation purposes:
# from .data_models import CaseContext # Assuming relative import
# print(CaseContext.model_json_schema(indent=2))
```

This schema will be the definitive structure for the output `mystery_case.json` file. It will also be used to validate the output during testing (as per Story 4.3 in `epic4.md`).

## 3. Adherence to OpenAI Structured Output Constraints

All models defined above use only supported Pydantic field types for structured outputs:
- Primitives: `str`, `bool`
- `Enum` (e.g., `MMOElementType`)
- `List` of primitives or `List` of nested Pydantic models.
- Nested Pydantic models (e.g., `VictimProfile` within `CaseContext`, `SuspectProfile` and `MMO` within `Suspect`).
- `Optional` fields are used appropriately.

Direct `dict` types or complex `Union` types that are problematic for LLM structured output have been avoided in favor of nested Pydantic models or more specific typing. 