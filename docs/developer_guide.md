# Developer Guide

This guide provides information for developers working on the Mystery.AI system, including how to manage master lists and configurable parameters.

## 1. Managing Master Lists

Master lists are used by the system to provide diverse options for various generated elements like victim attributes, suspect attributes, and evidence types. These lists are designed to be easily editable by developers to expand or customize the generation possibilities.

### Location and Format

All master lists are stored as JSON files within the `MurderMysteryGen/config/master_lists/` directory.

Each JSON file typically contains a single key, which is an array of strings. The key name usually reflects the content of the list (e.g., `"causes_of_death"`, `"evidence_categories"`).

**Example (`evidence_categories.json`):**
```json
{
  "evidence_categories": [
    "Personal Correspondence (Letter, Email, Diary Entry)",
    "Official Document (Police Report, Certificate, Will)",
    // ... more categories ...
  ]
}
```

### Currently Used Master Lists:

-   `cause_of_death.json`: Contains categories for causes of death.
-   `motive_categories.json`: Contains categories for suspect motives.
-   `occupation_archetypes.json`: Contains generic occupation archetypes.
-   `personality_archetypes.json`: Contains generic personality archetypes.
-   `evidence_categories.json`: Contains types/categories of evidence.

### How to Update Master Lists

1.  **Locate the File:** Navigate to `MurderMysteryGen/config/master_lists/` and open the relevant JSON file (e.g., `occupation_archetypes.json`).
2.  **Edit the List:**
    *   **To Add an Item:** Add a new string to the JSON array under the main key. Ensure it's a valid JSON string (e.g., enclosed in double quotes, with commas separating items).
    *   **To Remove an Item:** Delete the string entry from the array. Be mindful of commas to maintain valid JSON syntax.
    *   **To Modify an Item:** Edit the existing string directly.
3.  **Save the File:** Ensure the file is saved with UTF-8 encoding.

**Important Considerations:**
-   Ensure the JSON syntax remains valid after editing. You can use a JSON validator to check.
-   The descriptive text within the list items is often used by the LLM agents. Clear, concise, and evocative descriptions generally yield better results.
-   Adding too many highly similar items might not significantly increase perceived diversity in generated outputs.

## 2. Configurable Parameters

Several parameters that influence the generation process are managed as constants at the top of the `src/mystery_ai/orchestration/main_orchestrator.py` file. This allows for easy tweaking by developers.

### Location

Open `src/mystery_ai/orchestration/main_orchestrator.py`.
The relevant constants are typically defined near the top of the file, after imports and logger setup.

### Key Configurable Parameters:

-   `NUM_ATTRIBUTE_OPTIONS = 3`
    -   **Description:** The number of options (e.g., for cause of death, motive, occupation, personality) randomly selected from their respective master lists to be provided to the `CaseInitializationAgent` and `SuspectGenerationAgent`.
    -   **How to Change:** Modify the integer value.
-   `VICTIM_NAME_SAMPLE_SIZE = 3`
    -   **Description:** The number of first names and last names to be randomly sampled from the thematically generated name lists to be provided as options to the `CaseInitializationAgent`.
    -   **How to Change:** Modify the integer value.
-   `SUSPECT_NAME_SAMPLE_SIZE = 8`
    -   **Description:** The number of first names and last names to be randomly sampled from the thematically generated name lists to be provided as options to the `SuspectGenerationAgent`.
    -   **How to Change:** Modify the integer value.
-   `NUM_EVIDENCE_CATEGORY_OPTIONS = 5`
    -   **Description:** The number of evidence categories randomly selected from the `evidence_categories.json` master list to be provided as options to the `EvidenceGenerationAgent` for each piece of evidence it generates.
    -   **How to Change:** Modify the integer value.

### Other Configuration Points:

-   **Number of Thematic Names:** The `PreInitializationIdeationAgent` is currently prompted to generate a specific number of thematic first and last names (e.g., "50"). To change this, the agent's instructions in `src/mystery_ai/agents/pre_initialization_ideation_agent.py` would need to be modified directly.
-   **Number of Suspects:** The `SuspectGenerationAgent` is prompted to generate "2 to 3 unique suspect profiles." This is defined in its instructions in `src/mystery_ai/agents/suspect_generator.py`.
-   **Number of Evidence Items per Suspect:** The `EvidenceGenerationAgent` is prompted to generate "1-3 distinct pieces of evidence" per suspect. This is defined in its instructions in `src/mystery_ai/agents/evidence_generator.py`.

To change these, the respective agent instruction strings need to be updated. 