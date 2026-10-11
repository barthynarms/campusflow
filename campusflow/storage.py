
import json
import os
import tempfile

DEFAULT_PATH = os.path.join("data", "tickets.json")


class StorageError(Exception):
    """Raised when the data file cannot be read safely."""


def load_tickets(path=DEFAULT_PATH):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as error:
        raise StorageError(
            f"{path} is not valid JSON ({error}). Fix or move the file; "
            "it was not changed."
        ) from error
    except OSError as error:
        raise StorageError(f"Could not read {path}: {error}") from error

    if not isinstance(data, list) or not all(isinstance(t, dict) and "id" in t for t in data):
        raise StorageError(
            f"{path} does not contain a list of tickets. It was not changed."
        )
    return data


def save_tickets(path, tickets):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(dir=folder or ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(tickets, f, indent=2)
        os.replace(temp_path, path)
    except Exception:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise