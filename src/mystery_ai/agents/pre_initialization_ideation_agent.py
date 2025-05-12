# src/mystery_ai/agents/pre_initialization_ideation_agent.py

"""
Pre-Initialization Ideation Agent for the Murder Mystery Generation system.

This module defines the Pre-Initialization Ideation Agent, which is responsible for
generating thematically appropriate first and last names based on the given theme.
These names are used for victims and suspects, ensuring consistent theming throughout
the mystery.
"""

from typing import List

from agents import Agent
from pydantic import BaseModel, Field


# Define the Pydantic model for the agent's output
class ThematicNameLists(BaseModel):
    """Model representing thematically appropriate name lists for a given theme."""

    first_names: List[str] = Field(description="A list of thematically appropriate first names.")
    last_names: List[str] = Field(description="A list of thematically appropriate last names.")


# Define the agent's instructions
PRE_INITIALIZATION_IDEATION_INSTRUCTIONS = """
You are the Pre-Initialization Ideation Agent for a murder mystery generation system.
Your primary role is to generate thematically appropriate names based on a provided theme.

Input:
- You will receive a theme for the mystery as a simple string (e.g., "Cyberpunk Dystopia", "Victorian London", "Wild West Outpost").

Task:
1. Analyze the provided theme carefully.
2. Generate TWO separate lists:
   - A list of 50 thematically appropriate FIRST NAMES that would plausibly exist within the given theme.
   - A list of 50 thematically appropriate LAST NAMES that would plausibly exist within the given theme.
3. Ensure the names are diverse while remaining thematically consistent. Avoid repetitive patterns or extremely similar names.
4. Consider cultural, historical, linguistic, and geographic elements that might influence naming conventions within the theme.
5. Ensure an appropriate gender balance in first names unless the theme specifically suggests otherwise.
6. Include names of varying lengths and complexity.

Output Format:
- You MUST output your response as a single, valid JSON object that strictly conforms to the following schema:
  ```json
  {
    "first_names": ["Name1", "Name2", "Name3", ...], // List of 50 first names
    "last_names": ["Surname1", "Surname2", "Surname3", ...] // List of 50 last names
  }
  ```

Example Input:
"Cyberpunk Dystopia"

Example Output:
```json
{
  "first_names": [
    "Zara", "Neo", "Vex", "Trinity", "Raven", "Jax", "Echo", "Nova", "Cyrus", "Ava",
    "Axel", "Pax", "Dex", "Iris", "Matrix", "Maddox", "Nyx", "Ripley", "Deckard", "Vale",
    "Flux", "Zero", "Cortex", "Hex", "Rex", "Bit", "Glitch", "Pixel", "Quorra", "Chrome",
    "Neon", "Syntax", "Vector", "Cache", "Cinder", "Cipher", "Jet", "Core", "Blaze", "Trace",
    "Phoenix", "Link", "Dash", "Zion", "Pulse", "Spark", "Static", "Chip", "Data", "Void"
  ],
  "last_names": [
    "Zhang", "Reeves", "Nakamura", "Deckard", "Rodriguez", "Walsh", "Chen", "Kim", "Takeda", "Weyland",
    "Monroe", "Ryder", "Tesla", "Singh", "Anderson", "Wilson", "Watts", "Kurosawa", "Tyrell", "Gibson",
    "Sterling", "Kovacs", "Hayes", "Chiba", "Morgan", "Lawson", "Blackburn", "Gray", "Mori", "Nova",
    "Flynn", "Shaw", "Teller", "Cruz", "Steel", "Jones", "Maxwell", "Weber", "Price", "Crane",
    "Takeshi", "Batty", "Wallace", "Corben", "Shimada", "Blake", "Quantum", "Lee", "Sato", "Cairo"
  ]
}
```

Ensure all lists contain 50 items each, are properly formatted as JSON arrays, and follow the exact schema specified above.
"""

# Define the agent
pre_initialization_ideation_agent = Agent(
    name="Pre-Initialization Ideation Agent",
    instructions=PRE_INITIALIZATION_IDEATION_INSTRUCTIONS,
    model="gpt-4.1-mini",  # Using the same model as other agents in the project
    # model_settings=ModelSettings(temperature=0.7), # Optional: can be adjusted for more variety
    output_type=ThematicNameLists,
)

# Example test block for direct testing
if __name__ == "__main__":
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
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    dotenv_path = os.path.join(project_root, ".env")
    if not os.path.exists(dotenv_path):
        print(
            f"Error: .env file not found at {dotenv_path}. Please create one with your OPENAI_API_KEY."
        )
    else:
        load_dotenv(dotenv_path=dotenv_path)
        if not os.getenv("OPENAI_API_KEY"):
            print("Error: OPENAI_API_KEY not found in .env file.")
        else:
            print("OPENAI_API_KEY found.")

            # Test themes
            test_themes = [
                "Cyberpunk Dystopia",
                "Victorian London",
                "Wild West Outpost",
            ]

            for theme in test_themes:
                print(f"\n\n===== Testing with theme: {theme} =====")
                try:
                    result = Runner.run_sync(pre_initialization_ideation_agent, input=theme)

                    if result and result.final_output:
                        name_lists = result.final_output_as(ThematicNameLists)
                        print("\nSuccessfully generated ThematicNameLists:")
                        print(
                            f"Generated {len(name_lists.first_names)} first names and {len(name_lists.last_names)} last names."
                        )

                        # Print first few names as a sample
                        print("\nSample of first names:")
                        print(", ".join(name_lists.first_names[:10]))
                        print("\nSample of last names:")
                        print(", ".join(name_lists.last_names[:10]))

                        # Optionally save to JSON file for review
                        output_dir = os.path.join(project_root, "test_outputs")
                        os.makedirs(output_dir, exist_ok=True)
                        output_file = os.path.join(
                            output_dir, f"{theme.replace(' ', '_')}_names.json"
                        )
                        with open(output_file, "w") as f:
                            f.write(name_lists.model_dump_json(indent=2))
                        print(f"\nFull output saved to: {output_file}")
                    else:
                        print("\nAgent run did not produce the expected output or failed.")
                        if result:
                            print(f"Raw output: {result.final_output}")
                except Exception as e:
                    print(f"\nAn error occurred: {e}")
