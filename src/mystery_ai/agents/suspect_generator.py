# src/mystery_ai/agents/suspect_generator.py

from typing import List, Dict, Any
from agents import Agent, ModelSettings
from ..core.data_models import VictimProfile, SuspectProfile, CaseContext # Assuming CaseContext might be passed for full context

SUSPECT_GENERATOR_INSTRUCTIONS = """
You are the Suspect Generation Agent for a murder mystery generation system.
Your role is to create a list of 2-3 distinct and plausible suspect profiles based on the provided case context (theme and victim details).

Input:
- You will receive the case context, which includes:
  - `theme`: The overall theme of the mystery (e.g., "Cyberpunk Noir Detective").
  - `victim`: An object containing details about the victim (`name`, `occupation`, `personality`, `cause_of_death`).
  - `motive_category_options`: A list of 2-3 potential motive categories you must choose from for each suspect.

Task:
1.  Analyze the theme and victim details.
2.  Generate 2 to 3 unique suspect profiles. Do not generate more than 3.
3.  For each suspect, provide:
    *   `name`: A plausible full name fitting the theme and potentially having some connection or contrast to the victim's name/status.
    *   `description`: A brief (1-2 sentences) description of the suspect, outlining their archetype, key characteristics, or general demeanor. This should be consistent with the theme.
    *   `relationship_to_victim`: A concise description of how the suspect knew or was connected to the victim (e.g., "Business partner", "Jilted lover", "Estranged sibling", "Rival scientist").
    *   `chosen_motive_category`: Select one motive category from the provided `motive_category_options` that best fits this specific suspect. Each suspect should have their own appropriate motive category that makes sense for their character and relationship to the victim.
4.  Ensure suspects are distinct from each other and from the victim in terms of their core description/role.
5.  IMPORTANT: Assign a different motive category to each suspect whenever possible from the provided options.

Output Format:
- You MUST output your response as a single, valid JSON list, where each item in the list is an object strictly conforming to the SuspectProfile schema:
  `name: str` (Full name of the suspect.)
  `description: str` (A brief description of the suspect.)
  `relationship_to_victim: str` (The suspect's relationship to the victim.)
  `chosen_motive_category: str` (The specific motive category selected from the options provided.)

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
  "motive_category_options": ["Revenge", "Financial Gain", "Fear / Self-preservation"]
}
```

Example Output (a JSON list of SuspectProfile objects):
```json
[
  {
    "name": "Lord Alistair Finch",
    "description": "A skeptical nobleman and wealthy client of Madame Blackwood, known for his rationality and disdain for the occult.",
    "relationship_to_victim": "Wealthy client, publicly debunked her rival medium.",
    "chosen_motive_category": "Revenge"
  },
  {
    "name": "Miss Clara Holloway",
    "description": "Madame Blackwood's timid and observant young assistant, privy to all her secrets.",
    "relationship_to_victim": "Personal assistant and confidante.",
    "chosen_motive_category": "Financial Gain"
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
    output_type=List[SuspectProfile] # Expecting a list of SuspectProfile objects
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