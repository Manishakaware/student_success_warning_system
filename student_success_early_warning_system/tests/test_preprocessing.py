import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from data_preprocessing import TARGET_COLUMN, load_dataset

def test_dataset_loads_with_required_columns():
    data = load_dataset()
    assert len(data) == 395
    assert {TARGET_COLUMN, "G1", "G2", "studytime", "absences"}.issubset(data.columns)

def test_dataset_has_expected_schema():
    data = load_dataset()
    assert data.shape[1] == 33
    assert data[TARGET_COLUMN].between(0, 20).all()
