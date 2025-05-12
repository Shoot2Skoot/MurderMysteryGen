"""
Case Initialization Agent for the Murder Mystery Generation system.

This module defines the Case Initialization Agent, which is responsible for generating
the initial victim profile based on the theme and selected attributes. It generates 
a plausible victim with a name, occupation, personality, and cause of death that are
thematically consistent.
"""

from agents import (
    Agent,
)  # Assuming ModelSettings might be used later, not for MVP default model params

from ..core.data_models import VictimProfile

# Define the CaseInitializationAgent
# This agent is responsible for taking a theme, a set of attribute options,
# selecting one from each option list, and generating the initial victim profile,
# thematically integrating the selected attributes and populating chosen category fields.

# Instructions for the agent:
# - It will receive a theme (e.g., "Cyberpunk", "Haunted Mansion").
# - Its goal is to generate plausible victim details: Name, Occupation, Personality, and Cause of Death.
# - These details must be consistent with the provided theme.
# - The output must be a JSON object matching the VictimProfile schema.

CASE_INITIALIZER_INSTRUCTIONS = """
You are the Case Initialization Agent for a murder mystery generation system.
Your primary role is to establish the foundational details of the victim.

Input:
- You will receive a JSON object containing:
  - `theme`: A string for the mystery's overall theme (e.g., "Cyberpunk", "Haunted Mansion").
  - `attribute_options`: An object containing four lists of strings:
    - `cause_of_death_options`: A list of 2-3 potential cause of death categories.
    - `motive_category_options`: A list of 2-3 potential motive categories (for later use with suspects, NOT for the victim).
    - `occupation_archetype_options`: A list of 2-3 potential occupation archetypes for the victim.
    - `personality_archetype_options`: A list of 2-3 potential personality archetypes for the victim.
  - `thematic_names`: An object containing two lists of strings:
    - `first_names`: A list of thematically appropriate first names (typically 50 names).
    - `last_names`: A list of thematically appropriate last names (typically 50 names).

Task:
1.  Review the overall `theme`.
2.  From the relevant lists within `attribute_options`, SELECT EXACTLY ONE option from:
    - `cause_of_death_options` 
    - `occupation_archetype_options`
    - `personality_archetype_options`
    (Note: The `motive_category_options` are for suspects and will be handled later)
3.  From the provided `thematic_names` lists, SELECT EXACTLY ONE name from each:
    - Select ONE first name from the `first_names` list
    - Select ONE last name from the `last_names` list
    - Combine these to form the victim's full name
4.  Based on the `theme`, your selected options, and the chosen name, generate the following details for the victim:
    *   `name`: The combined first and last name you selected from the thematic name lists.
    *   `occupation`: The victim's occupation. This description should be inspired by and thematically consistent with your SELECTED `occupation_archetype_options` and the overall `theme`. Do not just state the archetype; describe the occupation.
    *   `personality`: A brief (1-2 sentence) description of the victim's key personality traits. This description should be inspired by and thematically consistent with your SELECTED `personality_archetype_options` and the overall `theme`.
    *   `cause_of_death`: The apparent or determined cause of death. This description should be inspired by and thematically consistent with your SELECTED `cause_of_death_options` and the overall `theme`.
5.  Populate the explicit tracking fields with the exact string value of the option you selected in step 2:
    *   `chosen_cause_of_death_category`: The exact string you selected from `cause_of_death_options`.
    *   `chosen_occupation_archetype`: The exact string you selected from `occupation_archetype_options`.
    *   `chosen_personality_archetype`: The exact string you selected from `personality_archetype_options`.
6. Ensure the overall victim profile, including their name and implied circumstances, is coherent and thematically consistent.

Output Format:
- You MUST output your response as a single, valid JSON object that strictly conforms to the following Pydantic model schema (VictimProfile):
  `name: str` (Full name of the victim.)
  `occupation: str` (The victim's occupation or primary role.)
  `personality: str` (A brief description of the victim's personality traits.)
  `cause_of_death: str` (The determined or apparent cause of death.)
  `chosen_cause_of_death_category: Optional[str]` (The specific category of cause of death selected by the agent.)
  `chosen_occupation_archetype: Optional[str]` (The specific occupation archetype selected by the agent for the victim.)
  `chosen_personality_archetype: Optional[str]` (The specific personality archetype selected by the agent for the victim.)

Example for input:
```json
{
  "theme": "Gothic Victorian Manor",
  "attribute_options": {
    "cause_of_death_options": ["Poisoning", "Fall from height", "Asphyxiation"],
    "motive_category_options": ["Inheritance", "Forbidden Love", "Dark Secret"],
    "occupation_archetype_options": ["Reclusive Scholar", "Wealthy Dowager", "Disgraced Doctor"],
    "personality_archetype_options": ["Melancholy", "Manipulative", "Secretive"]
  },
  "thematic_names": {
    "first_names": ["Beatrice", "Edmund", "Victoria", "Clarence", "Adelaide", "Theodore", "Florence", "Augustus", "Henrietta", "Reginald"],
    "last_names": ["Blackwood", "Thornfield", "Ravenscroft", "Hawthorne", "Wellington", "Pembrooke", "Montgomery", "Greystone", "Devereux", "Winchester"]
  }
}
```

Example of corresponding output (if "Fall from height", "Wealthy Dowager", and "Manipulative" were selected, and "Beatrice" and "Blackwood" were chosen from the name lists):
```json
{
  "name": "Beatrice Blackwood",
  "occupation": "The elderly, and exceedingly wealthy, matriarch of Blackwood Manor. Known for her vast fortune and control over the family estate.",
  "personality": "A woman of sharp intellect and a subtly manipulative nature, often pitting family members against each other for her amusement and to maintain her influence.",
  "cause_of_death": "Found at the bottom of the grand staircase, a tragic fall that many whisper was no accident, given the frayed nerves and simmering resentments within the household.",
  "chosen_cause_of_death_category": "Fall from height",
  "chosen_occupation_archetype": "Wealthy Dowager",
  "chosen_personality_archetype": "Manipulative"
}
```
Ensure all fields are populated and the JSON is correctly structured.
"""

case_initializer_agent = Agent(
    name="Case Initialization Agent",
    instructions=CASE_INITIALIZER_INSTRUCTIONS,
    model="gpt-4.1-mini",  # Changed to gpt-4.1-mini
    # model_settings=ModelSettings(temperature=0.7), # Example if we needed to adjust settings
    output_type=VictimProfile,
)

# To test this agent (example usage, actual orchestration will be in main_orchestrator.py):
if __name__ == "__main__":
    import json
    import logging
    import os

    from agents import Runner
    from dotenv import load_dotenv

    # Setup basic logging to see agent activity
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Load .env file from the project root
    # This script is in src/mystery_ai/agents/
    # Project root is ../../../ from here
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    dotenv_path = os.path.join(project_root, ".env")
    if not os.path.exists(dotenv_path):
        print(
            "Error: .env file not found. Please create one in the project root (MurderMysteryGen/) with your OPENAI_API_KEY."
        )
    else:
        load_dotenv(dotenv_path=dotenv_path)
        print(f".env loaded from {dotenv_path}")
        if not os.getenv("OPENAI_API_KEY"):
            print("Error: OPENAI_API_KEY not found in .env file.")
        else:
            print("OPENAI_API_KEY found.")

            # Test with a theme and sample thematic name lists
            test_input = {
                "theme": "Haunted Library",
                "attribute_options": {
                    "cause_of_death_options": [
                        "Poisoning",
                        "Nerve Agent",
                        "Blunt Force Trauma",
                    ],
                    "motive_category_options": [
                        "Revenge",
                        "Mistaken Identity",
                        "Eliminating a Rival",
                    ],
                    "occupation_archetype_options": [
                        "Librarian/Archivist",
                        "Researcher",
                        "Historian",
                    ],
                    "personality_archetype_options": [
                        "Naive/Gullible",
                        "Curious/Inquisitive",
                        "Reclusive/Reserved",
                    ],
                },
                "thematic_names": {
                    "first_names": [
                        "Evelyn",
                        "Edgar",
                        "Luna",
                        "Theodore",
                        "Agnes",
                        "Silas",
                        "Cordelia",
                        "Gideon",
                        "Mabel",
                        "Ambrose",
                    ],
                    "last_names": [
                        "Blackwood",
                        "Grimsley",
                        "Carrington",
                        "Hawthorne",
                        "Ashcroft",
                        "Winchester",
                        "Lockwood",
                        "Blythe",
                        "Fairchild",
                        "Hargrove",
                    ],
                },
            }

            print(f"\nTesting CaseInitializationAgent with theme: {test_input['theme']}")
            # Simply mention that we have names without trying to display them
            print(
                f"Using thematically appropriate first and last names for '{test_input['theme']}'..."
            )

            try:
                # Convert the input dictionary to a JSON string
                test_input_json = json.dumps(test_input)

                # Run the agent with the test input
                result = Runner.run_sync(case_initializer_agent, input=test_input_json)

                if result and result.final_output:
                    victim_profile: VictimProfile = result.final_output_as(VictimProfile)
                    print("\nSuccessfully generated VictimProfile:")
                    print(victim_profile.model_dump_json(indent=2))
                    print(f"\nSelected victim name: {victim_profile.name}")
                    print(
                        f"Selected cause of death: {victim_profile.chosen_cause_of_death_category}"
                    )
                    print(f"Selected occupation: {victim_profile.chosen_occupation_archetype}")
                    print(f"Selected personality: {victim_profile.chosen_personality_archetype}")
                else:
                    print("\nAgent run did not produce the expected output or failed.")
                    if result:
                        print(f"Raw output: {result.final_output}")

            except Exception as e:
                print(f"\nAn error occurred: {e}")
