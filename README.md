# 🎵 GDE - Grande École de Musique

Site vitrine moderne pour l'école de musique GDE, avec animations fluides et design responsive.

## 🚀 Technologies utilisées

### Backend

- **FastAPI** - Framework web moderne et performant
- **Python 3.11+**

### Frontend

- **HTML5/CSS3** - Structure et design responsive
- **JavaScript ES6+** - Logique côté client
- **GSAP 3.12** - Animations fluides et scroll-triggered
- **Design mobile-first** - Optimisé pour tous les appareils

### Infrastructure

- **Docker** - Conteneurisation
- **Docker Compose** - Orchestration des microservices
- **Nginx** - Serveur web et reverse proxy
- **PostgreSQL** - Base de données relationnelle

## 🐳 Démarrage rapide avec Docker (RECOMMANDÉ)

### Prérequis
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé
- C'est tout ! Aucune autre installation nécessaire

### Lancer l'application

**Windows PowerShell :**
```powershell
.\docker.ps1 init
```

**Linux/Mac ou avec Make :**
```bash
make init
```

**Ou directement avec Docker Compose :**
```bash
docker-compose -f docker/docker-compose.yml up -d --build
```

### Accès aux services

- **Site Web** : <http://localhost:3000>
- **Backend API** : <http://localhost:8000>
- **Health Check** : <http://localhost:8000/health>

### Commandes utiles

```powershell
# Démarrer
.\docker.ps1 start

# Arrêter
.\docker.ps1 stop

# Voir les logs
.\docker.ps1 logs

# Redémarrer
.\docker.ps1 restart

# Nettoyer
.\docker.ps1 clean
```

Voir [docs/DOCKER.md](docs/DOCKER.md) pour plus de détails.

## 📁 Structure du projet

```
GDEMusiqueWebsite/
├── backend/                 # Backend API
│   ├── main.py              # Point d'entrée FastAPI
│   ├── database.py          # Configuration DB
│   ├── health.py            # Health check
│   └── media/               # Uploads (si nécessaire)
│
├── frontend/                # Site vitrine
│   ├── index.html           # Page principale
│   └── static/
│       ├── css/
│       │   └── style.css    # Styles responsive
│       ├── js/
│       │   ├── app.js       # Logique principale
│       │   └── animations.js # Animations GSAP
│       └── images/          # Images et logos
│
├── docker/                  # Configuration Docker
│   ├── Dockerfile.backend   # Image Docker Backend
│   ├── Dockerfile.frontend  # Image Docker Frontend
│   ├── docker-compose.yml   # Orchestration
│   ├── docker-compose.prod.yml
│   ├── nginx.conf          # Config Nginx
│   └── wait-for-postgres.sh
│
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md      # Architecture du projet
│   ├── DOCKER.md            # Guide Docker
│   ├── DOCKER-SETUP.md
│   ├── DEPLOYMENT.md        # Guide déploiement
│   ├── QUICKSTART.md        # Démarrage rapide
│   ├── COMMANDS.md          # Commandes utiles
│   └── CHANGELOG.md         # Historique des versions
│
├── docker.ps1              # Script PowerShell
├── Makefile                # Commandes Make
├── requirements.txt         # Dépendances Python
└── run.py                   # Lancement dev local
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              Docker Network (Bridge)             │
│                                                  │
│  ┌──────────────┐                               │
│  │   Frontend   │  Nginx (Port 3000)            │
│  │              │  - Site vitrine responsive    │
│  └──────┬───────┘  - Animations GSAP            │
│         │                                        │
│         ▼                                        │
│  ┌──────────────┐                               │
│  │   Backend    │  FastAPI (Port 8000)          │
│  │              │  - API REST (si besoin)       │
│  └──────┬───────┘  - Health check               │
│         │                                        │
│         ▼                                        │
│  ┌──────────────┐                               │
│  │  PostgreSQL  │  Database (Port 15432)        │
│  │              │  - Données persistantes       │
│  └──────────────┘  - Volume Docker              │
│                                                  │
└─────────────────────────────────────────────────┘
```

## 🛠️ Installation locale (sans Docker)

Si vous préférez installer les dépendances localement :

### 1. Cloner le dépôt

```bash
git clone https://github.com/Riotic/GDEMusiqueWebsite.git
cd GDEMusiqueWebsite
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
```

### 3. Activer l'environnement virtuel

**Windows:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 🎮 Lancement de l'application

### Démarrer le serveur

```bash
python run.py
```

L'application sera accessible à :

- **Site Web**: <http://localhost:8000>
- **Health Check**: <http://localhost:8000/health>

---

## 🐳 Avantages de Docker

✅ **Zéro installation** - Juste Docker Desktop  
✅ **Isolation complète** - Pas de conflit de dépendances  
✅ **Reproductible** - Fonctionne partout de la même façon  
✅ **Scalable** - Facile d'ajouter des services  
✅ **Production-ready** - Configuration proche de la prod

## ✨ Fonctionnalités

- ✅ Interface moderne et responsive
- ✅ Design mobile-first (breakpoints 968px, 640px)
- ✅ Animations fluides avec GSAP ScrollTrigger
- ✅ Sections : Hero, À propos, Cours, Événements, Communauté, Contact
- ✅ Palette de couleurs GDE (rouge, or, tons boisés)
- ✅ Formulaire de contact
- ✅ Newsletter
- ✅ API Backend (extensible)

## 🎨 Animations

Le site utilise **GSAP 3.12** pour des animations modernes :

- Animations au scroll (ScrollTrigger)
- Effets parallax
- Transitions fluides entre sections
- Compteurs animés pour les statistiques
- Wave gradient animée

## 📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails

## 👤 Auteur

**Riotic**

- GitHub: [@Riotic](https://github.com/Riotic)