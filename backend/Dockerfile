# Backend Dockerfile pour FastAPI
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements (depuis la racine du repo)
COPY ./requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# DEBUG: Lister les fichiers à la racine du context
RUN echo "📂 Contenu de la racine du context:" && ls -la /

# Copier le code de l'application
COPY ./backend/ ./backend/
RUN echo "📂 Contenu de /app après COPY backend:" && ls -la /app
COPY backend/seed_data.py .
RUN echo "📂 Contenu de /app après COPY seed:" && ls -la /app
COPY backend/start-backend.sh /start-backend.sh

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
