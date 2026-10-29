
import csv
from collections import Counter
from pathlib import Path

# Donnees entierement fictives
samples = [
    # DevOps
    ("Linux Docker Kubernetes Terraform Ansible", "DevOps"),
    ("GitLab CI Docker Linux Prometheus", "DevOps"),
    ("AWS Terraform Kubernetes Helm ArgoCD", "DevOps"),
    ("Linux Bash Ansible Nginx Docker", "DevOps"),
    ("Azure Terraform GitHub Actions Kubernetes", "DevOps"),
    ("Docker Compose Grafana Prometheus Linux", "DevOps"),
    ("Helm Kubernetes ArgoCD GitOps Security", "DevOps"),
    ("Linux CI CD Docker Trivy Terraform", "DevOps"),
    ("Ansible Terraform Networks Infrastructure", "DevOps"),
    ("GitHub Actions Docker Monitoring SRE", "DevOps"),

    # Backend
    ("Python FastAPI PostgreSQL Pytest", "Backend"),
    ("Java Spring Boot MySQL REST API", "Backend"),
    ("NodeJS Express MongoDB JavaScript", "Backend"),
    ("Python Django Redis PostgreSQL", "Backend"),
    ("TypeScript NestJS PostgreSQL API", "Backend"),
    ("Python Flask SQLAlchemy Pytest", "Backend"),
    ("Java Spring Security Kafka Microservices", "Backend"),
    ("FastAPI Docker PostgreSQL Alembic", "Backend"),
    ("NodeJS REST API Authentication JWT", "Backend"),
    ("Go Gin GRPC API PostgreSQL", "Backend"),

    # MLOps
    ("Python MLflow Scikit-learn Pandas", "MLOps"),
    ("TensorFlow Python MLflow Model Training", "MLOps"),
    ("PyTorch Python Experiment Tracking", "MLOps"),
    ("MLflow Docker Inference Machine Learning", "MLOps"),
    ("Pandas Sklearn Data Preprocessing Classification", "MLOps"),
    ("Python Machine Learning Feature Engineering", "MLOps"),
    ("Keras Neural Network Training Python", "MLOps"),
    ("MLflow Model Registry Model Evaluation", "MLOps"),
    ("Sklearn Regression Classification Pipeline", "MLOps"),
    ("Python Transformers Embeddings MLflow", "MLOps"),
]

output = Path("data/profiles.csv")
output.parent.mkdir(parents=True, exist_ok=True)

with output.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "skills", "domain"])

    for profile_id, (skills, domain) in enumerate(samples, start=1):
        writer.writerow([profile_id, skills, domain])

print(f"Dataset cree : {output}")
print(f"Nombre de profils : {len(samples)}")
print(f"Repartition : {dict(Counter(label for _, label in samples))}")

