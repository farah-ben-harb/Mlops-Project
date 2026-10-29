"""Structural checks for the small, synthetic training dataset."""

import csv
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "profiles.csv"
EXPECTED_COLUMNS = {"id", "skills", "domain"}
EXPECTED_DOMAINS = {"Backend", "DevOps", "MLOps"}


def validate_dataset(path: Path = DATA_PATH) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        if not EXPECTED_COLUMNS.issubset(columns):
            raise ValueError(f"Missing dataset columns: {EXPECTED_COLUMNS - columns}")
        rows = list(reader)

    if len(rows) < 30:
        raise ValueError("Dataset must contain at least 30 rows")
    if any(not row["skills"].strip() or not row["domain"].strip() for row in rows):
        raise ValueError("Dataset contains empty skills or domain values")
    if len({row["id"] for row in rows}) != len(rows):
        raise ValueError("Dataset IDs must be unique")
    domains = Counter(row["domain"] for row in rows)
    if set(domains) != EXPECTED_DOMAINS or min(domains.values()) < 3:
        raise ValueError(f"Unexpected domain distribution: {dict(domains)}")
    return rows


def main() -> None:
    rows = validate_dataset()
    domains = Counter(row["domain"] for row in rows)
    print(f"Dataset validation passed: {len(rows)} rows; {dict(domains)}")


if __name__ == "__main__":
    main()
