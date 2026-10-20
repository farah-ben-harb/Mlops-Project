# Mini CRM Intelligence — DevOps & MLOps

End-to-end DevOps/MLOps project combining machine learning, infrastructure automation, DevSecOps and container deployment.

## Architecture

GitHub → GitHub Actions → GHCR → Ansible → Docker Compose → FastAPI

Terraform provisions the Docker network.
MLflow tracks ML experiments and metrics.

## Tech Stack

- Backend: Python, FastAPI
- ML: scikit-learn, TF-IDF, Logistic Regression
- MLOps: MLflow
- Containers: Docker, Docker Compose
- Infrastructure: Terraform, Ansible
- CI/CD: GitHub Actions, GHCR
- Security: Bandit, Gitleaks, Trivy
- Testing: pytest

## Features

- GET /health — API health check
- GET /profiles — Sample profiles
- POST /predict — Predict Backend, DevOps or MLOps
- MLflow experiment tracking
- Automated CI and DevSecOps checks
- Versioned Docker images published to GHCR
- Ansible deployment, verification and manual rollback

## CI/CD Pipeline

1. Pull Request triggers automated tests and security scans.
2. Docker image is built and security-scanned.
3. After merging into main, the image is published to GHCR.
4. Ansible deploys a selected image version using Docker Compose.
5. Post-deployment health checks validate the services.

## Deployment

Requires Docker, Docker Compose, Ansible and Terraform
in a configured Ubuntu environment.

From the ansible directory:

    ansible-playbook playbooks/site.yml

Override the Docker image version:

    ansible-playbook playbooks/site.yml -e "api_image=IMAGE_TAG"

The deployment is idempotent and supports manual rollback.

## Local URLs

- FastAPI: http://localhost:8002/docs
- MLflow: http://localhost:5001

## Notes

The ML dataset is small and synthetic.
Model accuracy is not representative of production performance.
Deployment is currently manual on a local Ubuntu VM.
