# Rapport GitHub — état et proposition de PR

## État observé avant cette branche

- `main` : `13f70c4`, stable mais CI historique en échec Gitleaks.
- `fix/gitleaks-image-tag` : branche issue de la PR #4, conservée après fusion pour préserver l'historique de la correction Gitleaks.
- `feature/devsecops-scanning`, `feature/ghcr-publish`, `feature/ghcr-deploy` : branches historiques, PR #1–#3 fusionnées dans `main`.
- `feature/mlops-pipeline` : branche distante non fusionnée ; elle contient une première automatisation ML mais mélange le téléchargement du modèle et le build Docker dans un ordre incorrect. Elle reste à examiner séparément.
- Protection de `main` : non activée au moment de l'audit ; aucune règle n'a été changée.
- Description mise à jour : « Educational FastAPI MLOps lab for synthetic CRM profile classification with MLflow, Docker Compose, DevSecOps CI, GHCR, Terraform and Ansible. »
- Topics configurés : `python`, `fastapi`, `machine-learning`, `mlops`, `mlflow`, `docker`, `docker-compose`, `devops`, `devsecops`, `github-actions`, `ghcr`, `terraform`, `ansible`, `crm`, `scikit-learn`.

## Travail réalisé ici

Branche locale et distante : `fix/local-stabilization`. Les branches de travail utilisent les préfixes `feature/`, `fix/` et `docs/`.

Le périmètre est cohérent : stabilisation FastAPI/tests, qualité de données et entraînement ML, portabilité Compose/MLflow, Ruff/CI et documentation. Aucun secret AWS, déploiement Cloud, force push, suppression de branche ou fusion dans `main` n'a été effectué.

PR fusionnée : [#5 — fix: stabilize local API and ML workflow](https://github.com/farah-ben-harb/crm-intelligence-mlops/pull/5). Commit initial : `c6b0545`. Son premier run CI (`40851592879`) est vert pour Python Tests, ML Training and Validation, Bandit, Gitleaks, Trivy et Docker Build and Security Scan ; la publication GHCR est correctement ignorée sur une Pull Request.

## Découpage recommandé des PR

1. PR #4 : correction de l'exception Gitleaks ciblée, fusionnée dans `main` avec la CI verte.
2. PR #5 : stabilisation locale FastAPI/ML, fusionnée dans `main` après synchronisation avec la PR #4.
3. PR #6 : documentation et gouvernance GitHub, fusionnée dans `main` avec la CI verte.

## Protection recommandée pour `main`

Activer après validation des noms de jobs : fusion par Pull Request, checks `Python Tests`, `ML Training and Validation`, `Python SAST - Bandit`, `Secret Scanning - Gitleaks`, `Dependencies and IaC - Trivy` et `Docker Build and Security Scan`, branche à jour avant fusion, interdiction de force push et de suppression. Pour un dépôt personnel, une seule approbation de la mainteneuse peut être suffisante ; ne pas imposer une règle impossible à satisfaire seule.

## Suivi après ouverture

La publication GHCR reste conditionnée à un push sur `main`; aucune publication AWS n'est introduite.
