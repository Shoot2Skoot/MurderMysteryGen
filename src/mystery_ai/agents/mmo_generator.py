# src/mystery_ai/agents/mmo_generator.py

"""
MMO Generator Agent for the Murder Mystery Generation system.

This module defines the MMO (Means, Motive, Opportunity) Generator Agent, which is
responsible for creating plausible means, motives, and opportunities for each suspect.
These elements form the core of the mystery's logic and provide the foundation for the
suspect's potential involvement in the crime.
"""

from agents import Agent

from ..core.data_models import (
    MMO,
)  # CaseContext for theme/victim, SuspectProfile for current suspect

MMO_GENERATOR_INSTRUCTIONS = """
You are the MMO (Means, Motive, Opportunity) Generation Agent for a murder mystery generation system.
Your role is to develop a plausible Means, Motive, and Opportunity for a *specific suspect* based on the overall case context (theme, victim details) and the suspect's own profile.

Input:
- You will receive a dictionary containing:
  - `theme`: The overall theme of the mystery (e.g., "Victorian London Séance").
  - `victim`: An object with victim details (`name`, `occupation`, `personality`, `cause_of_death`).
  - `suspect_profile`: An object with the specific suspect's details (`name`, `description`, `relationship_to_victim`).

Task:
1.  Analyze all provided input: the theme, the victim's details, and the specific suspect's profile.
2.  For this *specific suspect*, generate one distinct and plausible:
    *   `means`: How this suspect could have committed the crime, consistent with their profile, the victim, and the theme.
    *   `motive`: Why this suspect might have wanted to commit the crime, linking to their relationship with the victim, their personality, or the thematic context.
    *   `opportunity`: When and where this suspect could have had the chance to commit the crime, consistent with the setting and their profile.
3.  Ensure the Means, Motive, and Opportunity are logically consistent with each other and with all provided context for this specific suspect.

Output Format:
- You MUST output your response as a single, valid JSON object that strictly conforms to the MMO schema:
  `means: str` (How the suspect could have committed the crime.)
  `motive: str` (Why the suspect might have wanted to commit the crime.)
  `opportunity: str` (When and where the suspect could have had the chance to commit the crime.)

Example Input (passed as a dictionary to the 'input' of Runner.run_sync):
```json
{
  "theme": "Victorian London Séance",
  "victim": {
    "name": "Madame Eleanor Blackwood",
    "occupation": "Renowned Spiritual Medium",
    "personality": "Charismatic and enigmatic...",
    "cause_of_death": "Strangulation during a séance..."
  },
  "suspect_profile": {
    "name": "Lord Alistair Finch",
    "description": "A skeptical nobleman...",
    "relationship_to_victim": "Wealthy client..."
  }
}
```

Example Output (a JSON object for the MMO):
```json
{
  "means": "Used a silk scarf, easily concealed, to strangle her during the darkened séance when everyone's attention was supposedly on the 'spirits'.",
  "motive": "Finch discovered Blackwood was defrauding him and other wealthy patrons; he intended to expose her, but she threatened him with a scandal of his own, leading to a confrontation.",
  "opportunity": "Was present at the séance, seated near Madame Blackwood. The confusion and darkness of the event provided the perfect cover."
}
```
Ensure all fields are populated and the JSON is correctly structured.
"""

mmo_generator_agent = Agent(
    name="MMO Generation Agent",
    instructions=MMO_GENERATOR_INSTRUCTIONS,
    model="gpt-4.1-mini",
    # model_settings=ModelSettings(temperature=0.7),
    output_type=MMO,
)

# Example Test Block (for isolated testing if needed)
# if __name__ == '__main__':
#     from agents import Runner
#     from dotenv import load_dotenv
#     import os
#     import logging
#     from ..core.data_models import CaseContext, VictimProfile, SuspectProfile, MMO # For constructing test input

#     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
#     dotenv_path = os.path.join(project_root, '.env')
#     load_dotenv(dotenv_path=dotenv_path)

#     if not os.getenv("OPENAI_API_KEY"):
#         print("Error: OPENAI_API_KEY not found.")
#     else:
#         print("OPENAI_API_KEY found for MMOGenerator test.")

#         sample_victim = VictimProfile(
#             name="Madame Eleanor Blackwood",
#             occupation="Renowned Spiritual Medium",
#             personality="Charismatic and enigmatic...",
#             cause_of_death="Strangulation during a séance..."
#         )
#         sample_suspect_profile = SuspectProfile(
#             name="Lord Alistair Finch",
#             description="A skeptical nobleman...",
#             relationship_to_victim="Wealthy client..."
#         )
#         test_input_dict = {
#             "theme": "Victorian London Séance",
#             "victim": sample_victim.model_dump(),
#             "suspect_profile": sample_suspect_profile.model_dump()
#         }

#         print(f"\nTesting MMOGenerationAgent with input:\n{test_input_dict}")

#         try:
#             result = Runner.run_sync(mmo_generator_agent, input=test_input_dict)

#             if result and result.final_output:
#                 mmo_output: MMO = result.final_output # output_type handles conversion
#                 print("\nSuccessfully generated MMO:")
#                 print(mmo_output.model_dump_json(indent=2))
#             else:
#                 print("\nAgent run did not produce the expected output or failed.")
#                 if result:
#                     print(f"Raw output: {result.final_output}")
#                     print(f"All messages: {result.messages}")
#         except Exception as e:
#             print(f"\nAn error occurred: {e}", exc_info=True)
