
# 1. Image de base
FROM python:3.12-slim

# 2. Configuration Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Dossier de travail
WORKDIR /app

# 4. Installer les dependances
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

# 5. Copier l'application
COPY app/ ./app/

# 6. Copier le modele entraine
COPY models/model.joblib ./models/model.joblib

# 7. Port utilise par FastAPI
EXPOSE 8000

# 8. Demarrer l'API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

