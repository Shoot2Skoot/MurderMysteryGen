import unittest
import json
from typing import List, Optional

from pydantic import ValidationError

# Assuming linter and test runner are configured to find 'mystery_ai' from 'src'
from mystery_ai.core.data_models import EvidenceItem, MMOElementType

class TestEvidenceItemModel(unittest.TestCase):
    def test_evidence_item_creation_valid(self):
        """Test successful creation of an EvidenceItem with all fields."""
        evidence_data = {
            "description": "A blood-stained candlestick found in the study.",
            "related_suspect_name": "Professor Plum",
            "points_to_mmo_element": MMOElementType.MEANS,
            "is_red_herring": False,
            "connection_explanation": "This was likely the murder weapon and was found near the Professor's favorite reading chair.",
            "evidence_category": "Physical Object (Weapon, Clothing, Tool)",
            "narrative_function_description": "A direct piece of evidence linking the suspect to the means of the crime."
        }
        try:
            item = EvidenceItem(**evidence_data)
            self.assertEqual(item.description, evidence_data["description"])
            self.assertEqual(item.related_suspect_name, evidence_data["related_suspect_name"])
            self.assertEqual(item.points_to_mmo_element, evidence_data["points_to_mmo_element"])
            self.assertEqual(item.is_red_herring, evidence_data["is_red_herring"])
            self.assertEqual(item.connection_explanation, evidence_data["connection_explanation"])
            self.assertEqual(item.evidence_category, evidence_data["evidence_category"])
            self.assertEqual(item.narrative_function_description, evidence_data["narrative_function_description"])
        except ValidationError as e:
            self.fail(f"EvidenceItem creation failed with valid data: {e}")

    def test_evidence_item_missing_required_fields(self):
        """Test that EvidenceItem raises ValidationError if required fields (including new ones) are missing."""
        # Missing description, evidence_category, narrative_function_description
        invalid_data = {
            "related_suspect_name": "Miss Scarlett",
            "points_to_mmo_element": MMOElementType.MOTIVE,
            "is_red_herring": True,
            "connection_explanation": "Appears to point to motive but is misleading."
        }
        with self.assertRaises(ValidationError):
            EvidenceItem(**invalid_data)

    def test_evidence_item_serialization_deserialization(self):
        """Test JSON serialization and deserialization of EvidenceItem including new fields."""
        evidence_data = {
            "description": "Torn love letter.",
            "related_suspect_name": "Colonel Mustard",
            "points_to_mmo_element": "motive", # Using string value for MMOElementType for JSON
            "is_red_herring": True,
            "connection_explanation": "Suggests a secret affair, a classic red herring.",
            "evidence_category": "Personal Correspondence (Letter, Email, Diary Entry)",
            "narrative_function_description": "This red herring suggests an emotional motive, diverting attention from the real killer."
        }
        item = EvidenceItem(**evidence_data)
        item_json = item.model_dump_json()
        
        rehydrated_item = EvidenceItem.model_validate_json(item_json)

        self.assertEqual(item.description, rehydrated_item.description)
        self.assertEqual(item.related_suspect_name, rehydrated_item.related_suspect_name)
        self.assertEqual(item.points_to_mmo_element, rehydrated_item.points_to_mmo_element)
        self.assertEqual(item.is_red_herring, rehydrated_item.is_red_herring)
        self.assertEqual(item.connection_explanation, rehydrated_item.connection_explanation)
        self.assertEqual(item.evidence_category, rehydrated_item.evidence_category)
        self.assertEqual(item.narrative_function_description, rehydrated_item.narrative_function_description)

    def test_evidence_item_optional_connection_explanation(self):
        """Test EvidenceItem creation when optional connection_explanation is None."""
        evidence_data = {
            "description": "Muddy footprints leading away from the conservatory.",
            "related_suspect_name": "Mrs. Peacock",
            "points_to_mmo_element": MMOElementType.OPPORTUNITY,
            "is_red_herring": False,
            "connection_explanation": None, # Explicitly None
            "evidence_category": "Physical Object (Weapon, Clothing, Tool)", # Example category
            "narrative_function_description": "Indicates someone was present and left in a hurry."
        }
        try:
            item = EvidenceItem(**evidence_data)
            self.assertIsNone(item.connection_explanation)
        except ValidationError as e:
            self.fail(f"EvidenceItem creation failed with connection_explanation=None: {e}")

if __name__ == '__main__':
    unittest.main() 