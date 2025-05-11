from pydantic import BaseModel, Field
from typing import List, Optional

class VictimProfile(BaseModel):
    """Represents the details of the victim."""
    name: str = Field(description="Full name of the victim.")
    occupation: str = Field(description="The victim's occupation or primary role.")
    personality: str = Field(description="A brief description of the victim's personality traits.")
    cause_of_death: str = Field(description="The determined or apparent cause of death.")

class SuspectProfile(BaseModel):
    """Represents the profile of a suspect, distinct from their MMO."""
    name: str = Field(description="Full name of the suspect.")
    description: str = Field(description="A brief description of the suspect (e.g., archetype, key characteristics).")
    relationship_to_victim: str = Field(description="The suspect's relationship to the victim.")

class MMO(BaseModel):
    """Represents the Means, Motive, and Opportunity for a suspect."""
    means: str = Field(description="How the suspect could have committed the crime.")
    motive: str = Field(description="Why the suspect might have wanted to commit the crime.")
    opportunity: str = Field(description="When and where the suspect could have committed the crime.")

# Forward reference for Suspect within CaseContext
# We need to define Suspect before CaseContext uses List[Suspect]
# However, Suspect itself might need MMO and SuspectProfile which are defined above.

class Suspect(BaseModel):
    """Represents a single suspect, including their profile and original MMO."""
    profile: SuspectProfile = Field(description="The suspect's profile information.")
    original_mmo: MMO = Field(description="The suspect's original, fully plausible Means, Motive, and Opportunity.")
    is_killer: bool = Field(default=False, description="True if this suspect is the designated killer, False otherwise.")
    # modified_mmo_elements will be added in Epic 3

class CaseContext(BaseModel):
    """Main data model to hold all generated mystery elements, evolving per epic."""
    theme: str = Field(description="The overall theme or setting of the mystery.")
    victim: Optional[VictimProfile] = Field(default=None, description="Details of the victim.")
    suspects: Optional[List[Suspect]] = Field(default_factory=list, description="A list of all suspects involved in the case.")
    # evidence_items: Optional[List['EvidenceItem']] = Field(default_factory=list, description="A list of all evidence items generated for the case.")
    # author_notes: Optional[str] = Field(default=None, description="Internal notes or a brief summary of the solution for the author/designer.")

    def get_killer(self) -> Optional[Suspect]:
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