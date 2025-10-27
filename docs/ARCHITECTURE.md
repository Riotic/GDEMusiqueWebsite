# 🏗️ Architecture - GDE Music Platform

## Vue d'ensemble

GDE Music Platform est une application web moderne basée sur une architecture **microservices** conteneurisée avec Docker.

## Architecture Microservices

```
┌─────────────────────────────────────────────────────────────┐
│                    Internet / Utilisateurs                   │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
                   ┌──────────────────┐
                   │   Nginx (Port 80)│
                   │   Reverse Proxy   │
                   └────────┬─────────┘
                            │
                ┌───────────┴────────────┐
                │                        │
                ▼                        ▼
    ┌──────────────────┐    ┌──────────────────┐
    │   Frontend       │    │    Backend       │
    │   (Nginx)        │    │   (FastAPI)      │
    │   Port 3000      │    │   Port 8000      │
    │                  │    │                  │
    │ - HTML/CSS/JS    │    │ - API REST       │
    │ - Animations     │    │ - Business Logic │
    │ - Player Audio   │    │ - Validation     │
    └──────────────────┘    └────────┬─────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │   PostgreSQL     │
                            │   Port 5432      │
                            │                  │
                            │ - User Data      │
                            │ - Songs Info     │
                            │ - Playlists      │
                            └──────────────────┘
```

## Composants

### 1. Frontend (Microservice)

**Technologie** : Nginx + HTML/CSS/JavaScript

**Responsabilités** :
- Servir les fichiers statiques (HTML, CSS, JS, images)
- Routage côté client
- Interface utilisateur
- Animations et interactions
- Lecteur audio

**Fichiers clés** :
- `frontend/index.html` - Page principale
- `frontend/static/js/app.js` - Logique application
- `frontend/static/js/player.js` - Lecteur audio
- `frontend/static/js/animations.js` - Animations GSAP
- `frontend/static/css/style.css` - Styles

**Container** :
- Image : `nginx:alpine`
- Port : 3000 (externe) → 80 (interne)
- Configuration : `nginx.conf`

### 2. Backend (Microservice)

**Technologie** : Python 3.11 + FastAPI

**Responsabilités** :
- API RESTful
- Logique métier
- Validation des données
- Authentification/Autorisation
- Gestion des fichiers
- Communication avec la base de données

**Fichiers clés** :
- `backend/main.py` - Point d'entrée FastAPI
- `backend/models.py` - Modèles de données
- `backend/schemas.py` - Validation Pydantic
- `backend/database.py` - Configuration DB
- `backend/routers/` - Endpoints API

**Container** :
- Image : `python:3.11-slim`
- Port : 8000
- Hot reload en développement

**Endpoints principaux** :
```
GET  /health              - Health check
GET  /api/music/songs     - Liste des chansons
POST /api/music/songs     - Créer une chanson
GET  /api/playlists       - Liste des playlists
POST /api/users/register  - Inscription
```

### 3. Base de données (Microservice)

**Technologie** : PostgreSQL 15

**Responsabilités** :
- Stockage persistant
- Gestion des transactions
- Intégrité des données
- Relations entre entités

**Container** :
- Image : `postgres:15-alpine`
- Port : 5432
- Volume : `postgres_data` (persistant)

**Modèles de données** :
- `users` - Utilisateurs
- `songs` - Chansons
- `playlists` - Playlists
- `playlist_songs` - Association playlists-chansons

## Communication entre services

### Frontend ↔ Backend

```javascript
// Frontend (JavaScript)
fetch('/api/music/songs')
  .then(response => response.json())
  .then(songs => displaySongs(songs));
```

Le frontend communique avec le backend via :
- **HTTP/REST** - Requêtes AJAX (Fetch API)
- **JSON** - Format d'échange de données
- **Proxy Nginx** - `/api/*` redirige vers `backend:8000`

### Backend ↔ Database

```python
# Backend (Python/SQLAlchemy)
songs = db.query(Song).all()
```

Le backend communique avec PostgreSQL via :
- **SQLAlchemy ORM** - Mapping objet-relationnel
- **psycopg2** - Driver PostgreSQL
- **Connexion TCP** - Port 5432

## Réseau Docker

Tous les services sont dans un réseau Docker privé (`gde_network`) :

```yaml
networks:
  gde_network:
    driver: bridge
```

**Avantages** :
- Isolation des services
- Communication par nom de service
- Sécurité accrue
- Facile à scaler

## Volumes Docker

### Données persistantes

```yaml
volumes:
  postgres_data:     # Base de données
  media_files:       # Fichiers uploadés
```

**Caractéristiques** :
- Survivent aux redémarrages
- Peuvent être sauvegardés
- Indépendants des containers

## Flux de données

### 1. Affichage des chansons

```
User → Frontend → Nginx Proxy → Backend → PostgreSQL
                                    ↓
                                  JSON
                                    ↓
User ← Frontend ← ─ ─ ─ ─ ─ ─ ─ Backend
```

### 2. Lecture d'une chanson

```
User clicks play
    ↓
Frontend updates UI
    ↓
Audio player loads file
    ↓
POST /api/music/{id}/play
    ↓
Backend increments play count
    ↓
PostgreSQL updates counter
```

## Scalabilité

### Scalabilité horizontale

```bash
# Augmenter les instances du backend
docker-compose up -d --scale backend=3
```

### Load Balancing

Nginx peut être configuré pour distribuer la charge :

```nginx
upstream backend {
    server backend_1:8000;
    server backend_2:8000;
    server backend_3:8000;
}
```

## Sécurité

### Isolation

- Chaque service dans son container
- Réseau privé Docker
- Pas d'accès direct à PostgreSQL depuis l'extérieur

### HTTPS (Production)

```
Internet → HTTPS (443) → Nginx SSL Termination → HTTP Backend
```

### Variables d'environnement

Données sensibles stockées dans `.env` :
- Mots de passe
- Clés secrètes
- Configuration DB

## Monitoring

### Health Checks

```yaml
healthcheck:
  test: ["CMD", "pg_isready", "-U", "gde_user"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### Logs

```bash
# Logs centralisés
docker-compose logs -f

# Par service
docker-compose logs -f backend
```

## Déploiement

### Développement

```bash
docker-compose up -d
```

### Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

**Différences** :
- Pas de hot reload
- Workers multiples
- Optimisations performances
- HTTPS activé
- Logs en production

## Extensions futures

### Redis (Cache)

```yaml
redis:
  image: redis:alpine
  ports:
    - "6379:6379"
```

**Usage** :
- Cache des requêtes
- Sessions utilisateur
- File d'attente de tâches

### Elasticsearch (Recherche)

```yaml
elasticsearch:
  image: elasticsearch:8.11.0
  environment:
    - discovery.type=single-node
```

**Usage** :
- Recherche full-text avancée
- Indexation des chansons
- Suggestions de recherche

### S3/MinIO (Stockage)

```yaml
minio:
  image: minio/minio
  command: server /data
```

**Usage** :
- Stockage des fichiers audio
- Stockage des images
- CDN pour les médias

## Bonnes pratiques

✅ **Séparation des préoccupations** - Chaque service a une responsabilité unique
✅ **Stateless** - Le backend ne stocke pas d'état de session
✅ **12-Factor App** - Configuration via environnement
✅ **Containerisation** - Reproductibilité garantie
✅ **Versioning** - Git + Tags Docker
✅ **CI/CD** - GitHub Actions pour le déploiement

## Diagramme de séquence complet

```
┌────────┐    ┌─────────┐    ┌─────────┐    ┌──────────┐
│ User   │    │Frontend │    │ Backend │    │PostgreSQL│
└───┬────┘    └────┬────┘    └────┬────┘    └────┬─────┘
    │              │              │              │
    │ GET /        │              │              │
    ├─────────────>│              │              │
    │              │              │              │
    │   HTML/CSS/JS│              │              │
    │<─────────────┤              │              │
    │              │              │              │
    │Click "Play"  │              │              │
    ├─────────────>│              │              │
    │              │              │              │
    │              │GET /api/songs│              │
    │              ├─────────────>│              │
    │              │              │              │
    │              │              │SELECT * FROM │
    │              │              ├─────────────>│
    │              │              │              │
    │              │              │  Songs data  │
    │              │              │<─────────────┤
    │              │              │              │
    │              │  JSON songs  │              │
    │              │<─────────────┤              │
    │              │              │              │
    │ Display songs│              │              │
    │<─────────────┤              │              │
    │              │              │              │
```

---

Pour plus de détails, consultez :
- [DOCKER.md](DOCKER.md) - Guide Docker
- [DEPLOYMENT.md](DEPLOYMENT.md) - Guide de déploiement
- [COMMANDS.md](COMMANDS.md) - Commandes rapides
