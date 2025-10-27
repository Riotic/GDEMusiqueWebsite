# Backend Dockerfile pour FastAPI
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements (depuis la racine du repo)
COPY ./requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
CMD ["ls"]

COPY ./backend/ ./backend/
COPY seed_data.py .
COPY start-backend.sh /start-backend.sh

# Créer le dossier pour les uploads
RUN mkdir -p /app/backend/media/uploads

# Rendre le script exécutable
RUN chmod +x /start-backend.sh

# Exposer le port
EXPOSE 8000

# Variables d'environnement par défaut
ENV PYTHONUNBUFFERED=1

# Script de démarrage
CMD ["/start-backend.sh"]
