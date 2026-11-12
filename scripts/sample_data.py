"""Read the bundled CSV fixture without connecting to a warehouse."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "sample.csv"
CONFIG_FILE = ROOT / "scripts" / "configs.yaml"


def read_sample():
    with DATA_FILE.open(newline="", encoding="utf-8") as source:
        return [
            (row["col1"], int(row["col2"]), float(row["col3"]))
            for row in csv.DictReader(source)
        ]


if __name__ == "__main__":
    rows = read_sample()
    print(f"Validated {len(rows)} sample rows")
