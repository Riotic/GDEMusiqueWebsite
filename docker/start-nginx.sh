#!/bin/sh

# Script de démarrage pour Railway
# Remplace la variable BACKEND_URL dans nginx.conf

if [ -z "$BACKEND_URL" ]; then
    echo "❌ BACKEND_URL non définie, utilisation localhost par défaut"
    export BACKEND_URL="http://localhost:8000"
fi

echo "✅ Configuration Nginx avec BACKEND_URL=$BACKEND_URL"

# Créer nginx.conf avec substitution
envsubst '${BACKEND_URL}' < /etc/nginx/nginx.template.conf > /etc/nginx/conf.d/default.conf

echo "✅ Démarrage de Nginx..."
nginx -g 'daemon off;'
