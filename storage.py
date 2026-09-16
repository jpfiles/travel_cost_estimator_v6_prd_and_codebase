import copy
import json
import tempfile
from datetime import datetime
from pathlib import Path


def save_travel_request(travel_request, file_path):
    """
    Save a travel request dictionary to a JSON file.

    The project metadata is updated only after the file has been
    saved successfully. A temporary file is used to avoid leaving
    a partially written project file if saving fails.

    Args:
        travel_request: The travel request dictionary.
        file_path: Destination JSON file.

    Returns:
        True if the save succeeds. Otherwise, False.
    """

    destination = Path(file_path)

    if destination.suffix.lower() != ".json":
        print(
            "Error saving travel request: "
            "File must be a JSON file."
        )
        return False

    temporary_path = None

    try:
        current_time = datetime.now().isoformat(
            timespec="seconds"
        )

        request_to_save = copy.deepcopy(
            travel_request
        )

        if request_to_save["metadata"]["created"] == "":
            request_to_save["metadata"]["created"] = (
                current_time
            )

        request_to_save["metadata"]["last_modified"] = (
            current_time
        )

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(
                temporary_file.name
            )

            json.dump(
                request_to_save,
                temporary_file,
                indent=4,
            )

        temporary_path.replace(destination)

        travel_request["metadata"]["created"] = (
            request_to_save["metadata"]["created"]
        )
        travel_request["metadata"]["last_modified"] = (
            request_to_save["metadata"]["last_modified"]
        )

        return True

    except (OSError, TypeError, ValueError, KeyError) as error:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass

        print(
            f"Error saving travel request: {error}"
        )
        return False


def load_travel_request(file_path):
    """
    Load a travel request dictionary from a JSON file.

    Args:
        file_path: JSON file to load.

    Returns:
        The loaded travel request dictionary, or None if loading
        fails.
    """

    source = Path(file_path)

    if source.suffix.lower() != ".json":
        print(
            "Error loading travel request: "
            "File must be a JSON file."
        )
        return None

    try:
        with source.open(
            "r",
            encoding="utf-8",
        ) as file:
            travel_request = json.load(file)

        return travel_request

    except FileNotFoundError:
        print(
            "Error loading travel request: "
            "File not found."
        )
        return None

    except PermissionError:
        print(
            "Error loading travel request: "
            "Permission denied."
        )
        return None

    except json.JSONDecodeError:
        print(
            "Error loading travel request: "
            "File contains invalid JSON."
        )
        return None

    except OSError as error:
        print(
            f"Error loading travel request: {error}"
        )
        return None