# Rapport technique — stabilisation locale

## Réalisé

- FastAPI conserve `/health`, `/profiles` et `/predict`, avec ajout de `/ready`.
- Le modèle est chargé à la première utilisation et mis en cache ; l'absence ou l'invalidité de l'artefact produit `503` sur readiness/prédiction sans empêcher le liveness.
- Les entrées de `/predict` sont bornées à 1–1000 caractères et les réponses sont typées.
- Les tests couvrent santé, profils, inférence, données invalides, modèle absent et chargement d'un artefact de test.
- Le dataset est validé par colonnes, taille, valeurs vides, IDs et distribution des domaines.
- L'entraînement calcule accuracy, precision, recall, F1, baseline, validation croisée et matrice de confusion ; il écrit des artefacts et journalise le run MLflow.
- Compose et MLflow n'utilisent plus le chemin absolu de l'ancienne VM ; les artefacts sont montés depuis `./mlartifacts`, avec healthchecks et réseau créé automatiquement.
- Ruff est intégré aux dépendances de développement et à la CI. Le build Docker utilise le modèle produit par le job ML après téléchargement de l'artefact.

## Validation exécutée

| Contrôle | Résultat |
|---|---|
| `python -m pytest -q` | 12 passed |
| `python -m ruff check .` | All checks passed |
| `python -m bandit -r app ml -ll` | No issues identified |
| `python ml/validate_data.py` | 30 rows; 10 par domaine |
| `python -m ml.train` | Exécuté avec succès ; métriques écrites et run MLflow créé |
| Parsing YAML de `compose.yaml` | Services `api` et `mlflow` détectés |
| Docker/Compose local | Non exécuté : Docker Desktop n'est pas installé sur la machine d'audit |
| Trivy/Gitleaks locaux | Non exécutés : outils absents ; configurés dans GitHub Actions |

L'entraînement local a observé 1,00 d'accuracy/F1 sur les 9 lignes de test et environ 0,525 de F1 macro moyen en validation croisée à trois plis. Ces valeurs sont descriptives du dataset synthétique et ne constituent pas une preuve de généralisation. Le modèle versionné n'a pas été remplacé par l'artefact produit sous scikit-learn 1.7.2 ; la CI Python 3.12 et scikit-learn 1.9.1 reste la référence pour générer l'artefact officiel.

## Points restants

- Exécuter Docker/Compose dans un environnement équipé et vérifier réellement les healthchecks, permissions de `mlartifacts`, persistance et redémarrage.
- Obtenir le run CI complet de la branche de stabilisation, notamment le job ML et le scan Docker.
- Revoir puis fusionner séparément la PR Gitleaks déjà ouverte (#4) avant de fusionner cette branche.
- Évaluer un jeu de validation externe avant toute communication de performance.
- Ne pas activer AWS : aucun code ou workflow AWS n'a été ajouté.
