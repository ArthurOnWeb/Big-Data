from __future__ import annotations
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename: str):
    """Load a JSON file from the data directory."""
    path = DATA_DIR / filename
    with open(path, "r") as fh:
        return json.load(fh)


def load_json_lines(filename: str):
    """Load a newline delimited JSON file from the data directory."""
    path = DATA_DIR / filename
    items = []
    with open(path, "r") as fh:
        for line in fh:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items
