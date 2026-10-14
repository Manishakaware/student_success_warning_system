"""Dataset loading and leakage-safe preprocessing utilities."""
from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "student-mat.csv"
TARGET_COLUMN = "G3"
RANDOM_STATE = 42
GRADE_FEATURES = ["G1", "G2"]

def load_dataset(data_path=DATA_PATH):
    data_path = Path(data_path)
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found at {data_path}. Run `python src/download_data.py`.")
    data = pd.read_csv(data_path, sep=";")
    if TARGET_COLUMN not in data.columns or data.empty:
        raise ValueError("Dataset must be non-empty and include G3.")
    return data

def split_features_target(data, include_prior_grades=True):
    features = data.drop(columns=[TARGET_COLUMN]).copy()
    if not include_prior_grades:
        features = features.drop(columns=GRADE_FEATURES)
    return features, data[TARGET_COLUMN].copy()

def build_preprocessor(features):
    numeric = features.select_dtypes(include=["number"]).columns.tolist()
    categorical = [column for column in features.columns if column not in numeric]
    return ColumnTransformer([
        ("numeric", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric),
        ("categorical", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), categorical),
    ], verbose_feature_names_out=False)
