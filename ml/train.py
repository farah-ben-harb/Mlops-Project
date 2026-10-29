"""Reproducible training and evaluation for the synthetic classifier."""

import json
import os
from pathlib import Path

import joblib
import mlflow
from mlflow.models import infer_signature
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

try:
    from ml.validate_data import DATA_PATH, validate_dataset
except ModuleNotFoundError:  # pragma: no cover - supports `python ml/train.py`
    from validate_data import DATA_PATH, validate_dataset

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "model.joblib"
EVALUATION_PATH = BASE_DIR / "models" / "evaluation.json"
CONFUSION_PATH = BASE_DIR / "models" / "confusion_matrix.csv"
RANDOM_STATE = 42


def build_model() -> Pipeline:
    return Pipeline(
        [
            ("tfidf", TfidfVectorizer()),
            (
                "classifier",
                LogisticRegression(C=0.1, max_iter=1000, random_state=RANDOM_STATE),
            ),
        ]
    )


def load_data() -> tuple[list[str], list[str]]:
    rows = validate_dataset(DATA_PATH)
    return [row["skills"] for row in rows], [row["domain"] for row in rows]


def train_and_evaluate() -> dict[str, object]:
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=RANDOM_STATE, stratify=y
    )
    candidate = build_model().fit(X_train, y_train)
    predictions = candidate.predict(X_test)
    labels = sorted(set(y))
    majority = max(set(y_train), key=y_train.count)
    baseline_predictions = [majority] * len(y_test)
    folds = StratifiedKFold(n_splits=3, shuffle=True, random_state=RANDOM_STATE)
    cross_val_f1 = cross_val_score(build_model(), X, y, cv=folds, scoring="f1_macro")
    matrix = confusion_matrix(y_test, predictions, labels=labels)

    metrics: dict[str, object] = {
        "rows": len(X),
        "test_rows": len(X_test),
        "classes": labels,
        "random_state": RANDOM_STATE,
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision_macro": float(precision_score(y_test, predictions, average="macro")),
        "recall_macro": float(recall_score(y_test, predictions, average="macro")),
        "f1_macro": float(f1_score(y_test, predictions, average="macro")),
        "f1_weighted": float(f1_score(y_test, predictions, average="weighted")),
        "baseline_accuracy": float(accuracy_score(y_test, baseline_predictions)),
        "cross_validation_f1_macro_mean": float(cross_val_f1.mean()),
        "cross_validation_f1_macro_std": float(cross_val_f1.std()),
        "confusion_matrix": matrix.tolist(),
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVALUATION_PATH.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    with CONFUSION_PATH.open("w", encoding="utf-8", newline="") as handle:
        handle.write("actual/predicted," + ",".join(labels) + "\n")
        for label, values in zip(labels, matrix, strict=False):
            handle.write(label + "," + ",".join(str(value) for value in values) + "\n")

    joblib.dump(build_model().fit(X, y), MODEL_PATH)
    return metrics


def log_run(metrics: dict[str, object]) -> None:
    tracking_uri = os.environ.get(
        "MLFLOW_TRACKING_URI", f"sqlite:///{BASE_DIR / 'mlflow.db'}"
    )
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(
        os.environ.get("MLFLOW_EXPERIMENT_NAME", "MiniCRM-Classification")
    )
    with mlflow.start_run(run_name="tfidf-logreg"):
        mlflow.log_params(
            {
                "algorithm": "LogisticRegression",
                "vectorizer": "TF-IDF",
                "dataset_path": str(DATA_PATH.relative_to(BASE_DIR)),
                "dataset_rows": metrics["rows"],
                "random_state": RANDOM_STATE,
            }
        )
        mlflow.log_metrics(
            {
                key: value
                for key, value in metrics.items()
                if isinstance(value, (int, float))
            }
        )
        mlflow.log_artifact(str(MODEL_PATH), artifact_path="model")
        mlflow.log_artifact(str(EVALUATION_PATH), artifact_path="evaluation")
        mlflow.log_artifact(str(CONFUSION_PATH), artifact_path="evaluation")
        mlflow.sklearn.log_model(
            sk_model=joblib.load(MODEL_PATH),
            name="classifier",
            signature=infer_signature(["Python Docker"], ["DevOps"]),
        )


def main() -> None:
    metrics = train_and_evaluate()
    log_run(metrics)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
