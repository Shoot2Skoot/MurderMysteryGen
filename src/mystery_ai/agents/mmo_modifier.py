# src/mystery_ai/agents/mmo_modifier.py

from agents import Agent, ModelSettings
from ..core.data_models import Suspect, MMOElementType, ModifiedMMOElement, VictimProfile
from typing import List, Dict, Any
import random

MMO_MODIFIER_INSTRUCTIONS_TEMPLATE = """
You are the MMO Modification Agent.
Your task is to weaken or invalidate ONE key aspect (Means, Motive, or Opportunity) of a given non-killer suspect to make them a strong red herring, while ensuring their other two MMO elements remain plausible.

Case Context:
- Theme: {theme}
- Victim Name: {victim_name}
- Victim Occupation: {victim_occupation}
- Victim Personality: {victim_personality}
- Cause of Death: {cause_of_death}

Suspect to Modify:
- Name: {suspect_name}
- Description: {suspect_description}
- Relationship to Victim: {suspect_relationship}
- Original Means: {original_means}
- Original Motive: {original_motive}
- Original Opportunity: {original_opportunity}

Task:
1.  You have been told that **{suspect_name} is NOT the killer.**
2.  Randomly choose ONE of the following elements to modify for {suspect_name}: Means, Motive, or Opportunity. Let's say you chose: **{element_to_modify}**.
3.  Carefully review the chosen Original {element_to_modify}: "{original_element_value}".
4.  Generate a new, *modified* description for this {element_to_modify}. This modified version should:
    a.  Significantly weaken the suspect's culpability regarding this specific element.
    b.  Introduce a complication, an alibi, a contradiction, or a piece of counter-evidence that makes their original {element_to_modify} less likely or impossible.
    c.  Still allow the other two original MMO elements to appear plausible at first glance, making the suspect a convincing red herring.
5.  Provide a brief (1 sentence) `reason_for_modification` explaining *how* this change makes the suspect less likely to be the killer regarding the chosen element.

Output Format:
- You MUST output your response as a single, valid JSON object strictly conforming to the ModifiedMMOElement schema:
  `element_type: str` (The element you chose to modify: "means", "motive", or "opportunity")
  `original_element_description: str` (The original, unmodified description of the chosen element you were given.)
  `modified_element_description: str` (Your new, weakened/invalidated description for the chosen element.)
  `reason_for_modification: str` (Your 1-sentence explanation of how this modification reduces culpability for this element.)

Example (if you chose to modify 'Opportunity'):
```json
{{
  "element_type": "opportunity",
  "original_element_description": "Was seen arguing with the victim in the library shortly before the murder.",
  "modified_element_description": "Although seen arguing with the victim in the library earlier, a confirmed credit card receipt shows they were making a purchase at a shop across town at the exact estimated time of death.",
  "reason_for_modification": "The confirmed alibi makes their original opportunity impossible."
}}
```
Ensure all fields are populated and the JSON is correctly structured.
"""

# For Story 3.1, we are defining the agent skeleton.
# The actual implementation will involve the orchestrator preparing the detailed prompt.

mmo_modifier_agent = Agent(
    name="MMO Modification Agent",
    instructions="You will be provided with detailed instructions for modifying a suspect's MMO. Follow them precisely.", # Placeholder, actual instructions built dynamically
    model="gpt-4.1-mini",
    output_type=ModifiedMMOElement 
)

# Helper function to choose which element to modify and prepare detailed instructions
# This will be called by the orchestrator for each non-killer suspect.

def prepare_mmo_modification_input_and_instructions(
    theme: str, 
    victim: VictimProfile, 
    suspect: Suspect
) -> tuple[Dict[str, Any], str]:
    
    elements = ["means", "motive", "opportunity"]
    element_to_modify_str = random.choice(elements)
    
    original_value = ""
    if element_to_modify_str == "means":
        original_value = suspect.original_mmo.means
    elif element_to_modify_str == "motive":
        original_value = suspect.original_mmo.motive
    else: # opportunity
        original_value = suspect.original_mmo.opportunity

    # Dynamic instructions using the template
    # (This assumes the LLM can handle a fairly long prompt with filled-in details effectively)
    # An alternative is to make the input to the agent more structured (a dict with all these fields)
    # and the instructions more generic, telling it to use fields from the input dict.
    # For now, dynamic instruction string is fine for an agent expecting a ModifiedMMOElement output.
    
    formatted_instructions = MMO_MODIFIER_INSTRUCTIONS_TEMPLATE.format(
        theme=theme,
        victim_name=victim.name,
        victim_occupation=victim.occupation,
        victim_personality=victim.personality,
        cause_of_death=victim.cause_of_death,
        suspect_name=suspect.profile.name,
        suspect_description=suspect.profile.description,
        suspect_relationship=suspect.profile.relationship_to_victim,
        original_means=suspect.original_mmo.means,
        original_motive=suspect.original_mmo.motive,
        original_opportunity=suspect.original_mmo.opportunity,
        element_to_modify=element_to_modify_str.upper(),
        original_element_value=original_value
    )
    
    # The input to the mmo_modifier_agent itself can be minimal if instructions are this detailed.
    # Or, we could pass the structured data and have simpler instructions telling the agent to use that data.
    # For an agent with output_type, the input is often just the core data it needs to transform.
    # Here, the detailed instructions *become* the main input content processed by the LLM.
    # The agent.instructions will be overridden by this specific formatted_instructions when run.
    # For now, we'll let the orchestrator pass the formatted_instructions as the agent's runtime instructions.
    # Alternatively, the `input` to the agent could be a dictionary of all these fields,
    # and the agent's static instructions tell it to use these fields.
    # Let's plan for the orchestrator to update the agent's instructions for the run.
    # The `Runner.run_sync` does not directly take new instructions for a run.
    # So, the best way is to have the mmo_modifier_agent's instructions be generic, 
    # and the `input` to the agent is the detailed context.

    # Revised approach: Agent has generic instructions, input is the detailed context dict.
    input_dict_for_agent = {
        "theme": theme,
        "victim": victim.model_dump(),
        "suspect_profile": suspect.profile.model_dump(),
        "original_mmo": suspect.original_mmo.model_dump(),
        "element_to_modify": element_to_modify_str,
        "original_element_value_to_modify": original_value # Explicitly pass the value to modify
    }
    
    # We will refine the MMO_MODIFIER_INSTRUCTIONS to expect this input dict structure.
    return input_dict_for_agent, element_to_modify_str # Return element type for orchestrator to know 