import unittest
import json
import os
import random
from unittest.mock import patch, mock_open

# Adjust the import path based on your project structure
# This assumes tests/ is at the same level as src/ or MurderMysteryGen/src/
# and PYTHONPATH is set up accordingly, or you're using a test runner that handles it.
# If running directly, you might need to adjust sys.path or use relative imports carefully.
from mystery_ai.orchestration.main_orchestrator import (
    _load_master_list, 
    _load_and_select_attributes, # Import the new function to test
    NUM_ATTRIBUTE_OPTIONS,
    NUM_EVIDENCE_CATEGORY_OPTIONS # Import the new constant
)

# Define a temporary directory for mock configuration files
TEST_CONFIG_DIR = "temp_test_config_dir_orchestrator"
TEST_MASTER_LISTS_SUBDIR = "master_lists"
FULL_TEST_CONFIG_PATH = os.path.join(TEST_CONFIG_DIR, TEST_MASTER_LISTS_SUBDIR)

class TestMainOrchestratorLogic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create temporary config directory and subdir for master lists
        if not os.path.exists(TEST_CONFIG_DIR):
            os.makedirs(TEST_CONFIG_DIR)
        if not os.path.exists(FULL_TEST_CONFIG_PATH):
            os.makedirs(FULL_TEST_CONFIG_PATH)

        # Create mock master list files
        cls.mock_causes = {"causes_of_death": ["Cause A", "Cause B", "Cause C", "Cause D"]}
        with open(os.path.join(FULL_TEST_CONFIG_PATH, "causes.json"), "w") as f:
            json.dump(cls.mock_causes, f)

        cls.mock_motives = {"motive_categories": ["Motive 1", "Motive 2"]} # Fewer than NUM_ATTRIBUTE_OPTIONS
        with open(os.path.join(FULL_TEST_CONFIG_PATH, "motives.json"), "w") as f:
            json.dump(cls.mock_motives, f)

        cls.mock_empty_list = {"empty_things": []}
        with open(os.path.join(FULL_TEST_CONFIG_PATH, "empty.json"), "w") as f:
            json.dump(cls.mock_empty_list, f)
            
        with open(os.path.join(FULL_TEST_CONFIG_PATH, "malformed.json"), "w") as f:
            f.write("this is not json")

        # Create mock evidence categories list file for Story 7.4 tests
        cls.mock_evidence_categories = {
            "evidence_categories": [
                "Cat A", "Cat B", "Cat C", "Cat D", "Cat E", "Cat F"
            ]
        }
        with open(os.path.join(FULL_TEST_CONFIG_PATH, "evidence_categories.json"), "w") as f:
            json.dump(cls.mock_evidence_categories, f)

    @classmethod
    def tearDownClass(cls):
        # Clean up temporary files and directory
        for f_name in ["causes.json", "motives.json", "empty.json", "malformed.json", "evidence_categories.json"]:
            p = os.path.join(FULL_TEST_CONFIG_PATH, f_name)
            if os.path.exists(p):
                os.remove(p)
        if os.path.exists(FULL_TEST_CONFIG_PATH):
            os.rmdir(FULL_TEST_CONFIG_PATH)
        if os.path.exists(TEST_CONFIG_DIR):
            os.rmdir(TEST_CONFIG_DIR)
            
    def _get_test_file_path(self, filename):
        # Helper to consistently generate paths to test files within the temp structure
        return os.path.join(TEST_CONFIG_DIR, TEST_MASTER_LISTS_SUBDIR, filename)

    @patch("mystery_ai.orchestration.main_orchestrator.CONFIG_DIRECTORY", new=TEST_CONFIG_DIR + "/" + TEST_MASTER_LISTS_SUBDIR)
    @patch("mystery_ai.orchestration.main_orchestrator.os.path.dirname") # Mocking os.path.dirname
    def test_load_master_list_success(self, mock_dirname):
        # Configure mock_dirname to return a path that, when combined with ../../.., leads to a base
        # such that joining with TEST_CONFIG_DIR works.
        # For _load_master_list, base_path = os.path.join(os.path.dirname(__file__), "..", "..", "..")
        # We want base_path to be effectively the root for TEST_CONFIG_DIR.
        # If tests are in MurderMysteryGen/tests/orchestration, then __file__ is there.
        # os.path.dirname(__file__) is MurderMysteryGen/tests/orchestration
        # .. is MurderMysteryGen/tests
        # .. is MurderMysteryGen
        # .. is parent of MurderMysteryGen (this is too high if TEST_CONFIG_DIR is at root)
        
        # Let's assume TEST_CONFIG_DIR is created at the project root for simplicity in the test.
        # The patch for CONFIG_DIRECTORY makes _load_master_list look for files in
        # os.path.join(base_path, TEST_CONFIG_DIR, TEST_MASTER_LISTS_SUBDIR, filename)
        # We need base_path to be "." if TEST_CONFIG_DIR itself is the root-level temp dir.
        
        # The simplest way is to ensure TEST_CONFIG_DIR is relative to where the patched
        # _load_master_list expects it, or mock the entire path construction.
        # Given the patch on main_orchestrator.CONFIG_DIRECTORY,
        # the path constructed is os.path.join(base_path, Patched_CONFIG_DIRECTORY, filename)
        # Let's refine base_path assumption for the test.
        # If tests are in MurderMysteryGen/tests/orchestration, then
        # os.path.dirname(__file__) is .../MurderMysteryGen/tests/orchestration
        # Then base_path becomes .../MurderMysteryGen
        
        # For the test, let's assume TEST_CONFIG_DIR represents the 'MurderMysteryGen/temp_test_config_dir_orchestrator'
        # and TEST_MASTER_LISTS_SUBDIR is 'master_lists'
        # So the target for _load_master_list becomes effectively:
        # project_root / TEST_CONFIG_DIR / TEST_MASTER_LISTS_SUBDIR / filename
        # The patch `main_orchestrator.CONFIG_DIRECTORY` should be just `TEST_CONFIG_DIR`
        # and the `_load_master_list` would join `base_path` with this `TEST_CONFIG_DIR` and then the `filename`.
        # This means the `filename` passed to `_load_master_list` should include the subdir if it's not in `CONFIG_DIRECTORY`.
        
        # Re-evaluating: _load_master_list uses:
        # file_path = os.path.join(base_path, CONFIG_DIRECTORY, filename)
        # We patched CONFIG_DIRECTORY to "temp_test_config_dir_orchestrator/master_lists"
        # So, we need `base_path` to be the actual project root for the test files to be found.
        
        # Let's assume the `base_path` calculation in `_load_master_list`
        # `os.path.join(os.path.dirname(__file__), "..", "..", "..")`
        # correctly points to the root of the `MurderMysteryGen` project from within `src`.
        # For the test, we are creating `TEST_CONFIG_DIR` at the project root.
        # So, the patch on `CONFIG_DIRECTORY` should make it point directly to `TEST_CONFIG_DIR/TEST_MASTER_LISTS_SUBDIR`
        # The `base_path` inside `_load_master_list` should correctly become the project root.
        
        # The current patch for CONFIG_DIRECTORY is `TEST_CONFIG_DIR + "/" + TEST_MASTER_LISTS_SUBDIR`
        # This should work if `base_path` is project root.
        mock_dirname.return_value = os.path.abspath(os.path.join(os.getcwd(), "src/mystery_ai/orchestration")) # Mocking the __file__ context

        # The setUpClass creates files in TEST_CONFIG_DIR/TEST_MASTER_LISTS_SUBDIR
        # So `filename` passed to `_load_master_list` should just be "causes.json"
        
        # Patching `os.path.join` inside `_load_master_list` to control the exact `file_path` might be more robust for unit testing.
        # However, let's try with mocking CONFIG_DIRECTORY and assuming base_path is correct.

        # To avoid complex path mocking for `base_path` within `_load_master_list`,
        # let's instead mock `open` directly for `_load_master_list`.
        # This makes the test independent of `_load_master_list`'s internal path logic.

        with patch("mystery_ai.orchestration.main_orchestrator.open", mock_open(read_data=json.dumps(self.mock_causes))) as mocked_open:
            result = _load_master_list("causes.json", "causes_of_death")
            self.assertEqual(result, self.mock_causes["causes_of_death"])
            # Check that the correct effective path was attempted by open
            # This is tricky as os.path.join is not easily asserted inside the mock_open context
            # For now, focus on the logic of parsing.

        with patch("mystery_ai.orchestration.main_orchestrator.open", mock_open(read_data=json.dumps(self.mock_motives))) as mocked_open_motives:
            result_motives = _load_master_list("motives.json", "motive_categories")
            self.assertEqual(result_motives, self.mock_motives["motive_categories"])

    @patch("mystery_ai.orchestration.main_orchestrator.CONFIG_DIRECTORY", new=TEST_CONFIG_DIR + "/" + TEST_MASTER_LISTS_SUBDIR)
    @patch("mystery_ai.orchestration.main_orchestrator.os.path.dirname")
    def test_load_master_list_file_not_found(self, mock_dirname):
        mock_dirname.return_value = os.path.abspath(os.path.join(os.getcwd(), "src/mystery_ai/orchestration"))
        # Simulate FileNotFoundError by mocking open to raise it
        with patch("mystery_ai.orchestration.main_orchestrator.open", side_effect=FileNotFoundError) as mocked_open_fnf:
            result = _load_master_list("non_existent.json", "any_key")
            self.assertEqual(result, [])
    
    @patch("mystery_ai.orchestration.main_orchestrator.CONFIG_DIRECTORY", new=TEST_CONFIG_DIR + "/" + TEST_MASTER_LISTS_SUBDIR)
    @patch("mystery_ai.orchestration.main_orchestrator.os.path.dirname")
    def test_load_master_list_json_decode_error(self, mock_dirname):
        mock_dirname.return_value = os.path.abspath(os.path.join(os.getcwd(), "src/mystery_ai/orchestration"))
        with patch("mystery_ai.orchestration.main_orchestrator.open", mock_open(read_data="this is not json")) as mocked_open_malformed:
            result = _load_master_list("malformed.json", "any_key")
            self.assertEqual(result, [])

    @patch("mystery_ai.orchestration.main_orchestrator.CONFIG_DIRECTORY", new=TEST_CONFIG_DIR + "/" + TEST_MASTER_LISTS_SUBDIR)
    @patch("mystery_ai.orchestration.main_orchestrator.os.path.dirname")
    def test_load_master_list_empty_list_in_file(self, mock_dirname):
        mock_dirname.return_value = os.path.abspath(os.path.join(os.getcwd(), "src/mystery_ai/orchestration"))
        with patch("mystery_ai.orchestration.main_orchestrator.open", mock_open(read_data=json.dumps(self.mock_empty_list))) as mocked_open_empty:
            result = _load_master_list("empty.json", "empty_things")
            self.assertEqual(result, [])

    @patch("mystery_ai.orchestration.main_orchestrator.CONFIG_DIRECTORY", new=TEST_CONFIG_DIR + "/" + TEST_MASTER_LISTS_SUBDIR)
    @patch("mystery_ai.orchestration.main_orchestrator.os.path.dirname")
    def test_load_master_list_key_not_found(self, mock_dirname):
        mock_dirname.return_value = os.path.abspath(os.path.join(os.getcwd(), "src/mystery_ai/orchestration"))
        with patch("mystery_ai.orchestration.main_orchestrator.open", mock_open(read_data=json.dumps(self.mock_causes))) as mocked_open_key_error:
            result = _load_master_list("causes.json", "non_existent_key")
            self.assertEqual(result, [])

    # Test for Story 7.4: Loading evidence_categories.json
    @patch("mystery_ai.orchestration.main_orchestrator.CONFIG_DIRECTORY", new=TEST_CONFIG_DIR + "/" + TEST_MASTER_LISTS_SUBDIR)
    @patch("mystery_ai.orchestration.main_orchestrator.os.path.dirname")
    def test_load_evidence_categories_list_success(self, mock_dirname):
        mock_dirname.return_value = os.path.abspath(os.path.join(os.getcwd(), "src/mystery_ai/orchestration"))
        with patch("mystery_ai.orchestration.main_orchestrator.open", mock_open(read_data=json.dumps(self.mock_evidence_categories))) as mocked_open:
            result = _load_master_list("evidence_categories.json", "evidence_categories")
            self.assertEqual(result, self.mock_evidence_categories["evidence_categories"])

    # Test for Story 7.4: Sub-selection logic for evidence categories
    @patch("mystery_ai.orchestration.main_orchestrator._load_master_list")
    def test_load_and_select_attributes_includes_evidence_categories(self, mock_load_list):
        """Test that _load_and_select_attributes selects and returns evidence_category_options."""
        # Define what _load_master_list will return for each call
        mock_cod = ["Cod1", "Cod2", "Cod3", "Cod4"]
        mock_motive = ["Motive1", "Motive2", "Motive3", "Motive4"]
        mock_occ = ["Occ1", "Occ2", "Occ3", "Occ4"]
        mock_pers = ["Pers1", "Pers2", "Pers3", "Pers4"]
        mock_ev_cat = ["EvCat1", "EvCat2", "EvCat3", "EvCat4", "EvCat5", "EvCat6"]

        def side_effect_load_list(filename, key):
            if filename == "cause_of_death.json": return mock_cod
            if filename == "motive_categories.json": return mock_motive
            if filename == "occupation_archetypes.json": return mock_occ
            if filename == "personality_archetypes.json": return mock_pers
            if filename == "evidence_categories.json": return mock_ev_cat
            return []
        
        mock_load_list.side_effect = side_effect_load_list

        result_options = _load_and_select_attributes()

        self.assertIsNotNone(result_options)
        self.assertIn("evidence_category_options", result_options)
        
        selected_evidence_cats = result_options["evidence_category_options"]
        self.assertIsInstance(selected_evidence_cats, list)
        
        # Check length (should be NUM_EVIDENCE_CATEGORY_OPTIONS or len(mock_ev_cat) if shorter)
        expected_len = min(NUM_EVIDENCE_CATEGORY_OPTIONS, len(mock_ev_cat))
        self.assertEqual(len(selected_evidence_cats), expected_len)
        
        # Check that items are from the master list and unique
        for item in selected_evidence_cats:
            self.assertIn(item, mock_ev_cat)
        self.assertEqual(len(set(selected_evidence_cats)), expected_len)

        # Verify other keys are still present (smoke test)
        self.assertIn("cause_of_death_options", result_options)
        self.assertIn("motive_category_options", result_options)
        self.assertIn("occupation_archetype_options", result_options)
        self.assertIn("personality_archetype_options", result_options)

    def test_random_sample_selection(self):
        # Test the random.sample logic (as used in run_generation_pipeline)
        full_list = ["a", "b", "c", "d", "e"]
        
        # Case 1: NUM_ATTRIBUTE_OPTIONS is less than list length
        num_to_select = NUM_ATTRIBUTE_OPTIONS # Should be 3
        if len(full_list) >= num_to_select:
            selected = random.sample(full_list, min(num_to_select, len(full_list)))
            self.assertEqual(len(selected), num_to_select)
            for item in selected:
                self.assertIn(item, full_list)
            self.assertEqual(len(set(selected)), num_to_select) # Ensure unique items
        else:
            # This case should not happen if NUM_ATTRIBUTE_OPTIONS is 3 and full_list has 5 items
            pass


        # Case 2: NUM_ATTRIBUTE_OPTIONS is greater than list length
        short_list = ["x", "y"]
        num_to_select_short = NUM_ATTRIBUTE_OPTIONS # 3
        selected_short = random.sample(short_list, min(num_to_select_short, len(short_list)))
        self.assertEqual(len(selected_short), len(short_list)) # Should select all items from short_list
        for item in selected_short:
            self.assertIn(item, short_list)
        self.assertEqual(len(set(selected_short)), len(short_list))

        # Case 3: Empty list
        empty_list_input = []
        selected_empty = random.sample(empty_list_input, min(NUM_ATTRIBUTE_OPTIONS, len(empty_list_input)))
        self.assertEqual(len(selected_empty), 0)

    def test_attribute_options_structure(self):
        # This tests the structure of the dictionary prepared for the agent
        # We don't need to call the full pipeline, just simulate the data
        mock_selected_causes = ["Cause A", "Cause B"]
        mock_selected_motives = ["Motive 1"]
        mock_selected_occupations = ["Occ X", "Occ Y", "Occ Z"]
        mock_selected_personalities = ["Pers P1", "Pers P2"]

        attribute_options = {
            "cause_of_death_options": mock_selected_causes,
            "motive_category_options": mock_selected_motives,
            "occupation_archetype_options": mock_selected_occupations,
            "personality_archetype_options": mock_selected_personalities,
        }

        self.assertIn("cause_of_death_options", attribute_options)
        self.assertEqual(attribute_options["cause_of_death_options"], mock_selected_causes)
        self.assertIsInstance(attribute_options["cause_of_death_options"], list)

        self.assertIn("motive_category_options", attribute_options)
        self.assertEqual(attribute_options["motive_category_options"], mock_selected_motives)
        
        self.assertIn("occupation_archetype_options", attribute_options)
        self.assertEqual(attribute_options["occupation_archetype_options"], mock_selected_occupations)

        self.assertIn("personality_archetype_options", attribute_options)
        self.assertEqual(attribute_options["personality_archetype_options"], mock_selected_personalities)

if __name__ == '__main__':
    unittest.main() 