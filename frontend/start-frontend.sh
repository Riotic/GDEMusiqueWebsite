#!/bin/sh
# Script de démarrage pour le frontend Railway
# Génère config.js avec les bonnes variables d'environnement

echo "🔧 Génération de config.js..."

# Créer config.js avec l'URL du backend
cat > /usr/share/nginx/html/static/js/config.js << EOF
// Configuration générée automatiquement au déploiement
const isDevelopment = window.location.hostname === 'localhost';
const API_URL = isDevelopment 
    ? 'http://localhost:8000/api'
    : '${BACKEND_URL:-https://gde-backend-production.up.railway.app/api}';

window.CONFIG = { API_URL, isDevelopment };
console.log('✅ Config chargée:', window.CONFIG);
EOF

echo "✅ Config généré avec BACKEND_URL=${BACKEND_URL}"

# Configurer le port Nginx depuis la variable Railway
PORT=${PORT:-80}
echo "📡 Configuration du port: $PORT"
sed -i "s/listen 80;/listen $PORT;/g" /etc/nginx/conf.d/default.conf

echo "🚀 Démarrage de Nginx..."

# Démarrer Nginx
nginx -g 'daemon off;'
