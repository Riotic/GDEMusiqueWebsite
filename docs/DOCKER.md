# 🐳 Docker - Guide de démarrage rapide

## Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé
- Aucune autre dépendance nécessaire !

## 🚀 Lancement ultra-rapide

### Option 1 : Tout en une commande

```powershell
docker-compose up --build
```

### Option 2 : En mode détaché (arrière-plan)

```powershell
docker-compose up -d --build
```

## 🌐 Accès aux services

Une fois les containers démarrés :

- **Frontend (Site web)** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs
- **PostgreSQL** : localhost:5432

## 📊 Commandes utiles

### Voir les logs

```powershell
# Tous les services
docker-compose logs -f

# Un service spécifique
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Arrêter les services

```powershell
# Arrêter
docker-compose stop

# Arrêter et supprimer les containers
docker-compose down

# Arrêter et supprimer containers + volumes (⚠️ efface la DB)
docker-compose down -v
```

### Redémarrer un service

```powershell
docker-compose restart backend
docker-compose restart frontend
```

### Reconstruire après modification du code

```powershell
# Reconstruire un service
docker-compose up -d --build backend

# Reconstruire tous les services
docker-compose up -d --build
```

### Accéder au shell d'un container

```powershell
# Backend
docker exec -it gde_backend sh

# PostgreSQL
docker exec -it gde_postgres psql -U gde_user -d gde_music

# Frontend
docker exec -it gde_frontend sh
```

### Voir les containers en cours

```powershell
docker-compose ps
```

### Nettoyer complètement

```powershell
# Supprimer containers, réseaux, volumes
docker-compose down -v

# Supprimer aussi les images
docker-compose down -v --rmi all

# Nettoyer tout Docker (⚠️ attention)
docker system prune -a --volumes
```

## 🔧 Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine :

```env
POSTGRES_PASSWORD=votre_mot_de_passe_securise
SECRET_KEY=votre_cle_secrete_generee
DEBUG=False
```

### Régénérer la base de données

```powershell
# Arrêter les services
docker-compose down -v

# Redémarrer (les données seront réinitialisées)
docker-compose up -d --build
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                  Docker Network                  │
│                                                  │
│  ┌──────────────┐     ┌──────────────┐         │
│  │   Frontend   │────▶│   Backend    │         │
│  │   (Nginx)    │     │  (FastAPI)   │         │
│  │   Port 3000  │     │   Port 8000  │         │
│  └──────────────┘     └──────┬───────┘         │
│                              │                   │
│                              ▼                   │
│                       ┌──────────────┐          │
│                       │  PostgreSQL  │          │
│                       │   Port 5432  │          │
│                       └──────────────┘          │
│                                                  │
└─────────────────────────────────────────────────┘
```

## ✨ Fonctionnalités

✅ **Hot reload** - Le code se recharge automatiquement
✅ **Données persistantes** - La DB survit aux redémarrages
✅ **Isolation complète** - Pas besoin d'installer Python/Node
✅ **Prêt pour la prod** - Configuration facilement adaptable
✅ **Multi-plateforme** - Fonctionne sur Windows/Mac/Linux

## 🐛 Dépannage

### Le port 3000 est déjà utilisé

Modifiez dans `docker-compose.yml` :
```yaml
ports:
  - "8080:80"  # Utilisez 8080 au lieu de 3000
```

### Erreur de connexion à PostgreSQL

```powershell
# Vérifier que PostgreSQL est démarré
docker-compose ps

# Voir les logs
docker-compose logs postgres

# Redémarrer le service
docker-compose restart postgres
```

### Le frontend ne se connecte pas au backend

Vérifiez que l'URL dans `frontend/static/js/app.js` pointe vers :
```javascript
const API_URL = '/api';  // Utilise le proxy Nginx
```

## 📦 Volumes

- `postgres_data` : Données PostgreSQL
- `media_files` : Fichiers uploadés (musique, images)

Ces volumes persistent même après `docker-compose down`.

## 🎯 Prêt pour la production

Pour déployer en production :

1. Changez les mots de passe dans `.env`
2. Générez une vraie `SECRET_KEY`
3. Mettez `DEBUG=False`
4. Utilisez un reverse proxy (Traefik, Nginx)
5. Activez HTTPS

Bon développement ! 🎵
