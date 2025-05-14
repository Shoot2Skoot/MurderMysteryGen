from typing import List, Optional, Dict
from pydantic import BaseModel, Field
import json # <--- IMPORT JSON MODULE

# Assuming MMOElementType is defined elsewhere if needed by other models
# from ..core.data_models import MMOElementType # Example import

class Location(BaseModel):
    """Represents a distinct location within the mystery setting."""
    location_id: str = Field(
        description="Unique identifier for the location (e.g., 'loc_library', 'loc_garden')."
    )
    name: str = Field(description="Human-readable name of the location (e.g., 'Library', 'Walled Garden').")
    description: Optional[str] = Field(
        default=None,
        description="Optional description of the location, potentially including features relevant to clues (e.g., 'Dusty, with shelves reaching the ceiling', 'Has a single window overlooking the courtyard')."
    )
    connected_location_ids: List[str] = Field(
        default_factory=list,
        description="List of location IDs directly connected via normal paths (e.g., doors, hallways). Assumed to be two-way unless specified otherwise by game logic."
    )
    secret_connections: Optional[List[Dict[str, str]]] = Field(
        default=None,
        description="Optional list of secret connections, each a dict with 'to_location_id' and 'description' (e.g., {'to_location_id': 'loc_cellar', 'description': 'Hidden trapdoor under rug'})."
    )
    can_be_seen_from_ids: List[str] = Field(
        default_factory=list,
        description="List of location IDs from which *this* location (self) can be seen (e.g., if 'loc_hallway' is in 'loc_kitchen.can_be_seen_from_ids', then from the hallway you can see into the kitchen). Assumed bidirectional unless context implies otherwise."
    )
    can_be_heard_from_ids: List[str] = Field(
        default_factory=list,
        description="List of location IDs from which sounds occurring in *this* location (self) might be heard (e.g., if 'loc_study' is in 'loc_library.can_be_heard_from_ids', sounds in the library can be heard in the study)."
    )

# Raw data from your Villa_Estate_1.py
rooms_data = ["Green","Ocean","Beach","Yoga","Game","Sauna","Pool","Lounge","Night","Mount","Library","Ballroom","Dining","Kitchen","Courtyard","Hall","Entrance","Garden","MasterBed","Study","Mineral","Staff","Conservatory","BathA","BathB","BathC","BathD","BathMaster","ClosetA","ClosetB","ClosetC","ClosetD","ClosetE","c1","c2","c3","c4","c5","c6","c7","c8","c9","c10","c11","c12","c13","c14"]

connections_input = [
    ["c1","c2","c3","c4"], ["c4","c5","Night"], ["c3","c6","BathB","BathC"], ["c6","c7","c8","Game"],
    ["c8","c5","c9","c10"], ["c7","Courtyard"], ["c9","Hall","Courtyard"], ["c11","Garden"],
    ["c11","Courtyard"], ["c12", "Courtyard"], ["c12","c13"], ["c13","c14","Staff"],
    ["c14","Courtyard","Hall"], ["c1","Green"], ["c1","BathA"], ["c1","Ocean"], ["c1","Beach"],
    ["c4","Yoga"], ["c4","Game"], ["c4","Pool"], ["c4","BathD"], ["Pool","Sauna"],
    ["ClosetC","Night"], ["ClosetB","Lounge"], ["c5","Mount"], ["c10","Library"],
    ["c7","Dining"], ["c8","Lounge"], ["c8","Ballroom"], ["c11","MasterBed"],
    ["c13","Mineral","Study"], ["c14","Conservatory","Hall","Courtyard"],
    ["ClosetA","Dining"], ["Kitchen","Courtyard"], ["Ballroom","Courtyard"],
    ["Library","Hall"], ["Hall", "Entrance"], ["ClosetE","Courtyard"],
    ["MasterBed","BathMaster"], ["Mineral","Courtyard"]
]

visibility_input = [
    ["Dining", "Garden"], ["MasterBed", "Garden"], ["Kitchen", "Garden"], ["Beach", "Garden"],
]

# --- Processing Logic ---
adj = {room: set() for room in rooms_data}
for group in connections_input:
    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            room1, room2 = group[i], group[j]
            if room1 in adj and room2 in adj:
                adj[room1].add(room2)
                adj[room2].add(room1)

processed_visibility = {room: set() for room in rooms_data}
for room_a_str, room_b_str in visibility_input:
    if room_a_str in rooms_data and room_b_str in rooms_data:
        processed_visibility[room_b_str].add(room_a_str)
        processed_visibility[room_a_str].add(room_b_str)

processed_hearing = {room: set() for room in rooms_data}
for room1 in rooms_data:
    direct_neighbors = adj.get(room1, set())
    for neighbor in direct_neighbors:
        neighbors_of_neighbor = adj.get(neighbor, set())
        for two_steps_away_room in neighbors_of_neighbor:
            if two_steps_away_room != room1 and two_steps_away_room not in direct_neighbors:
                processed_hearing[room1].add(two_steps_away_room)
                processed_hearing[two_steps_away_room].add(room1)

# --- Generate Location Objects ---
villa_estate_1_locations: List[Location] = []
for room_name in rooms_data:
    loc_id = f"loc_{room_name.lower().replace(' ', '_')}"
    connected_ids = sorted([f"loc_{n.lower().replace(' ', '_')}" for n in adj.get(room_name, [])])
    seen_from_ids = sorted([f"loc_{s.lower().replace(' ', '_')}" for s in processed_visibility.get(room_name, [])])
    heard_from_ids = sorted([f"loc_{h.lower().replace(' ', '_')}" for h in processed_hearing.get(room_name, [])])
    
    villa_estate_1_locations.append(
        Location(
            location_id=loc_id,
            name=room_name,
            description=f"The {room_name}.", 
            connected_location_ids=connected_ids,
            secret_connections=[], 
            can_be_seen_from_ids=seen_from_ids,
            can_be_heard_from_ids=heard_from_ids
        )
    )

# --- Export to JSON file ---
# Convert list of Pydantic models to list of dicts
locations_as_dicts = [loc.model_dump() for loc in villa_estate_1_locations]

# Define the output file path
output_file_path = "MurderMysteryGen/maps/villa_estate_1_processed.json" # <--- DEFINE YOUR PATH

# Write to JSON file
try:
    with open(output_file_path, 'w') as f:
        json.dump(locations_as_dicts, f, indent=4)
    print(f"Successfully exported map data to: {output_file_path}")
except IOError as e:
    print(f"Error writing to file {output_file_path}: {e}")
