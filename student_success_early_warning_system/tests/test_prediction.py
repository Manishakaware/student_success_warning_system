import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from data_preprocessing import load_dataset
from predict import MODEL_PATH, load_model, predict_grade

def test_model_file_loads():
    assert MODEL_PATH.exists()
    assert hasattr(load_model(), "predict")

def test_prediction_is_numeric_and_in_grade_range():
    sample = load_dataset().drop(columns=["G3"]).iloc[0].to_dict()
    prediction = predict_grade(load_model(), sample)
    assert isinstance(prediction, float)
    assert 0 <= prediction <= 20
