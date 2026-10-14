"""Prediction helpers used by the application and tests."""
import joblib
import numpy as np
import pandas as pd
from data_preprocessing import PROJECT_ROOT
MODEL_PATH = PROJECT_ROOT / "models" / "student_performance_model.pkl"
def load_model(model_path=MODEL_PATH): return joblib.load(model_path)
def predict_grade(model, student_data):
    return float(np.clip(float(model.predict(pd.DataFrame([student_data]))[0]), 0, 20))
def performance_category(grade):
    if grade >= 16: return "Excellent"
    if grade >= 14: return "Very Good"
    if grade >= 12: return "Good"
    if grade >= 10: return "Average"
    return "At Risk"
def academic_support_indicator(grade):
    if grade < 10: return "Higher Support Need"
    if grade < 12: return "Moderate Support Need"
    return "Lower Support Need"
