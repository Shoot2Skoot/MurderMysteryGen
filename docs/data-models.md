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
from enum import Enum

class VictimProfile(BaseModel):
    """Represents the details of the victim."""
    name: str = Field(description="Full name of the victim.")
    occupation: str = Field(description="The victim's occupation or primary role.")
    personality: str = Field(description="A brief description of the victim's personality traits.")
    cause_of_death: str = Field(description="The determined or apparent cause of death.")
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
    """Represents the profile of a suspect, distinct from their MMO."""
    name: str = Field(description="Full name of the suspect.")
    description: str = Field(description="A brief description of the suspect (e.g., archetype, key characteristics).")
    relationship_to_victim: str = Field(description="The suspect's relationship to the victim.")
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
    evidence_category: str = Field(description="The type or category of the evidence, e.g., 'Letter', 'Financial Record'.")
    narrative_function_description: str = Field(description="An explanation of the evidence's intended narrative role, subtlety, or how it functions as a clue or red herring.")
```

### 1.8. `CaseContext` (Root Model)

The main data model that encapsulates the entire generated mystery. This will be the structure of the final JSON output.

```python
class CaseContext(BaseModel):
    """Main data model to hold all generated mystery elements, evolving per epic."""
    theme: str = Field(description="The overall theme or setting of the mystery.")
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

## 2. CaseContext JSON Schema

This is the JSON schema for the `CaseContext` Pydantic model, which defines the structure of the output `mystery_case.json` file.
It is generated by `CaseContext.model_json_schema()`.

```json
{
  "$defs": {
    "EvidenceItem": {
      "description": "Represents a single piece of evidence.",
      "properties": {
        "description": {
          "description": "A textual description of the evidence item.",
          "title": "Description",
          "type": "string"
        },
        "related_suspect_name": {
          "description": "Name of the suspect this evidence primarily relates to.",
          "title": "Related Suspect Name",
          "type": "string"
        },
        "points_to_mmo_element": {
          "$ref": "#/$defs/MMOElementType",
          "description": "Which MMO element of the suspect this evidence supports or alludes to."
        },
        "is_red_herring": {
          "description": "True if this evidence is intended to mislead, False if it supports the true killer's narrative.",
          "title": "Is Red Herring",
          "type": "boolean"
        },
        "connection_explanation": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "description": "Brief explanation of how this evidence links to the suspect's MMO element.",
          "title": "Connection Explanation"
        },
        "evidence_category": {
          "description": "The type or category of the evidence, e.g., 'Letter', 'Financial Record'.",
          "title": "Evidence Category",
          "type": "string"
        },
        "narrative_function_description": {
          "description": "An explanation of the evidence's intended narrative role, subtlety, or how it functions as a clue or red herring.",
          "title": "Narrative Function Description",
          "type": "string"
        }
      },
      "required": [
        "description",
        "related_suspect_name",
        "points_to_mmo_element",
        "is_red_herring",
        "evidence_category",
        "narrative_function_description"
      ],
      "title": "EvidenceItem",
      "type": "object"
    },
    "MMO": {
      "description": "Represents the Means, Motive, and Opportunity for a suspect.",
      "properties": {
        "means": {
          "description": "How the suspect could have committed the crime.",
          "title": "Means",
          "type": "string"
        },
        "motive": {
          "description": "Why the suspect might have wanted to commit the crime.",
          "title": "Motive",
          "type": "string"
        },
        "opportunity": {
          "description": "When and where the suspect could have committed the crime.",
          "title": "Opportunity",
          "type": "string"
        }
      },
      "required": [
        "means",
        "motive",
        "opportunity"
      ],
      "title": "MMO",
      "type": "object"
    },
    "MMOElementType": {
      "description": "Enumeration for the types of MMO elements.",
      "enum": [
        "means",
        "motive",
        "opportunity"
      ],
      "title": "MMOElementType",
      "type": "string"
    },
    "ModifiedMMOElement": {
      "description": "Represents a single, modified MMO element for a non-killer suspect.",
      "properties": {
        "element_type": {
          "$ref": "#/$defs/MMOElementType",
          "description": "Which MMO element was modified (means, motive, or opportunity)."
        },
        "original_element_description": {
          "description": "The original description of this MMO element before modification.",
          "title": "Original Element Description",
          "type": "string"
        },
        "modified_element_description": {
          "description": "The new, weakened/invalidated description of this MMO element.",
          "title": "Modified Element Description",
          "type": "string"
        },
        "reason_for_modification": {
          "description": "Brief explanation of how or why this element makes them less likely the killer.",
          "title": "Reason For Modification",
          "type": "string"
        }
      },
      "required": [
        "element_type",
        "original_element_description",
        "modified_element_description",
        "reason_for_modification"
      ],
      "title": "ModifiedMMOElement",
      "type": "object"
    },
    "Suspect": {
      "description": "Represents a single suspect, including their profile, original MMO, and killer status.",
      "properties": {
        "profile": {
          "$ref": "#/$defs/SuspectProfile",
          "description": "The suspect's profile information."
        },
        "original_mmo": {
          "$ref": "#/$defs/MMO",
          "description": "The suspect's original, fully plausible Means, Motive, and Opportunity."
        },
        "is_killer": {
          "default": false,
          "description": "True if this suspect is the designated killer, False otherwise.",
          "title": "Is Killer",
          "type": "boolean"
        },
        "modified_mmo_elements": {
          "description": "A list of MMO elements that were modified for this suspect if they are not the killer. Typically one element.",
          "items": {
            "$ref": "#/$defs/ModifiedMMOElement"
          },
          "title": "Modified Mmo Elements",
          "type": "array"
        }
      },
      "required": [
        "profile",
        "original_mmo"
      ],
      "title": "Suspect",
      "type": "object"
    },
    "SuspectProfile": {
      "description": "Represents the profile of a suspect, distinct from their MMO.",
      "properties": {
        "name": {
          "description": "Full name of the suspect.",
          "title": "Name",
          "type": "string"
        },
        "description": {
          "description": "A brief description of the suspect (e.g., archetype, key characteristics).",
          "title": "Description",
          "type": "string"
        },
        "relationship_to_victim": {
          "description": "The suspect's relationship to the victim.",
          "title": "Relationship To Victim",
          "type": "string"
        }
      },
      "required": [
        "name",
        "description",
        "relationship_to_victim"
      ],
      "title": "SuspectProfile",
      "type": "object"
    },
    "VictimProfile": {
      "description": "Represents the details of the victim.",
      "properties": {
        "name": {
          "description": "Full name of the victim.",
          "title": "Name",
          "type": "string"
        },
        "occupation": {
          "description": "The victim's occupation or primary role.",
          "title": "Occupation",
          "type": "string"
        },
        "personality": {
          "description": "A brief description of the victim's personality traits.",
          "title": "Personality",
          "type": "string"
        },
        "cause_of_death": {
          "description": "The determined or apparent cause of death.",
          "title": "Cause Of Death",
          "type": "string"
        }
      },
      "required": [
        "name",
        "occupation",
        "personality",
        "cause_of_death"
      ],
      "title": "VictimProfile",
      "type": "object"
    }
  },
  "description": "Main data model to hold all generated mystery elements, evolving per epic.",
  "properties": {
    "theme": {
      "description": "The overall theme or setting of the mystery.",
      "title": "Theme",
      "type": "string"
    },
    "victim": {
      "anyOf": [
        {
          "$ref": "#/$defs/VictimProfile"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Details of the victim."
    },
    "suspects": {
      "description": "A list of all suspects involved in the case.",
      "items": {
        "$ref": "#/$defs/Suspect"
      },
      "title": "Suspects",
      "type": "array"
    },
    "evidence_items": {
      "description": "A list of all evidence items generated for the case.",
      "items": {
        "$ref": "#/$defs/EvidenceItem"
      },
      "title": "Evidence Items",
      "type": "array"
    },
    "author_notes": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Internal notes or a brief summary of the solution for the author/designer.",
      "title": "Author Notes"
    }
  },
  "required": [
    "theme"
  ],
  "title": "CaseContext",
  "type": "object"
}
```

## 3. Adherence to OpenAI Structured Output Constraints

All models defined above use only supported Pydantic field types for structured outputs:
- Primitives: `str`, `bool`
- `Enum` (e.g., `MMOElementType`)
- `List` of primitives or `List` of nested Pydantic models.
- Nested Pydantic models (e.g., `VictimProfile` within `CaseContext`, `SuspectProfile` and `MMO` within `Suspect`).
- `Optional` fields are used appropriately.

Direct `dict` types or complex `Union` types that are problematic for LLM structured output have been avoided in favor of nested Pydantic models or more specific typing. 