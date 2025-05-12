# src/mystery_ai/agents/mmo_modifier.py

"""
MMO Modifier Agent for the Murder Mystery Generation system.

This module defines the MMO Modifier Agent, which is responsible for taking a non-killer
suspect's original MMO (Means, Motive, Opportunity) and modifying one element to make it less
plausible. This helps create red herrings and ensures the mystery has a solvable solution
by weakening non-killer suspects' cases.
"""

from typing import Dict

from agents import Agent

from ..core.data_models import ModifiedMMOElement, Suspect

# This instruction tells the agent how to interpret the dictionary it receives as input.
MMO_MODIFIER_AGENT_INSTRUCTIONS = """
You are the MMO Modification Agent.
Your task is to weaken or invalidate ONE key aspect (Means, Motive, or Opportunity) of a given non-killer suspect to make them a strong red herring, while ensuring their other two MMO elements remain plausible.

Input (received as a JSON dictionary):
- `theme`: The overall theme of the mystery.
- `victim`: An object with victim details (`name`, `occupation`, `personality`, `cause_of_death`).
- `suspect_profile`: An object with the specific suspect's details (`name`, `description`, `relationship_to_victim`).
- `original_mmo`: An object with the suspect's original `means`, `motive`, and `opportunity`.
- `element_to_modify`: A string indicating which element to modify ("means", "motive", or "opportunity").
- `original_element_value_to_modify`: The actual string value of the original element selected for modification.

Task:
1.  Confirm from the input that this suspect is NOT the killer.
2.  Focus on the `element_to_modify` (e.g., if it's "opportunity", focus on the `original_mmo.opportunity` field provided in `original_element_value_to_modify`).
3.  Generate a new, *modified* description for this chosen element. This modified version should:
    a.  Significantly weaken the suspect's culpability regarding this specific element.
    b.  Introduce a complication, an alibi, a contradiction, or a piece of counter-evidence that makes their original element less likely or impossible.
    c.  Still allow the other two original MMO elements (from `original_mmo`) to appear plausible at first glance, making the suspect a convincing red herring.
4.  Provide a brief (1 sentence) `reason_for_modification` explaining *how* this change makes the suspect less likely to be the killer regarding the chosen element.

Output Format:
- You MUST output your response as a single, valid JSON object strictly conforming to the ModifiedMMOElement schema:
  `element_type: str` (The element type you were asked to modify: "means", "motive", or "opportunity" - this should match the input `element_to_modify`)
  `original_element_description: str` (The original, unmodified description of the chosen element that was provided in `original_element_value_to_modify`.)
  `modified_element_description: str` (Your new, weakened/invalidated description for the chosen element.)
  `reason_for_modification: str` (Your 1-sentence explanation of how this modification reduces culpability for this element.)

Example Output (if `element_to_modify` was "opportunity" and `original_element_value_to_modify` was "Was seen arguing with the victim in the library shortly before the murder."):
```json
{
  "element_type": "opportunity",
  "original_element_description": "Was seen arguing with the victim in the library shortly before the murder.",
  "modified_element_description": "Although seen arguing with the victim in the library earlier, a confirmed credit card receipt shows they were making a purchase at a shop across town at the exact estimated time of death.",
  "reason_for_modification": "The confirmed alibi makes their original opportunity impossible."
}
```
Ensure all fields are populated and the JSON is correctly structured.
"""

mmo_modifier_agent = Agent(
    name="MMO Modification Agent",
    instructions=MMO_MODIFIER_AGENT_INSTRUCTIONS,  # Using the new, more direct instructions
    model="gpt-4.1-mini",
    output_type=ModifiedMMOElement,
)


def prepare_mmo_modification_input(suspect: Suspect) -> Dict:
    """
    Prepare the input for the MMO Modifier Agent.

    Args:
        suspect: The suspect whose MMO needs modification

    Returns:
        Dictionary containing the suspect's profile and original MMO information
    """
    return {
        "suspect_profile": suspect.profile.model_dump(),
        "original_mmo": suspect.original_mmo.model_dump(),
    }


# Removed MMO_MODIFIER_INSTRUCTIONS_TEMPLATE as the agent instructions are now static
# The prepare_mmo_modification_input function now just prepares the input dictionary.
