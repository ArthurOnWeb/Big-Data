import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import ingestion


def test_load_json():
    data = ingestion.load_json("btc_prices_3_months.json")
    assert isinstance(data, list)
    assert data and "date" in data[0]


def test_load_json_lines():
    items = ingestion.load_json_lines("processData.json")
    assert isinstance(items, list)
    assert items and "date" in items[0]
