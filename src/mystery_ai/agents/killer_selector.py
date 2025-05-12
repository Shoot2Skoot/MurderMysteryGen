# src/mystery_ai/agents/killer_selector.py

"""
Killer Selector module for the Murder Mystery Generation system.

This module contains logic for selecting which suspect will be the killer. It provides
both a random selection function and a more sophisticated agent-based approach for
determining the most suitable suspect to be the killer based on their characteristics.
"""

import random
from typing import List

from agents import Agent

from ..core.data_models import Suspect  # To update Suspect objects

# This agent might not need an LLM call for MVP if selection is random.
# It could directly modify the CaseContext or list of suspects.
# However, for consistency and future enhancement (e.g., selecting killer based on criteria),
# we can define it as an agent. Its output_type could be the updated List[Suspect].

KILLER_SELECTOR_INSTRUCTIONS = """
You are the Killer Selection Agent.
Your task is to designate one suspect as the killer from a provided list of suspects.
For the MVP, this selection will be random. 

Input:
- A list of Suspect objects, each with their profile and original MMO.
  (This will be passed as a list of dictionaries in the input to the Runner)

Task:
1. Randomly select one suspect from the input list to be the killer.
2. Update the `is_killer` flag to `True` for the selected suspect.
3. Ensure all other suspects have their `is_killer` flag set to `False` (it should be default False anyway).

Output Format:
- You MUST output your response as a single, valid JSON list of Suspect objects, where each object 
  reflects the updated `is_killer` status. The structure of each Suspect object in the output list
  must conform to the Suspect Pydantic model used in the system.
  Example fields: `profile`, `original_mmo`, `is_killer`.
"""

# This agent can be implemented without an LLM call for MVP if random selection is sufficient.
# If so, its main logic would be in a Python function called by the orchestrator, not an LLM-backed agent.
# For now, defining as an agent for consistency, but it might be refactored.
# If it *were* an LLM agent, it would need to understand to output the *full list* of suspects with one modified.
# A simpler non-LLM approach for random selection:


def select_killer_randomly(suspects: List[Suspect]) -> List[Suspect]:
    """Randomly selects one suspect as the killer and updates their status."""
    if not suspects:
        return []

    # Ensure all are initially not the killer
    for s in suspects:
        s.is_killer = False

    selected_killer = random.choice(suspects)
    selected_killer.is_killer = True
    return suspects


# For Story 3.1, we are just defining the agent skeleton.
# The actual implementation (LLM-based or Python-based) will be part of the story implementation.
# If we decide on a Python-based function for the orchestrator to call directly for random selection,
# then this agent definition might be simplified or removed for MVP.
# For now, let's assume it could be an agent that the orchestrator *could* call.

killer_selector_agent_placeholder = Agent(
    name="Killer Selection Agent (Placeholder)",
    instructions="Processes a list of suspects and designates one as the killer (currently placeholder for random Python logic).",
    model="gpt-4o-mini",  # Or any model, may not be used if logic is pure Python
    output_type=List[Suspect],  # If it were to output the modified list
)

# The actual function to be called by the orchestrator for MVP
# will be select_killer_randomly directly for simplicity in main_orchestrator.py
