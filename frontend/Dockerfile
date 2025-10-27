# Frontend Dockerfile avec Nginx
FROM nginx:alpine

# DEBUG: Afficher le contenu du context
RUN echo "=== Contenu du context Docker ===" && ls -la

# Copier les fichiers frontend
COPY frontend/ /usr/share/nginx/html/

# Copier la configuration Nginx personnalisée  
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

# Copier le script de démarrage
COPY ./frontend/start-frontend.sh /start-frontend.sh
RUN chmod +x /start-frontend.sh

# Exposer le port 80
EXPOSE 80

# Utiliser le script de démarrage
CMD ["/start-frontend.sh"]
