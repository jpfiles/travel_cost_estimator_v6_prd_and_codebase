import copy
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO
from pathlib import Path

from storage import load_travel_request, save_travel_request
from travel_model import create_travel_request


class TestTravelRequestStorage(unittest.TestCase):

    def setUp(self):
        """Create an isolated temporary directory for every test."""
        self.temp_directory = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_directory.name)
        self.trip = create_travel_request()

        self.trip["traveler"]["name"] = "Jonah Pickens"
        self.trip["traveler"]["destination"] = "Honolulu, Hawaii"
        self.trip["traveler"]["departure_date"] = "07/10/2026"
        self.trip["traveler"]["return_date"] = "07/15/2026"

    def tearDown(self):
        """Delete the temporary directory after every test."""
        self.temp_directory.cleanup()

    @staticmethod
    def run_without_console_output(function, *args):
        """
        Run a function while suppressing expected console output.

        This keeps tests for expected storage errors from cluttering
        the unittest results.
        """
        with redirect_stdout(StringIO()):
            return function(*args)

    def test_save_creates_json_file(self):
        file_path = self.temp_path / "trip.json"

        result = save_travel_request(
            self.trip,
            file_path,
        )

        self.assertTrue(result)
        self.assertTrue(file_path.exists())
        self.assertTrue(file_path.is_file())

    def test_saved_file_contains_valid_json(self):
        file_path = self.temp_path / "trip.json"

        save_travel_request(
            self.trip,
            file_path,
        )

        with file_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            saved_data = json.load(file)

        self.assertEqual(
            saved_data["traveler"]["name"],
            "Jonah Pickens",
        )
        self.assertEqual(
            saved_data["traveler"]["destination"],
            "Honolulu, Hawaii",
        )
        self.assertEqual(
            saved_data["metadata"]["version"],
            "6.0",
        )

    def test_save_assigns_created_timestamp(self):
        file_path = self.temp_path / "trip.json"

        self.assertEqual(
            self.trip["metadata"]["created"],
            "",
        )

        save_travel_request(
            self.trip,
            file_path,
        )

        created = self.trip["metadata"]["created"]

        self.assertNotEqual(created, "")
        datetime.fromisoformat(created)

    def test_save_assigns_last_modified_timestamp(self):
        file_path = self.temp_path / "trip.json"

        self.assertEqual(
            self.trip["metadata"]["last_modified"],
            "",
        )

        save_travel_request(
            self.trip,
            file_path,
        )

        last_modified = self.trip[
            "metadata"
        ]["last_modified"]

        self.assertNotEqual(last_modified, "")
        datetime.fromisoformat(last_modified)

    def test_save_preserves_existing_created_timestamp(self):
        file_path = self.temp_path / "trip.json"
        original_created = "2026-01-10T08:30:00"

        self.trip["metadata"]["created"] = (
            original_created
        )

        save_travel_request(
            self.trip,
            file_path,
        )

        self.assertEqual(
            self.trip["metadata"]["created"],
            original_created,
        )

    def test_save_updates_last_modified_timestamp(self):
        file_path = self.temp_path / "trip.json"
        original_modified = "2026-01-10T08:30:00"

        self.trip["metadata"]["last_modified"] = (
            original_modified
        )

        save_travel_request(
            self.trip,
            file_path,
        )

        updated_modified = self.trip[
            "metadata"
        ]["last_modified"]

        self.assertNotEqual(
            updated_modified,
            original_modified,
        )
        datetime.fromisoformat(updated_modified)

    def test_save_rejects_non_json_extension(self):
        file_path = self.temp_path / "trip.txt"
        original_metadata = copy.deepcopy(
            self.trip["metadata"]
        )

        result = self.run_without_console_output(
            save_travel_request,
            self.trip,
            file_path,
        )

        self.assertFalse(result)
        self.assertFalse(file_path.exists())
        self.assertEqual(
            self.trip["metadata"],
            original_metadata,
        )

    def test_failed_save_does_not_change_metadata(self):
        file_path = (
            self.temp_path
            / "missing_directory"
            / "trip.json"
        )

        original_metadata = copy.deepcopy(
            self.trip["metadata"]
        )

        result = self.run_without_console_output(
            save_travel_request,
            self.trip,
            file_path,
        )

        self.assertFalse(result)
        self.assertEqual(
            self.trip["metadata"],
            original_metadata,
        )

    def test_save_and_load_round_trip(self):
        file_path = self.temp_path / "trip.json"

        save_result = save_travel_request(
            self.trip,
            file_path,
        )
        loaded_trip = load_travel_request(
            file_path
        )

        self.assertTrue(save_result)
        self.assertIsNotNone(loaded_trip)
        self.assertEqual(loaded_trip, self.trip)

    def test_load_returns_saved_travel_request(self):
        file_path = self.temp_path / "trip.json"

        with file_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.trip,
                file,
                indent=4,
            )

        loaded_trip = load_travel_request(
            file_path
        )

        self.assertIsNotNone(loaded_trip)
        self.assertEqual(
            loaded_trip["traveler"]["name"],
            "Jonah Pickens",
        )
        self.assertEqual(
            loaded_trip["traveler"]["destination"],
            "Honolulu, Hawaii",
        )

    def test_load_rejects_non_json_extension(self):
        file_path = self.temp_path / "trip.txt"
        file_path.write_text(
            "{}",
            encoding="utf-8",
        )

        result = self.run_without_console_output(
            load_travel_request,
            file_path,
        )

        self.assertIsNone(result)

    def test_load_missing_file_returns_none(self):
        file_path = self.temp_path / "missing.json"

        result = self.run_without_console_output(
            load_travel_request,
            file_path,
        )

        self.assertIsNone(result)

    def test_load_invalid_json_returns_none(self):
        file_path = self.temp_path / "invalid.json"
        file_path.write_text(
            "{this is not valid JSON}",
            encoding="utf-8",
        )

        result = self.run_without_console_output(
            load_travel_request,
            file_path,
        )

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()