from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_profiles():
    response = client.get("/profiles")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_predict():
    response = client.post(
        "/predict",
        json={"skills": "Python Docker Kubernetes Terraform"}
    )

    assert response.status_code == 200
    assert response.json()["domain"] == "DevOps"
