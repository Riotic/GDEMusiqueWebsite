// Configuration générée automatiquement
// Ce fichier sera remplacé au déploiement Railway par un script

// En développement local
const isDevelopment = window.location.hostname === 'localhost';

// URL du backend selon l'environnement
const API_URL = isDevelopment 
    ? 'http://localhost:8000/api'
    : (window.ENV?.BACKEND_URL || 'https://gde-backend-production.up.railway.app/api');

// Export pour utilisation dans les autres fichiers
window.CONFIG = {
    API_URL,
    isDevelopment
};
