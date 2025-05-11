# MurderMysteryGen/tools/generate_schema.py

import json
import os
import sys

# Add src directory to Python path to allow importing mystery_ai
# This assumes the script is run from the MurderMysteryGen root directory
# or that the mystery_ai package is otherwise findable.
# A more robust way for a real tool might involve package installation or better path management.
SRC_PATH = os.path.join(os.path.dirname(__file__), '..', 'src')
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

try:
    from mystery_ai.core.data_models import CaseContext
except ImportError as e:
    print(f"Error: Could not import CaseContext. Ensure src path is correct and models are defined: {e}")
    print(f"Current sys.path: {sys.path}")
    sys.exit(1)

def main():
    """Generates and prints the JSON schema for the CaseContext Pydantic model."""
    print("Generating JSON schema for CaseContext...\n")
    
    # Pydantic v2 uses model_json_schema()
    schema_dict = CaseContext.model_json_schema() # Get the schema as a dictionary
    
    # The schema itself is a dictionary, print it as a JSON string for easy copy-pasting
    # or for direct use by other tools.
    # print(json.dumps(schema, indent=2)) # This would print it as a string with escaped quotes
    # For direct inclusion in markdown, just printing the dict-derived string is better:
    print("```json")
    # Dump the schema dictionary to a JSON formatted string with indentation
    print(json.dumps(schema_dict, indent=2)) 
    print("```")
    
    # Optionally, save to a file
    # schema_filename = "case_context_schema.json"
    # with open(schema_filename, 'w') as f:
    #     json.dump(schema_dict, f, indent=2) # Use schema_dict here too
    # print(f"\nSchema also saved to {schema_filename}")

if __name__ == "__main__":
    main() 