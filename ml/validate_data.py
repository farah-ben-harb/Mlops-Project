import csv
from collections import Counter
from pathlib import Path

data_path = Path("data/profiles.csv")

with data_path.open(encoding="utf-8") as f:
    reader = csv.DictReader(f)
    assert {"skills", "domain"}.issubset(reader.fieldnames or [])
    rows = list(reader)

assert len(rows) >= 30
assert all(row["skills"].strip() for row in rows)
assert all(row["domain"].strip() for row in rows)

labels = Counter(row["domain"] for row in rows)

assert set(labels) == {"Backend", "DevOps", "MLOps"}
assert min(labels.values()) >= 3

print("Dataset validation passed")
