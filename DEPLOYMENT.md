# 🚀 Guide de Déploiement - GDE Musique

## Option 1 : Railway.app (RECOMMANDÉ - Le plus simple)

### Étapes :

1. **Créer un compte** sur [Railway.app](https://railway.app)

2. **Nouveau projet** :
   - Cliquer "New Project"
   - Sélectionner "Deploy from GitHub repo"
   - Autoriser Railway à accéder à ton repo GitHub
   - Sélectionner le repo `GDEMusiqueWebsite`

3. **Configuration automatique** :
   - Railway détecte automatiquement `docker-compose.yml`
   - Il va créer 3 services : frontend, backend, postgres

4. **Variables d'environnement** :
   - Railway détecte automatiquement les variables
   - Tout fonctionne out-of-the-box !

5. **URL publique** :
   - Dans les settings du service `frontend`, activer "Generate Domain"
   - Tu obtiens une URL type : `gde-musique.up.railway.app`

**Temps estimé : 5 minutes** ⚡

---

## Option 2 : Render.com

### Étapes :

1. **Créer un compte** sur [Render.com](https://render.com)

2. **Nouveau Blueprint** :
   - Cliquer "New +" → "Blueprint"
   - Connecter ton repo GitHub
   - Render détecte `docker-compose.yml`

3. **Configuration** :
   - PostgreSQL : Plan gratuit (expire après 90 jours)
   - Backend : Web Service (Docker)
   - Frontend : Static Site ou Web Service

4. **Déploiement** :
   - Cliquer "Apply"
   - Attendre 5-10 minutes

**Gratuit mais avec limitations** (services s'endorment après inactivité)

---

## Option 3 : Vercel + Railway Postgres

### Pour le Frontend (Vercel) :

```bash
# Installer Vercel CLI
npm i -g vercel

# Dans le dossier frontend/
cd frontend
vercel

# Suivre les instructions
```

### Pour le Backend + DB (Railway) :

1. Créer projet Railway avec PostgreSQL
2. Créer Web Service pour le backend
3. Connecter GitHub repo
4. Définir Dockerfile : `docker/Dockerfile.backend`

---

## Option 4 : Déploiement Docker manuel (VPS)

### Si tu as un VPS (DigitalOcean, AWS, etc.) :

```bash
# Sur le serveur
git clone https://github.com/Riotic/GDEMusiqueWebsite.git
cd GDEMusiqueWebsite

# Copier et adapter les variables d'environnement
cp .env.example .env

# Lancer avec Docker Compose
docker-compose -f docker/docker-compose.yml up -d

# Configurer Nginx reverse proxy (optionnel)
```

---

## 📝 Variables d'environnement requises

Pour la production, créer un fichier `.env` :

```env
# PostgreSQL
POSTGRES_USER=gdemusique
POSTGRES_PASSWORD=CHANGE_ME_SECURE_PASSWORD
POSTGRES_DB=gde_musique_db
DATABASE_URL=postgresql://gdemusique:PASSWORD@postgres:5432/gde_musique_db

# Backend
SECRET_KEY=CHANGE_ME_VERY_SECURE_SECRET_KEY_MIN_32_CHARS
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Frontend
API_URL=https://your-backend-url.com/api
```

---

## ✅ Checklist avant déploiement

- [ ] Changer `SECRET_KEY` dans les variables d'env
- [ ] Changer le mot de passe PostgreSQL
- [ ] Mettre à jour `CORS_ORIGINS` dans `backend/main.py` avec l'URL de production
- [ ] Tester la connexion en local d'abord
- [ ] Vérifier que le seed data fonctionne
- [ ] Tester sur mobile (responsive)

---

## 🔒 Sécurité pour Production

### Dans `backend/main.py`, modifier CORS :

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.com",
        "https://www.your-frontend-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Dans `frontend/static/js/*.js`, changer API_URL :

```javascript
const API_URL = 'https://your-backend-domain.com/api';
```

---

## 🎯 URLs de démo recommandées

- **Frontend** : `https://gde-musique.vercel.app`
- **Backend API** : `https://gde-api.railway.app`
- **PostgreSQL** : Géré automatiquement par Railway

---

## 💡 Conseils

1. **Railway** = Le plus simple pour full-stack avec Docker
2. **Render** = Alternative gratuite mais services s'endorment
3. **Vercel** = Parfait pour le frontend uniquement
4. **Netlify** = Alternative à Vercel

**Mon choix pour une démo rapide : Railway** 🚂

Temps total : **5-10 minutes** pour un site en ligne complet !

---

## 🐛 Dépannage

### Le backend ne se connecte pas à la DB :
- Vérifier `DATABASE_URL` dans les variables d'env
- Vérifier que PostgreSQL est démarré

### CORS errors :
- Vérifier `allow_origins` dans `backend/main.py`
- Ajouter l'URL du frontend en production

### Seed data ne s'exécute pas :
- Vérifier les logs du backend
- Peut-être désactiver le seed en prod (retirer de `docker-compose.yml`)

---

Besoin d'aide ? Ouvre une issue GitHub ! 🚀
