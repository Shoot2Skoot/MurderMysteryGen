# src/mystery_ai/agents/evidence_generator.py

from agents import Agent, ModelSettings
from ..core.data_models import CaseContext, Suspect, EvidenceItem, MMOElementType, VictimProfile # For full context
from typing import List, Dict, Any

EVIDENCE_GENERATOR_INSTRUCTIONS_TEMPLATE = """
You are the Evidence Generation Agent.
Your task is to generate a list of 2-3 distinct pieces of evidence for a *specific suspect* based on the case context, their profile, their original MMO, and whether they are the killer (and if not, which MMO element was weakened).

Case Context:
- Theme: {theme}
- Victim Name: {victim_name}
- Victim Occupation: {victim_occupation}

Suspect Details:
- Name: {suspect_name}
- Is Killer: {is_killer}
- Original Means: {original_means}
- Original Motive: {original_motive}
- Original Opportunity: {original_opportunity}
- Modified MMO Element Type (if not killer): {modified_element_type_str}
- Modified MMO Element Description (if not killer): {modified_element_desc_str}
- Reason for Modification (if not killer): {reason_for_modification_str}

Task:
1.  If `Is Killer` is TRUE:
    *   Generate 2-3 pieces of evidence that *directly support* one or more aspects of their `Original Means`, `Original Motive`, or `Original Opportunity`.
    *   Each piece of evidence should be distinct and clearly point towards their guilt.
    *   Mark these evidence items with `is_red_herring: false`.
2.  If `Is Killer` is FALSE:
    *   You are given which element of their original MMO was modified/weakened (`Modified MMO Element Type`) and why (`Reason for Modification`).
    *   Generate 1-2 pieces of "red herring" evidence.
    *   This evidence should *initially appear to support* their `Original Means`, `Original Motive`, or `Original Opportunity` (especially the elements that were *not* weakened), OR it could subtly allude to the *original, unmodified version* of the weakened element, creating misdirection before the true alibi/weakness is found.
    *   The goal is to make them look suspicious at first glance.
    *   Mark these evidence items with `is_red_herring: true`.
3.  For each piece of evidence, provide:
    *   `description`: A textual description of the evidence item.
    *   `related_suspect_name`: (This will be {suspect_name} as you are generating for this specific suspect).
    *   `points_to_mmo_element`: Which element ("means", "motive", or "opportunity") of the suspect this evidence primarily relates to.
    *   `is_red_herring`: Boolean (true if it's a red herring for a non-killer, false if it's true evidence for the killer).
    *   `connection_explanation`: (Optional but helpful) A brief sentence on how this evidence connects to the suspect's MMO element.

Output Format:
- You MUST output your response as a single, valid JSON list of EvidenceItem objects. Each object must conform to the EvidenceItem schema.
  Example fields: `description`, `related_suspect_name`, `points_to_mmo_element`, `is_red_herring`, `connection_explanation`.

Example Output (for a killer):
```json
[
  {{
    "description": "A partially burned love letter from the victim found in the suspect's fireplace, detailing a secret affair.",
    "related_suspect_name": "{suspect_name}",
    "points_to_mmo_element": "motive",
    "is_red_herring": false,
    "connection_explanation": "Suggests a passionate motive related to a secret relationship."
  }},
  {{
    "description": "Security footage showing the suspect near the victim's apartment around the time of death.",
    "related_suspect_name": "{suspect_name}",
    "points_to_mmo_element": "opportunity",
    "is_red_herring": false,
    "connection_explanation": "Places the suspect at the scene providing opportunity."
  }}
]
```
Ensure the output is ONLY the JSON list of evidence items for this one suspect.
"""

# For Story 3.2, defining the agent skeleton.
# Orchestrator will call this for each suspect, building up detailed instructions/input.

evidence_generator_agent = Agent(
    name="Evidence Generation Agent",
    instructions="You will be provided with detailed case and suspect context to generate evidence. Follow instructions precisely.", # Generic, actual instructions built dynamically by orchestrator
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
        # For MVP, assume only one element is modified as per Epic 3 design
        if suspect.modified_mmo_elements[0]:
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