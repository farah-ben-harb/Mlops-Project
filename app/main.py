# api python 
from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import joblib
# Application FastAPI
app = FastAPI(
    title="Mini CRM Intelligence",
    description="Projet DevOps/MLOps de preparation NEOFACTO",
    version="1.0.0"
)


# Structure d'un profil professionnel
class Profile(BaseModel):
    id: int
    name: str
    skills: list[str]


# Donnees fictives
profiles = [
    Profile(
        id=1,
        name="Alex Martin",
        skills=["Python", "Docker", "Linux"]
    ),
    Profile(
        id=2,
        name="Samira Dupont",
        skills=["Terraform", "Ansible", "AWS"]
    ),
    Profile(
        id=3,
        name="Thomas Bernard",
        skills=["Python", "MLflow", "Machine Learning"]
    )
]


# Endpoint de verification
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "mini-crm"}


# Endpoint de consultation des profils
@app.get("/profiles", response_model=list[Profile])
def get_profiles():
    return profiles


# Charger le modele deja entraine
MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "model.joblib"
)

trained_model = joblib.load(MODEL_PATH)


# Structure de la requete
class PredictionRequest(BaseModel):
    skills: str


# Endpoint de prediction
@app.post("/predict")
def predict_domain(request: PredictionRequest):
    prediction = trained_model.predict([request.skills])[0]

    return {
        "domain": str(prediction)
    }

