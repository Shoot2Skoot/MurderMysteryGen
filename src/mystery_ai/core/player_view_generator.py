import logging # Import the logging module
import random
from typing import List, Optional
from pydantic import BaseModel # Import BaseModel

from ..core.data_models import CaseContext, VictimProfile, SuspectProfile, EvidenceItem # SuspectProfile is not used here directly but good for context if needed

# Define the Pydantic model for PlayerViewData first, as it will be the return type for extraction
class PlayerViewSuspect(BaseModel):
    """Minimal suspect details for player view."""
    name: str
    description: str
    relationship_to_victim: str

class PlayerViewData(BaseModel):
    """Holds the data extracted and shuffled for the player view."""
    theme: str
    victim: VictimProfile # Full victim profile is usually fine for players
    shuffled_suspects: List[PlayerViewSuspect]
    shuffled_evidence_descriptions: List[str]

logger = logging.getLogger(__name__)

def extract_player_view_data(case_context: CaseContext) -> PlayerViewData:
    """Extracts and prepares data specifically for the player view, excluding sensitive info."""
    logger.debug("Extracting data for player view...")
    
    # Extract victim details (already a Pydantic model, so can be used directly)
    victim_details = case_context.victim
    if not victim_details: # Should not happen if pipeline ran correctly
        logger.error("Victim details are missing from CaseContext for player view.")
        # Create a placeholder or handle error appropriately
        victim_details = VictimProfile(name="N/A", occupation="N/A", personality="N/A", cause_of_death="N/A")

    # Extract limited suspect information
    player_suspects: List[PlayerViewSuspect] = []
    if case_context.suspects:
        for s in case_context.suspects:
            player_suspects.append(
                PlayerViewSuspect(
                    name=s.profile.name,
                    description=s.profile.description,
                    relationship_to_victim=s.profile.relationship_to_victim
                )
            )
    
    # Extract only evidence descriptions
    evidence_descriptions: List[str] = []
    if case_context.evidence_items:
        for ev in case_context.evidence_items:
            evidence_descriptions.append(ev.description)
            
    return PlayerViewData(
        theme=case_context.theme,
        victim=victim_details,
        shuffled_suspects=player_suspects, # Will be shuffled by the calling function
        shuffled_evidence_descriptions=evidence_descriptions # Will be shuffled by the calling function
    )

def format_player_view_markdown(player_view_data: PlayerViewData) -> str:
    """Formats the extracted and shuffled player view data into a Markdown string."""
    logger.debug("Formatting player view data into Markdown...")
    lines = []
    lines.append(f"# The Case of the {player_view_data.theme} Mystery")
    lines.append("\n## The Victim")
    lines.append(f"- **Name:** {player_view_data.victim.name}")
    lines.append(f"- **Occupation:** {player_view_data.victim.occupation}")
    lines.append(f"- **Personality:** {player_view_data.victim.personality}")
    lines.append(f"- **Cause of Death:** {player_view_data.victim.cause_of_death}")
    
    lines.append("\n## The Suspects")
    lines.append("*(In no particular order)*")
    if player_view_data.shuffled_suspects:
        for s_profile in player_view_data.shuffled_suspects:
            lines.append(f"- **{s_profile.name}:** {s_profile.description} Relationship to Victim: {s_profile.relationship_to_victim}")
    else:
        lines.append("- *No suspects to display.*")
        
    lines.append("\n## The Evidence")
    lines.append("*(In no particular order)*")
    if player_view_data.shuffled_evidence_descriptions:
        for i, ev_desc in enumerate(player_view_data.shuffled_evidence_descriptions):
            lines.append(f"{i+1}. {ev_desc}")
    else:
        lines.append("- *No evidence to display.*")
        
    return "\n".join(lines)

def generate_player_view_file(case_context: CaseContext, base_filename_without_ext: str):
    """
    Generates and saves the player view Markdown file.

    Args:
        case_context: The full CaseContext object.
        base_filename_without_ext: The base part of the filename (e.g., "mystery_Theme_Timestamp") 
                                   to ensure player view matches the main JSON.
    """
    logger.info("Generating player view file...")
    try:
        player_data_unshuffled = extract_player_view_data(case_context)
        
        # Shuffle the extracted lists
        shuffled_suspect_list = list(player_data_unshuffled.shuffled_suspects) # Create a mutable copy
        random.shuffle(shuffled_suspect_list)
        
        shuffled_evidence_list = list(player_data_unshuffled.shuffled_evidence_descriptions) # Create a mutable copy
        random.shuffle(shuffled_evidence_list)
        
        # Create final PlayerViewData with shuffled lists
        final_player_data = PlayerViewData(
            theme=player_data_unshuffled.theme,
            victim=player_data_unshuffled.victim,
            shuffled_suspects=shuffled_suspect_list,
            shuffled_evidence_descriptions=shuffled_evidence_list
        )

        markdown_content = format_player_view_markdown(final_player_data)
        
        player_view_filename = f"{base_filename_without_ext}_player_view.md"
        # OUTPUT_DIRECTORY is assumed to be defined and handled by the orchestrator if needed
        # For simplicity here, assuming base_filename_without_ext might already include path to generated_mysteries/
        # Or, the orchestrator constructs the full path.
        # This function will just create the file based on the path it's given.

        with open(player_view_filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        logger.info(f"Successfully wrote player view to: {player_view_filename}")
        
    except Exception as e:
        logger.error(f"Failed to generate player view file: {e}", exc_info=True) 