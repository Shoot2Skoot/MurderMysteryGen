from pydantic import BaseModel, Field
from typing import List, Optional # Though List & Optional not used in this very first model

class VictimProfile(BaseModel):
    """Represents the details of the victim."""
    name: str = Field(description="Full name of the victim.")
    occupation: str = Field(description="The victim's occupation or primary role.")
    personality: str = Field(description="A brief description of the victim's personality traits.")
    cause_of_death: str = Field(description="The determined or apparent cause of death.")

# Other models like CaseContext, MMO, SuspectProfile, Suspect, EvidenceItem 
# will be added here in later stories as per their definitions in docs/data-models.md 