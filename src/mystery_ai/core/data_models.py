from pydantic import BaseModel, Field
from typing import List, Optional # Though List & Optional not used in this very first model

class VictimProfile(BaseModel):
    """Represents the details of the victim."""
    name: str = Field(description="Full name of the victim.")
    occupation: str = Field(description="The victim's occupation or primary role.")
    personality: str = Field(description="A brief description of the victim's personality traits.")
    cause_of_death: str = Field(description="The determined or apparent cause of death.")

class CaseContext(BaseModel):
    """Main data model to hold all generated mystery elements, evolving per epic."""
    theme: str = Field(description="The overall theme or setting of the mystery.")
    victim: Optional[VictimProfile] = Field(default=None, description="Details of the victim.")
    # suspects: Optional[List['Suspect']] = Field(default_factory=list, description="A list of all suspects involved in the case.")
    # evidence_items: Optional[List['EvidenceItem']] = Field(default_factory=list, description="A list of all evidence items generated for the case.")
    # author_notes: Optional[str] = Field(default=None, description="Internal notes or a brief summary of the solution for the author/designer.")

    # Forward references for models to be defined later (Suspect, EvidenceItem)
    # To handle these, Pydantic models can call .model_rebuild() after all models are defined,
    # or ensure definition order, or use string type hints if they are in different modules initially.
    # For now, keeping them commented out as they are for later epics.

# Other models like MMO, SuspectProfile, Suspect, EvidenceItem 
# will be added here in later stories as per their definitions in docs/data-models.md 