"""
Core data models for the Murder Mystery Generation system.

This module defines all the Pydantic models used throughout the application to represent
various components of a murder mystery, including victims, suspects, evidence, and the overall case.
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class VictimProfile(BaseModel):
    """Represents the details of the victim."""

    name: str = Field(description="Full name of the victim.")
    occupation: str = Field(description="The victim's occupation or primary role.")
    personality: str = Field(description="A brief description of the victim's personality traits.")
    cause_of_death: str = Field(description="The determined or apparent cause of death.")
    chosen_cause_of_death_category: Optional[str] = Field(
        default=None,
        description="The specific category of cause of death selected by the agent.",
    )
    chosen_occupation_archetype: Optional[str] = Field(
        default=None,
        description="The specific occupation archetype selected by the agent for the victim.",
    )
    chosen_personality_archetype: Optional[str] = Field(
        default=None,
        description="The specific personality archetype selected by the agent for the victim.",
    )


class SuspectProfile(BaseModel):
    """Defines the profile of a suspect, including their name, description, and relationship to the victim."""

    name: str = Field(description="Full name of the suspect.")
    description: str = Field(description="A brief description of the suspect.")
    relationship_to_victim: str = Field(description="The suspect's relationship to the victim.")
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


class MMO(BaseModel):
    """Represents the Means, Motive, and Opportunity for a suspect."""

    means: str = Field(description="How the suspect could have committed the crime.")
    motive: str = Field(description="Why the suspect might have wanted to commit the crime.")
    opportunity: str = Field(
        description="When and where the suspect could have committed the crime."
    )


class MMOElementType(str, Enum):
    """Enumeration for the types of MMO elements."""

    MEANS = "means"
    MOTIVE = "motive"
    OPPORTUNITY = "opportunity"


class ModifiedMMOElement(BaseModel):
    """Represents a single, modified MMO element for a non-killer suspect."""

    element_type: MMOElementType = Field(
        description="Which MMO element was modified (means, motive, or opportunity)."
    )
    original_element_description: str = Field(
        description="The original description of this MMO element before modification."
    )
    modified_element_description: str = Field(
        description="The new, weakened/invalidated description of this MMO element."
    )
    reason_for_modification: str = Field(
        description="Brief explanation of how or why this element makes them less likely the killer."
    )


class Suspect(BaseModel):
    """Represents a single suspect, including their profile, original MMO, and killer status."""

    profile: SuspectProfile = Field(description="The suspect's profile information.")
    original_mmo: MMO = Field(
        description="The suspect's original, fully plausible Means, Motive, and Opportunity."
    )
    is_killer: bool = Field(
        default=False,
        description="True if this suspect is the designated killer, False otherwise.",
    )
    modified_mmo_elements: List[ModifiedMMOElement] = Field(
        default_factory=list,
        description="A list of MMO elements that were modified for this suspect if they are not the killer. Typically one element.",
    )


class EvidenceItem(BaseModel):
    """Represents a single piece of evidence."""

    description: str = Field(description="A textual description of the evidence item.")
    related_suspect_name: str = Field(
        description="Name of the suspect this evidence primarily relates to."
    )
    points_to_mmo_element: MMOElementType = Field(
        description="Which MMO element of the suspect this evidence supports or alludes to."
    )
    is_red_herring: bool = Field(
        description="True if this evidence is intended to mislead, False if it supports the true killer's narrative."
    )
    connection_explanation: Optional[str] = Field(
        default=None,
        description="Brief explanation of how this evidence links to the suspect's MMO element."
    )
    evidence_category: str = Field(
        description="The type or category of the evidence, e.g., 'Letter', 'Financial Record'."
    )
    narrative_function_description: str = Field(
        description="An explanation of the evidence's intended narrative role, subtlety, or how it functions as a clue or red herring."
    )


class CaseContext(BaseModel):
    """Main data model to hold all generated mystery elements, evolving per epic."""

    theme: str = Field(description="The overall theme or setting of the mystery.")
    thematic_first_names: List[str] = Field(
        default_factory=list,
        description="A list of thematically appropriate first names for the given theme.",
    )
    thematic_last_names: List[str] = Field(
        default_factory=list,
        description="A list of thematically appropriate last names for the given theme.",
    )
    victim: Optional[VictimProfile] = Field(default=None, description="Details of the victim.")
    suspects: List[Suspect] = Field(
        default_factory=list, description="A list of all suspects involved in the case."
    )
    evidence_items: List[EvidenceItem] = Field(
        default_factory=list,
        description="A list of all evidence items generated for the case.",
    )
    author_notes: Optional[str] = Field(
        default=None,
        description="Internal notes or a brief summary of the solution for the author/designer.",
    )

    def get_killer(self) -> Optional[Suspect]:
        """
        Finds and returns the killer from the list of suspects.

        Returns:
            The suspect marked as the killer, or None if no killer is found or no suspects exist.
        """
        if self.suspects:
            for suspect in self.suspects:
                if suspect.is_killer:
                    return suspect
        return None


# Ensure all forward references are resolved if models were in different order or files
# For single file, order usually suffices. If issues, uncomment:
# Suspect.model_rebuild()
# CaseContext.model_rebuild()

# Other models like ModifiedMMOElement, EvidenceItem
# will be added here in later stories as per their definitions in docs/data-models.md
