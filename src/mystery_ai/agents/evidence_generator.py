# src/mystery_ai/agents/evidence_generator.py

from agents import Agent, ModelSettings
from ..core.data_models import CaseContext, Suspect, EvidenceItem, MMOElementType, VictimProfile # For full context
from typing import List, Dict, Any

EVIDENCE_GENERATOR_AGENT_INSTRUCTIONS = """
You are the Evidence Generation Agent.
Your task is to generate a list of 1-3 distinct pieces of evidence for a *specific suspect* based on the detailed case and suspect context provided in your input.

Input (received as a JSON dictionary):
- `theme`: The overall theme of the mystery.
- `victim_name`: Name of the victim.
- `victim_occupation`: Occupation of the victim.
- `suspect_name`: Name of the specific suspect for whom to generate evidence.
- `is_killer`: Boolean, true if this suspect is the killer, false otherwise.
- `original_means`: The suspect's original means.
- `original_motive`: The suspect's original motive.
- `original_opportunity`: The suspect's original opportunity.
- `modified_element_type_str`: (String, e.g., "means", "motive", "opportunity", or "N/A" if killer) The MMO element that was weakened if the suspect is NOT the killer.
- `modified_element_desc_str`: (String, or "N/A") The description of how the element was weakened.
- `reason_for_modification_str`: (String, or "N/A") The reason the element was weakened.

Task:
1.  Analyze all provided input details for the specific suspect.
2.  If `is_killer` is TRUE:
    *   Generate 2-3 pieces of evidence that *directly support* one or more aspects of their `original_means`, `original_motive`, or `original_opportunity`.
    *   Each piece of evidence should be distinct and clearly point towards their guilt.
    *   Mark these evidence items with `is_red_herring: false`.
3.  If `is_killer` is FALSE:
    *   Consider the `modified_element_type_str` and `reason_for_modification_str` to understand how this suspect was made a red herring.
    *   Generate 1-2 pieces of "red herring" evidence.
    *   This evidence should *initially appear to support* their `original_means`, `original_motive`, or `original_opportunity` (especially the elements that were *not* weakened), OR it could subtly allude to the *original, unmodified version* of the weakened element, creating misdirection.
    *   The goal is to make them look suspicious at first glance.
    *   Mark these evidence items with `is_red_herring: true`.
4.  For each piece of evidence, provide all fields required by the EvidenceItem schema.

Output Format:
- You MUST output your response as a single, valid JSON list of EvidenceItem objects. Each object must conform to the EvidenceItem schema:
  `description: str`
  `related_suspect_name: str` (This MUST be the `suspect_name` from your input.)
  `points_to_mmo_element: str` (Value must be one of "means", "motive", "opportunity")
  `is_red_herring: bool`
  `connection_explanation: str` (Optional but highly recommended; briefly explain how this evidence links to the suspect and their MMO element.)

Example Output (for a killer suspect named 'Silas Blackwood'):
```json
[
  {{
    "description": "A threatening note written on Silas Blackwood's company letterhead found in the victim's safe.",
    "related_suspect_name": "Silas Blackwood",
    "points_to_mmo_element": "motive",
    "is_red_herring": false,
    "connection_explanation": "The note indicates a strong conflict and motive for Silas Blackwood."
  }}
]
```
Ensure the output is ONLY the JSON list of evidence items for this one suspect.
"""

# For Story 3.2, defining the agent skeleton.
# Orchestrator will call this for each suspect, building up detailed instructions/input.

evidence_generator_agent = Agent(
    name="Evidence Generation Agent",
    instructions=EVIDENCE_GENERATOR_AGENT_INSTRUCTIONS,
    model="gpt-4.1-mini", 
    output_type=List[EvidenceItem]
)

# Helper function to prepare input for the EvidenceGenerationAgent for a single suspect
def prepare_evidence_generation_input(
    case_context: CaseContext, # Contains theme and victim
    suspect: Suspect # The specific suspect (with killer status and modified MMO if any)
) -> Dict[str, Any]:
    
    modified_element_type_str = "N/A"
    modified_element_desc_str = "N/A"
    reason_for_modification_str = "N/A"

    if not suspect.is_killer and suspect.modified_mmo_elements:
        # For MVP, assume only one element is modified
        if suspect.modified_mmo_elements: # Check if list is not empty
            mod_element = suspect.modified_mmo_elements[0]
            modified_element_type_str = mod_element.element_type.value
            modified_element_desc_str = mod_element.modified_element_description
            reason_for_modification_str = mod_element.reason_for_modification

    input_dict = {
        "theme": case_context.theme,
        "victim_name": case_context.victim.name if case_context.victim else "N/A",
        "victim_occupation": case_context.victim.occupation if case_context.victim else "N/A",
        "suspect_name": suspect.profile.name,
        "is_killer": suspect.is_killer,
        "original_means": suspect.original_mmo.means,
        "original_motive": suspect.original_mmo.motive,
        "original_opportunity": suspect.original_mmo.opportunity,
        "modified_element_type_str": modified_element_type_str,
        "modified_element_desc_str": modified_element_desc_str,
        "reason_for_modification_str": reason_for_modification_str
    }
    return input_dict
    
    # The instructions for the agent will be dynamically formatted with these details
    # by the orchestrator, similar to MMOModificationAgent, or this dict is passed as input
    # with more generic agent instructions.
    # For consistency, let's assume the orchestrator will pass this dict as input to the agent. 