from pathlib import Path

import pytest

from ml.validate_data import validate_dataset


def test_dataset_has_expected_distribution():
    rows = validate_dataset()
    assert len(rows) == 30


def test_dataset_rejects_duplicate_ids(tmp_path):
    path = Path(tmp_path / "profiles.csv")
    path.write_text(
        "id,skills,domain\n" + "\n".join("1,Python,Backend" for _ in range(30)),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="IDs"):
        validate_dataset(path)
