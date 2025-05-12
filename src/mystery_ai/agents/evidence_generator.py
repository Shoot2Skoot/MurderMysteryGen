# src/mystery_ai/agents/evidence_generator.py

"""
Evidence Generator Agent for the Murder Mystery Generation system.

This module defines the Evidence Generator Agent, which is responsible for creating
evidence items that point to suspects in the mystery. For each suspect, it generates
plausible evidence items related to their means, motive, or opportunity, with
appropriate consideration for whether they are the actual killer.
"""

from typing import Any, Dict, List

from agents import Agent

from ..core.data_models import CaseContext, EvidenceItem, Suspect  # For full context

EVIDENCE_GENERATOR_AGENT_INSTRUCTIONS = """
You are the Evidence Generation Agent.
Your task is to generate a list of 1-3 distinct pieces of evidence for a *specific suspect* based on the detailed case and suspect context provided in your input.

Input (received as a JSON dictionary):
- `theme`: The overall theme of the mystery.
- `victim_name`: Name of the victim.
- `victim_occupation`: Occupation of the victim.
- `suspect_name`: Name of the specific suspect for whom to generate evidence.
- `is_killer`: Boolean, true if this suspect is the killer, false otherwise.
- `original_means`: The suspect's original means.
- `original_motive`: The suspect's original motive.
- `original_opportunity`: The suspect's original opportunity.
- `modified_element_type_str`: (String, e.g., "means", "motive", "opportunity", or "N/A" if killer) The MMO element that was weakened if the suspect is NOT the killer.
- `modified_element_desc_str`: (String, or "N/A") The description of how the element was weakened.
- `reason_for_modification_str`: (String, or "N/A") The reason the element was weakened.
- `evidence_category_options`: A list of 3-5 potential evidence categories (e.g., "Personal Correspondence", "Forensic Report Snippet") you should choose from for each piece of evidence.

Task:
1.  Analyze all provided input details for the specific suspect.
2.  For each piece of evidence you generate (1-3 items total for this suspect):
    a.  SELECT one `evidence_category` from the provided `evidence_category_options` that best fits the nature of the evidence you are creating. This category determines the *type* or *form* of the evidence.
    b.  Generate a `description` for the evidence item. This `description` is CRITICAL: it should BE the evidence content itself, as if the player is directly observing or reading it. Do NOT just describe the type of evidence or restate the category. **Crucially, try to *imply* the nature of the item through its content rather than using the literal words from the `evidence_category` string in your description.** The category guides you on what *kind* of thing it is; the description is the thing itself. For example:
        -   **Category Selected:** `Personal Correspondence (Letter, Email, Diary Entry)`
            -   **GOOD Description (IS the evidence, implies category):** "A crumpled, tear-stained sheet of stationery found in the victim's waste bin, reading: 'My dearest Alistair, I cannot bear this deception any longer. The guilt consumes me. We must confess everything before it's too late. - E'"
            -   **BAD Description (too literal):** "A letter was found that showed the victim was feeling guilty."
        -   **Category Selected:** `Forensic Report Snippet (Fingerprints, DNA, Ballistics)`
            -   **GOOD Description (IS the evidence, implies category):** "Lab analysis sheet, Case #7B, Section 4: 'Partial latent print lifted from the stem of the antique wine glass matches Subject B, Theron Volkov. Smudging consistent with an attempt to wipe clean.'"
            -   **BAD Description (too literal):** "A forensic report showed Theron Volkov's fingerprints on the wine glass."
        -   **Category Selected:** `Map / Blueprint Fragment`
            -   **GOOD Description (IS the evidence, implies category):** "A tattered, oil-stained piece of drafting vellum, clearly torn from a larger schematic, detailed the conduits and access tunnels around the victim's quarters. A crudely drawn red 'X' marked a junction box near the main airlock."
            -   **BAD Description (too literal):** "A blueprint fragment was found showing the area."
        Make it specific, evocative, and deeply integrated with the theme and the suspect's situation.
    c.  Generate a `narrative_function_description`. This crucial field should explain the evidence's intended role, its subtlety, or how it functions as a clue or red herring. For example: "This letter directly implicates the suspect if the handwriting can be matched.", "A seemingly innocent receipt that becomes incriminating when cross-referenced with the victim's diary.", "This object appears to support the suspect's alibi but is actually misleading due to a hidden detail."
    d.  Determine `points_to_mmo_element` (means, motive, or opportunity).
    e.  Determine `is_red_herring` (boolean).
        - If `is_killer` is TRUE: The evidence should support their guilt (`is_red_herring: false`).
        - If `is_killer` is FALSE: The evidence should be a red herring, making them look suspicious (`is_red_herring: true`). Consider the `modified_element_type_str` to make red herrings effective.
    f.  Provide a brief `connection_explanation` (how the evidence links to the suspect and their MMO element).
3.  Ensure each generated piece of evidence is distinct.

Output Format:
- You MUST output your response as a single, valid JSON list of EvidenceItem objects. Each object must conform to the EvidenceItem schema:
  `description: str`
  `related_suspect_name: str` (This MUST be the `suspect_name` from your input.)
  `points_to_mmo_element: str` (Value must be one of "means", "motive", "opportunity")
  `is_red_herring: bool`
  `connection_explanation: str` (Optional but highly recommended; briefly explain how this evidence links to the suspect and their MMO element.)
  `evidence_category: str` (The category you selected from `evidence_category_options`.)
  `narrative_function_description: str` (Your explanation of the evidence's role/subtlety.)

Example Output (for a killer suspect named 'Silas Blackwood', if 'Personal Correspondence' was chosen as category):
```json
[
  {
    "description": "A hastily scrawled note found in the victim's desk: 'Silas, you will pay for what you did to my family. Your time is coming.' The ink is smudged, as if written in anger or haste.",
    "related_suspect_name": "Silas Blackwood",
    "points_to_mmo_element": "motive",
    "is_red_herring": false,
    "connection_explanation": "The note clearly indicates someone (implied to be Silas, or someone framing him) had a strong vengeful motive against the victim.",
    "evidence_category": "Personal Correspondence (Letter, Email, Diary Entry)",
    "narrative_function_description": "This handwritten note directly establishes a strong vengeful motive pointing towards Silas Blackwood, or suggests someone is trying to frame him."
  }
]
```
Ensure the output is ONLY the JSON list of evidence items for this one suspect.
"""

# For Story 3.2, defining the agent skeleton.
# Orchestrator will call this for each suspect, building up detailed instructions/input.

evidence_generator_agent = Agent(
    name="Evidence Generation Agent",
    instructions=EVIDENCE_GENERATOR_AGENT_INSTRUCTIONS,
    model="gpt-4.1-mini",
    output_type=List[EvidenceItem],
)


# Helper function to prepare input for the EvidenceGenerationAgent for a single suspect
def prepare_evidence_generation_input(
    case_context: CaseContext,  # Contains theme and victim
    suspect: Suspect,  # The specific suspect (with killer status and modified MMO if any)
    evidence_category_options: List[str] # Add parameter for options
) -> Dict[str, Any]:
    """
    Prepares the input dictionary for the Evidence Generation Agent.

    This function takes the overall case context, a specific suspect, and available
    evidence categories, then constructs a dictionary containing all the necessary
    information for the Evidence Generation Agent.

    Args:
        case_context: The main CaseContext object containing theme and victim details.
        suspect: The Suspect object for whom evidence needs to be generated.
        evidence_category_options: A list of evidence category strings to be offered to the agent.

    Returns:
        A dictionary formatted for the Evidence Generation Agent's input.
    """
    modified_element_type_str = "N/A"
    modified_element_desc_str = "N/A"
    reason_for_modification_str = "N/A"

    if not suspect.is_killer and suspect.modified_mmo_elements:
        # For MVP, assume only one element is modified
        if suspect.modified_mmo_elements:  # Check if list is not empty
            mod_element = suspect.modified_mmo_elements[0]
            modified_element_type_str = mod_element.element_type.value
            modified_element_desc_str = mod_element.modified_element_description
            reason_for_modification_str = mod_element.reason_for_modification

    input_dict = {
        "theme": case_context.theme,
        "victim_name": case_context.victim.name if case_context.victim else "N/A",
        "victim_occupation": (case_context.victim.occupation if case_context.victim else "N/A"),
        "suspect_name": suspect.profile.name,
        "is_killer": suspect.is_killer,
        "original_means": suspect.original_mmo.means,
        "original_motive": suspect.original_mmo.motive,
        "original_opportunity": suspect.original_mmo.opportunity,
        "modified_element_type_str": modified_element_type_str,
        "modified_element_desc_str": modified_element_desc_str,
        "reason_for_modification_str": reason_for_modification_str,
        "evidence_category_options": evidence_category_options, # Use passed-in options
    }
    return input_dict

    # The instructions for the agent will be dynamically formatted with these details
    # by the orchestrator, similar to MMOModificationAgent, or this dict is passed as input
    # with more generic agent instructions.
    # For consistency, let's assume the orchestrator will pass this dict as input to the agent.
