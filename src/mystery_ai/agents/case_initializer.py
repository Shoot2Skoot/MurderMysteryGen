# src/mystery_ai/agents/case_initializer.py

from agents import Agent, ModelSettings # Assuming ModelSettings might be used later, not for MVP default model params
from ..core.data_models import VictimProfile

# Define the CaseInitializationAgent
# This agent is responsible for taking a theme and generating the initial victim profile.

# Instructions for the agent:
# - It will receive a theme (e.g., "Cyberpunk", "Haunted Mansion").
# - Its goal is to generate plausible victim details: Name, Occupation, Personality, and Cause of Death.
# - These details must be consistent with the provided theme.
# - The output must be a JSON object matching the VictimProfile schema.

CASE_INITIALIZER_INSTRUCTIONS = """
You are the Case Initialization Agent for a murder mystery generation system.
Your primary role is to establish the foundational details of the victim based on a given theme.

Input:
- You will receive a theme for the mystery as a simple string (e.g., "Cyberpunk", "Haunted Mansion", "Pirate Ship").

Task:
1.  Based *only* on the provided theme, generate the following details for the victim:
    *   `name`: A plausible full name for the victim, fitting the theme.
    *   `occupation`: The victim's occupation or primary role within the story's setting, consistent with the theme.
    *   `personality`: A brief (1-2 sentence) description of the victim's key personality traits relevant to a mystery, fitting the theme.
    *   `cause_of_death`: Generate a CREATIVE and UNCOMMON cause of death that is HIGHLY SPECIFIC and PLAUSIBLE for the given theme. 
        Do NOT use generic causes like 'poisoning', 'strangulation', 'stabbing', or 'blunt force trauma' UNLESS the METHOD or WEAPON is exceptionally unique, deeply integrated with the theme, and described as such. 
        For example, for a theme like "Steampunk Airship Crew", a cause like "Impaled by a malfunctioning brass astrolabe during a high-altitude storm" is far more interesting than just "fell from height." 
        For a "Cyberpunk Megatower" theme, "Neural interface overload triggered by a rogue AI fragment" is better than "electrocuted."
        Consider the victim's potential occupation and personality within the theme to devise a fitting and intriguing demise that could be central to the mystery.

Output Format:
- You MUST output your response as a single, valid JSON object that strictly conforms to the following Pydantic model schema (VictimProfile):
  `name: str` (Full name of the victim.)
  `occupation: str` (The victim's occupation or primary role.)
  `personality: str` (A brief description of the victim's personality traits.)
  `cause_of_death: str` (The determined or apparent cause of death, fitting the creative and thematic criteria above.)

Example for theme "Noir Detective Agency":
Output:
```json
{
  "name": "Johnny 'Silas' Marlowe",
  "occupation": "Private Investigator, Owner of 'The Shadowed Lens' Detective Agency",
  "personality": "Cynical and world-weary, but with a hidden sense of justice. Known for his sharp wit and ability to blend into the city's underbelly.",
  "cause_of_death": "Found with a rare, untraceable neurotoxin delivered via a poisoned dart, disguised as a vintage fountain pen nib -- a collector's item only a few knew he possessed."
}
```
Ensure all fields are populated and the JSON is correctly structured.
"""

case_initializer_agent = Agent(
    name="Case Initialization Agent",
    instructions=CASE_INITIALIZER_INSTRUCTIONS,
    model="gpt-4.1-mini", # Changed to gpt-4.1-mini
    # model_settings=ModelSettings(temperature=0.7), # Example if we needed to adjust settings
    output_type=VictimProfile
)

# To test this agent (example usage, actual orchestration will be in main_orchestrator.py):
# if __name__ == '__main__':
#     from agents import Runner
#     from dotenv import load_dotenv
#     import os
#     import logging

#     # Setup basic logging to see agent activity
#     logging.basicConfig(level=logging.INFO,
#                         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
#     # Load .env file from the project root
#     # This script is in src/mystery_ai/agents/
#     # Project root is ../../../ from here
#     project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
#     dotenv_path = os.path.join(project_root, '.env')
#     if not os.path.exists(dotenv_path):
#         print("Error: .env file not found. Please create one in the project root (MurderMysteryGen/) with your OPENAI_API_KEY.")
#     else:
#         load_dotenv(dotenv_path=dotenv_path)
#         print(f".env loaded from {dotenv_path}")
#         if not os.getenv("OPENAI_API_KEY"):
#             print("Error: OPENAI_API_KEY not found in .env file.")
#         else:
#             print("OPENAI_API_KEY found.")
#             test_theme = "Medieval Fantasy Kingdom"
#             print(f"\nTesting CaseInitializationAgent with theme: {test_theme}")
            
#             # The input to an agent using output_type is typically a string or a dict.
#             # For this agent, the instructions imply it processes a theme passed as a simple string 
#             # or a dict like {"theme": "your_theme"}. Let's assume simple string for direct input for now,
#             # or the orchestrator can wrap it if needed.
#             # For structured input, you might define an input Pydantic model for the agent too.
            
#             try:
#                 # SDK expects input_data to be a string, or a dict for models expecting multiple inputs not via tools.
#                 # If instructions parse from a general input, a simple string might be fine.
#                 # If the agent expects a specific field like `theme`, pass a dict.
#                 # Let's try passing the theme as a simple string first, relying on the prompt to guide.
#                 # A more robust way if the agent strictly needs {"theme": ...} is to pass that dict.
#                 # For an agent expecting `output_type`, the `input_data` is the prompt or content it processes.
#                 # The instructions guide how it should interpret this input_data to produce the structured output.
                
#                 # Option 1: Pass theme as direct input string for the agent to process based on instructions.
#                 # result = Runner.run_sync(case_initializer_agent, test_theme)

#                 # Option 2: More explicit if the agent were designed to always expect a dict with a 'theme' key.
#                 # This is often better for clarity if the agent's prompt implies specific input fields.
#                 # Since our instructions say "You will receive a theme for the mystery as a simple string", Option 1 is closer.
#                 # However, the prompt for structured output often implies the LLM should *receive* the input data as part of its user message.
#                 # The `input` to `Runner.run` forms this user message. So, sending the theme string directly is correct.
                
#                 result = Runner.run_sync(case_initializer_agent, test_theme)

#                 if result and result.final_output:
#                     victim_profile: VictimProfile = result.final_output_as(VictimProfile)
#                     print("\nSuccessfully generated VictimProfile:")
#                     print(victim_profile.model_dump_json(indent=2))
#                 else:
#                     print("\nAgent run did not produce the expected output or failed.")
#                     if result:
#                         print(f"Raw output: {result.final_output}")
#                         print(f"All messages: {result.messages}")

#             except Exception as e:
#                 print(f"\nAn error occurred: {e}") 