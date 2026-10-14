"""Reproduce holdout evaluation for the saved model."""
from sklearn.model_selection import train_test_split
from train_model import score
from data_preprocessing import RANDOM_STATE, load_dataset, split_features_target
from predict import load_model

def main():
    data = load_dataset(); X, y = split_features_target(data, True)
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)
    metrics = score(y_test, load_model().predict(X_test))
    print("Saved model evaluation")
    for key, value in metrics.items(): print(f"{key}: {value:.4f}")
if __name__ == "__main__": main()
