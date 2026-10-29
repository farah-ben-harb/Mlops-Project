# Contribuer

Merci de contribuer à Mini CRM Intelligence. Le dépôt est un laboratoire pédagogique : les changements doivent rester reproductibles, documentés et limités au périmètre demandé.

## Préparer l'environnement

Utiliser Python 3.12, installer les dépendances, puis exécuter les contrôles avant de pousser :

```bash
python -m pip install -r requirements-api.txt -r requirements-dev.txt
python -m pytest -q
python -m ruff check .
python -m bandit -r app ml -ll
```

Pour un changement ML, ajouter également :

```bash
python -m pip install -r requirements-ml.txt
python ml/validate_data.py
python -m ml.train
```

## Branches et commits

- Partir de `main` à jour.
- Utiliser `feature/`, `fix/` ou `docs/` suivis d'un nom court en kebab-case.
- Ne jamais pousser de secret, credential, fichier `.env` ou artefact ML généré.
- Préférer un message de commit explicite, par exemple `fix(api): handle unavailable model`.
- Ne pas réécrire l'historique partagé et ne pas utiliser de force push.

## Pull request

Une PR doit :

1. expliquer le problème et la solution ;
2. indiquer les tests et scans exécutés ;
3. documenter toute limitation connue ;
4. rester focalisée sur un objectif ;
5. être verte dans GitHub Actions avant fusion.

Le merge privilégié est **Squash and merge** afin de garder `main` lisible. Les changements AWS ou les dépenses Cloud nécessitent une validation séparée et ne font pas partie du workflow local par défaut.
