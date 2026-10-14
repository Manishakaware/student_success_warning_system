"""Train, compare, and persist student final-grade regression pipelines."""
import json
from pathlib import Path
import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import ExtraTreesRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from data_preprocessing import PROJECT_ROOT, RANDOM_STATE, build_preprocessor, load_dataset, split_features_target

MODELS_DIR = PROJECT_ROOT / "models"; REPORTS_DIR = PROJECT_ROOT / "reports"; FIGURES_DIR = REPORTS_DIR / "figures"

def candidates():
    return {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=350, min_samples_leaf=2, random_state=RANDOM_STATE, n_jobs=-1),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=200, learning_rate=0.04, max_depth=2, loss="huber", random_state=RANDOM_STATE),
        "Extra Trees": ExtraTreesRegressor(n_estimators=350, min_samples_leaf=2, random_state=RANDOM_STATE, n_jobs=-1),
    }

def score(y_true, predictions):
    return {"MAE": mean_absolute_error(y_true, predictions), "RMSE": mean_squared_error(y_true, predictions) ** 0.5, "R2": r2_score(y_true, predictions)}

def fit_compare(data, include_prior_grades=True):
    X, y = split_features_target(data, include_prior_grades)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)
    records, fitted = [], {}
    for name, estimator in candidates().items():
        pipe = Pipeline([("preprocessor", build_preprocessor(X)), ("model", estimator)])
        pipe.fit(X_train, y_train)
        metrics = score(y_test, pipe.predict(X_test))
        records.append({"Model": name, **metrics})
        fitted[name] = pipe
    results = pd.DataFrame(records).sort_values(["RMSE", "MAE"], ignore_index=True)
    return results, fitted, X_test, y_test

def save_plots(results, best_pipe, X_test, y_test):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", palette="deep")
    fig, axis = plt.subplots(figsize=(8, 4.5)); sns.barplot(data=results, x="RMSE", y="Model", ax=axis); axis.set_title("Model Comparison: Lower RMSE Is Better"); fig.tight_layout(); fig.savefig(FIGURES_DIR / "model_comparison.png", dpi=180); plt.close(fig)
    predictions = best_pipe.predict(X_test)
    fig, axis = plt.subplots(figsize=(5.5, 5)); axis.scatter(y_test, predictions, alpha=.72, color="#2563eb"); axis.plot([0,20],[0,20],"--",color="#ef4444"); axis.set(xlabel="Actual G3", ylabel="Predicted G3", title="Actual vs Predicted Final Grade"); fig.tight_layout(); fig.savefig(FIGURES_DIR / "actual_vs_predicted.png", dpi=180); plt.close(fig)
    transformed = best_pipe.named_steps["preprocessor"].get_feature_names_out()
    model = best_pipe.named_steps["model"]
    importances = model.feature_importances_ if hasattr(model, "feature_importances_") else abs(model.coef_)
    importance = pd.DataFrame({"Feature": transformed, "Importance": importances}).sort_values("Importance", ascending=False).head(15).sort_values("Importance")
    fig, axis = plt.subplots(figsize=(8, 5.5)); axis.barh(importance.Feature, importance.Importance, color="#14b8a6"); axis.set(title="Top Model Features", xlabel="Importance"); fig.tight_layout(); fig.savefig(FIGURES_DIR / "feature_importance.png", dpi=180); plt.close(fig)
    fig, axis = plt.subplots(figsize=(6.5, 4)); residuals = y_test - predictions; axis.scatter(predictions, residuals, alpha=.7, color="#7c3aed"); axis.axhline(0, color="black", linewidth=1); axis.set(xlabel="Predicted G3", ylabel="Residual", title="Residual Plot"); fig.tight_layout(); fig.savefig(FIGURES_DIR / "residuals.png", dpi=180); plt.close(fig)
    return importance.sort_values("Importance", ascending=False)

def main():
    data = load_dataset(); MODELS_DIR.mkdir(exist_ok=True); REPORTS_DIR.mkdir(exist_ok=True)
    results, fitted, X_test, y_test = fit_compare(data, True)
    best_name = results.iloc[0]["Model"]; best_pipe = fitted[best_name]
    joblib.dump(best_pipe, MODELS_DIR / "student_performance_model.pkl")
    results.round(4).to_csv(REPORTS_DIR / "model_comparison.csv", index=False)
    early_results, _, _, _ = fit_compare(data, False)
    comparison = {"with_G1_G2_best": results.iloc[0].to_dict(), "without_G1_G2_best": early_results.iloc[0].to_dict()}
    with open(REPORTS_DIR / "grade_feature_comparison.json", "w", encoding="utf-8") as handle: json.dump(comparison, handle, indent=2)
    importance = save_plots(results, best_pipe, X_test, y_test)
    metadata = {"dataset_rows": len(data), "raw_features": data.shape[1]-1, "missing_values": int(data.isna().sum().sum()), "duplicate_rows": int(data.duplicated().sum()), "best_model": best_name, "best_metrics": results.iloc[0][["MAE","RMSE","R2"]].to_dict(), "feature_columns": list(X_test.columns), "top_features": importance.head(10).to_dict(orient="records")}
    with open(REPORTS_DIR / "training_metadata.json", "w", encoding="utf-8") as handle: json.dump(metadata, handle, indent=2)
    print(f"Rows: {len(data)} | Features: {data.shape[1]-1} | Missing values: {metadata['missing_values']} | Duplicates: {metadata['duplicate_rows']}")
    print(results.round(4).to_string(index=False)); print(f"Saved best model: {best_name}")
if __name__ == "__main__": main()

