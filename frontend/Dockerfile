# Frontend Dockerfile avec Nginx
FROM nginx:alpine

# Copier les fichiers frontend (HTML/CSS/JS)
COPY static/ /usr/share/nginx/html/static/
COPY index.html /usr/share/nginx/html/

# Copier la configuration Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copier le script de démarrage
COPY start-frontend.sh /start-frontend.sh
RUN chmod +x /start-frontend.sh

# Exposer le port 80
EXPOSE 80

# Utiliser le script de démarrage
CMD ["/start-frontend.sh"]
