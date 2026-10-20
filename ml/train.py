
import csv
from pathlib import Path

import joblib
import mlflow

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
)

# 1. Charger le dataset
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "profiles.csv"

with DATA_PATH.open("r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

X = [row["skills"] for row in rows]
y = [row["domain"] for row in rows]

print(f"Nombre total de profils : {len(X)}")

# 2. Separer Train / Test
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

print(f"Train : {len(X_train)} profils")
print(f"Test : {len(X_test)} profils")

# 3. Creer le Pipeline ML
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression(
        C=0.1,
        max_iter=1000,
        random_state=42
    ))
])

# 4. Entrainer le modele
model.fit(X_train, y_train)

# 5. Evaluer le modele
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
f1 = f1_score(
    y_test,
    predictions,
    average="weighted",
    zero_division=0
)

print(f"\nAccuracy : {accuracy:.2%}")
print(f"F1-score : {f1:.2%}")

print("\nClassification Report :")
print(classification_report(
    y_test,
    predictions,
    zero_division=0
))

# 6. Sauvegarder le modele
MODEL_PATH = BASE_DIR / "models" / "model.joblib"
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(model, MODEL_PATH)
print(f"\nModele sauvegarde : {MODEL_PATH}")

# 7. Tester une prediction
new_profile = ["Python Docker Kubernetes Terraform"]
result = model.predict(new_profile)

print(f"Profil : {new_profile[0]}")
print(f"Domaine predit : {result[0]}")

# 8. Configurer MLflow
mlflow.set_tracking_uri(
    f"sqlite:///{BASE_DIR / 'mlflow.db'}"
)

mlflow.set_experiment("MiniCRM-Classification")

# 9. Enregistrer un Run MLflow
with mlflow.start_run(run_name="tfidf-logreg-v2") as run:

    # Parameters
    mlflow.log_param("algorithm", "LogisticRegression")
    mlflow.log_param("vectorizer", "TF-IDF")
    mlflow.log_param("C", 0.1)
    mlflow.log_param("max_iter", 1000)
    mlflow.log_param("test_size", 0.30)

    # Metrics
    mlflow.log_metric("accuracy", float(accuracy))
    mlflow.log_metric("f1_weighted", float(f1))

    # Artifact : modele sauvegarde
    mlflow.log_artifact(
        str(MODEL_PATH),
        artifact_path="model"
    )

    print("\nMLflow Run enregistre !")
    print(f"Run ID : {run.info.run_id}")

