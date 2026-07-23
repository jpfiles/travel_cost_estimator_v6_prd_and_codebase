from pathlib import Path
import json
from datetime import datetime

def save_travel_request(travel_request, file_path):
    """
    Save a travel request dictionary to a JSON file.

    Args:
        travel_request: The travel request dictionary.
        file_path: The destination JSON file.

    Returns:
        True if successful, False otherwise.
    """

    try:
        current_time = datetime.now().isoformat(timespec="seconds")

        if travel_request["metadata"]["created"] == "":
            travel_request["metadata"]["created"] = current_time

        travel_request["metadata"]["last_modified"] = current_time

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(
                travel_request,
                file,
                indent=4
            )

        return True

    except Exception as error:
        print(f"Error saving travel request: {error}")
        return False

###############################################################################################################

def load_travel_request(file_path):
    """
    Load a travel request dictionary from a JSON file.

    Args:
        file_path: The JSON file to load.

    Returns:
        The travel request dictionary, or None if loading fails.
    """

    try:
        file_extension = Path(file_path).suffix.lower()

        if file_extension != ".json":
            print("Error loading travel request: File must be a JSON file.")
            return None

        with open(file_path, "r", encoding="utf-8") as file:
            travel_request = json.load(file)

        return travel_request

    except FileNotFoundError:
        print("Error loading travel request: File not found.")
        return None

    except PermissionError:
        print("Error loading travel request: Permission denied.")
        return None

    except json.JSONDecodeError:
        print("Error loading travel request: File contains invalid JSON.")
        return None

    except OSError as error:
        print(f"Error loading travel request: {error}")
        return None

### TEMPORARY TEST BLOCK BELOW ###

loaded_trip = load_travel_request("sample_trip.json")

if loaded_trip is not None:
    print("Traveler:", loaded_trip["traveler"]["name"])
    print("Destination:", loaded_trip["traveler"]["destination"])
    print("Departure:", loaded_trip["traveler"]["departure_date"])
    print("Return:", loaded_trip["traveler"]["return_date"])
else:
    print("Failed to load travel request.")


