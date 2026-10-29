"""HTTP interface for the synthetic profile classifier."""

import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from app.model import ModelUnavailable, get_model

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="Mini CRM Intelligence",
    description="Synthetic profile classification demo",
    version="1.1.0",
)


class Profile(BaseModel):
    id: int
    name: str
    skills: list[str]


class PredictionRequest(BaseModel):
    skills: str = Field(min_length=1, max_length=1000)

    @field_validator("skills")
    @classmethod
    def strip_and_validate_skills(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("skills must contain non-whitespace text")
        return value


class PredictionResponse(BaseModel):
    domain: str


PROFILES = [
    Profile(id=1, name="Alex Martin", skills=["Python", "Docker", "Linux"]),
    Profile(id=2, name="Samira Dupont", skills=["Terraform", "Ansible", "AWS"]),
    Profile(
        id=3,
        name="Thomas Bernard",
        skills=["Python", "MLflow", "Machine Learning"],
    ),
]


@app.get("/health")
def health_check() -> dict[str, str]:
    """Liveness does not depend on a model file."""
    return {"status": "healthy", "service": "mini-crm"}


@app.get("/ready")
def readiness_check() -> dict[str, str]:
    """Readiness verifies that the classifier can be loaded."""
    try:
        get_model()
    except ModelUnavailable as exc:
        raise HTTPException(status_code=503, detail="Model unavailable") from exc
    return {"status": "ready", "model": "loaded"}


@app.get("/profiles", response_model=list[Profile])
def get_profiles() -> list[Profile]:
    return PROFILES


@app.post("/predict", response_model=PredictionResponse)
def predict_domain(request: PredictionRequest) -> PredictionResponse:
    try:
        prediction = get_model().predict([request.skills])[0]
    except ModelUnavailable as exc:
        raise HTTPException(status_code=503, detail="Model unavailable") from exc
    except Exception as exc:
        logger.exception("Model inference failed")
        raise HTTPException(status_code=500, detail="Prediction failed") from exc
    return PredictionResponse(domain=str(prediction))
