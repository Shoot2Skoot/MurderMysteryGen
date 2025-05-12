# src/mystery_ai/agents/suspect_generator.py

"""
Suspect Generator Agent for the Murder Mystery Generation system.

This module defines the Suspect Generator Agent, which is responsible for creating
the initial profiles for all suspects in the mystery. It generates suspects with names,
descriptions, and relationships to the victim, ensuring they are thematically consistent
and diverse enough to create an engaging mystery.
"""

from typing import List

from agents import Agent

from ..core.data_models import (
    SuspectProfile,
)  # Assuming CaseContext might be passed for full context

SUSPECT_GENERATOR_INSTRUCTIONS = """
You are the Suspect Generation Agent for a murder mystery generation system.
Your role is to create a list of 2-3 distinct and plausible suspect profiles based on the provided case context (theme and victim details).

Input:
- You will receive the case context, which includes:
  - `theme`: The overall theme of the mystery (e.g., "Cyberpunk Noir Detective").
  - `victim`: An object containing details about the victim (`name`, `occupation`, `personality`, `cause_of_death`).
  - `motive_category_options`: A list of 2-3 potential motive categories you must choose from for each suspect.
  - `occupation_archetype_options`: A list of 2-3 potential occupation archetypes for the suspects.
  - `personality_archetype_options`: A list of 2-3 potential personality archetypes for the suspects.

Task:
1.  Analyze the theme and victim details.
2.  Generate 2 to 3 unique suspect profiles. Do not generate more than 3.
3.  For each suspect, provide:
    *   `name`: A plausible full name fitting the theme and potentially having some connection or contrast to the victim's name/status.
    *   `description`: A brief (1-2 sentences) description of the suspect. This description should paint a vivid picture of their character and demeanor. It must be thematically consistent with the overall `theme`. Crucially, it should be *inspired by* your selected `chosen_occupation_archetype` and `chosen_personality_archetype` for this suspect, but ***do not simply restate these archetypes***. Instead, weave their essence into a unique, descriptive narrative about the suspect. For instance:
        - If occupation is 'Scholar' and personality is 'Reserved' for a "Gothic University" theme, description could be: 'Dr. Alistair Finch, a reclusive historian, was rarely seen outside the dusty confines of the university's oldest wing, preferring the silent company of ancient texts to living colleagues.'
        - If occupation is 'Manual Laborer/Tradesperson' and personality is 'Extroverted/Outgoing' for a "Haunted Library" theme, description could be: 'The library's aging groundskeeper, Barnaby "Barney" Croft, a man whose boisterous laughter and endless supply of stories often felt jarringly out of place amidst the shadowed, silent stacks he meticulously tended.'
        - If occupation is 'Service Industry Worker' and personality is 'Deceptive/Manipulative' for a "Luxury Cruise Ship" theme, description could be: 'Leo Maxwell, a charismatic bartender on the ship, always had a charming smile and a listening ear, but his uncanny ability to extract secrets from passengers often left a subtle chill.'
    *   `relationship_to_victim`: A concise description of how the suspect knew or was connected to the victim (e.g., "Business partner", "Jilted lover", "Estranged sibling", "Rival scientist").
    *   `chosen_motive_category`: Select one motive category from the provided `motive_category_options` that best fits this specific suspect.
    *   `chosen_occupation_archetype`: Select one occupation archetype from the provided `occupation_archetype_options` for this suspect.
    *   `chosen_personality_archetype`: Select one personality archetype from the provided `personality_archetype_options` for this suspect.
4.  Ensure suspects are distinct from each other and from the victim in terms of their core description/role.
5.  IMPORTANT: Assign a different motive category to each suspect whenever possible from the provided options. Try to also diversify the chosen occupation and personality archetypes among suspects if the options allow.

Output Format:
- You MUST output your response as a single, valid JSON list, where each item in the list is an object strictly conforming to the SuspectProfile schema:
  `name: str` (Full name of the suspect.)
  `description: str` (A brief description of the suspect, integrating selected occupation and personality.)
  `relationship_to_victim: str` (The suspect's relationship to the victim.)
  `chosen_motive_category: str` (The specific motive category selected from the options provided.)
  `chosen_occupation_archetype: str` (The specific occupation archetype selected from the options provided.)
  `chosen_personality_archetype: str` (The specific personality archetype selected from the options provided.)

Example Input (passed as a dictionary to the 'input' or 'user_prompt' of the Runner.run_sync call):
```json
{
  "theme": "Victorian London Séance",
  "victim": {
    "name": "Madame Eleanor Blackwood",
    "occupation": "Renowned Spiritual Medium",
    "personality": "Charismatic and enigmatic, with a flair for the dramatic.",
    "cause_of_death": "Strangulation during a séance session."
  },
  "motive_category_options": ["Revenge", "Financial Gain", "Fear / Self-preservation"],
  "occupation_archetype_options": ["Disgruntled Client", "Jealous Rival", "Secret Admirer"],
  "personality_archetype_options": ["Volatile", "Calculating", "Obsessive"]
}
```

Example Output (a JSON list of SuspectProfile objects):
```json
[
  {
    "name": "Lord Alistair Finch",
    "description": "A skeptical nobleman often seen poring over obscure texts in the library's west wing. His volatile temper was well-known, particularly when his meticulously researched theories were challenged by Madame Blackwood.",
    "relationship_to_victim": "Wealthy client, publicly debunked her rival medium.",
    "chosen_motive_category": "Revenge",
    "chosen_occupation_archetype": "Disgruntled Client",
    "chosen_personality_archetype": "Volatile"
  },
  {
    "name": "Miss Clara Holloway",
    "description": "Madame Blackwood's quiet and observant assistant. Though outwardly timid, a calculating glint could often be seen in her eyes as she managed the spiritualist's affairs, perhaps dreaming of a grander life.",
    "relationship_to_victim": "Personal assistant and confidante.",
    "chosen_motive_category": "Financial Gain",
    "chosen_occupation_archetype": "Jealous Rival",
    "chosen_personality_archetype": "Calculating"
  }
]
```
Ensure the output is ONLY the JSON list of suspect profiles.
"""

suspect_generator_agent = Agent(
    name="Suspect Generation Agent",
    instructions=SUSPECT_GENERATOR_INSTRUCTIONS,
    model="gpt-4.1-mini",
    # model_settings=ModelSettings(temperature=0.75), # Slightly higher temp for more varied suspects
    output_type=List[SuspectProfile],  # Expecting a list of SuspectProfile objects
)

# Example Test Block (for isolated testing if needed)
# if __name__ == '__main__':
#     from agents import Runner
#     from dotenv import load_dotenv
#     import os
#     import logging
#     from ..core.data_models import CaseContext, VictimProfile # For constructing test input

#     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
#     dotenv_path = os.path.join(project_root, '.env')
#     load_dotenv(dotenv_path=dotenv_path)

#     if not os.getenv("OPENAI_API_KEY"):
#         print("Error: OPENAI_API_KEY not found.")
#     else:
#         print("OPENAI_API_KEY found for SuspectGenerator test.")
#         # Construct a sample CaseContext input similar to what the agent expects
#         sample_victim = VictimProfile(
#             name="Dr. Evelyn Reed",
#             occupation="Lead Scientist at Chronos Corp",
#             personality="Brilliant, ambitious, but secretive and known for taking credit for others' work.",
#             cause_of_death="Found dead in her locked lab, apparently from a sabotaged experiment."
#         )
#         sample_case_context_dict = {
#             "theme": "Near-Future Sci-Fi Corporate Espionage",
#             "victim": sample_victim.model_dump() # Pass victim as a dict, as LLM expects JSON-like input
#         }

#         print(f"\nTesting SuspectGenerationAgent with input:\n{sample_case_context_dict}")

#         try:
#             # The input to the agent should match what its instructions expect.
#             # Since instructions refer to receiving theme and victim (as an object),
#             # we should pass a dictionary representing this structure.
#             result = Runner.run_sync(suspect_generator_agent, input=sample_case_context_dict)

#             if result and result.final_output:
#                 suspect_profiles: List[SuspectProfile] = result.final_output # output_type handles conversion
#                 print("\nSuccessfully generated SuspectProfiles:")
#                 for profile in suspect_profiles:
#                     print(profile.model_dump_json(indent=2))
#             else:
#                 print("\nAgent run did not produce the expected output or failed.")
#                 if result:
#                     print(f"Raw output: {result.final_output}")
#                     print(f"All messages: {result.messages}")
#         except Exception as e:
#             print(f"\nAn error occurred: {e}", exc_info=True)
