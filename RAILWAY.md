# 🚂 Railway Deployment Guide

## Étapes de déploiement sur Railway

### 1. Créer la base de données PostgreSQL

1. Sur Railway → **New** → **Database** → **PostgreSQL**
2. Railway crée automatiquement la DB et génère `DATABASE_URL`

### 2. Déployer le Backend

1. **New** → **GitHub Repo** → Sélectionner `GDEMusiqueWebsite`
2. Railway détecte `railway.toml` automatiquement

#### Variables d'environnement à ajouter :

- `DATABASE_URL` : **Reference** depuis le service Postgres
- `SECRET_KEY` : Générer une valeur aléatoire (32+ caractères)
- `PORT` : Railway la définit automatiquement

#### Vérifier la configuration :

- **Root Directory**: `/` (racine du projet)
- **Dockerfile Path**: `docker/Dockerfile.backend`
- **Start Command**: Défini dans `railway.toml`

### 3. Déployer le Frontend (optionnel sur Railway)

**Option A : Nginx sur Railway**
1. **New** → **Empty Service**
2. Settings → **Dockerfile Path**: `docker/Dockerfile.frontend`
3. Generate Domain

**Option B : Vercel (recommandé pour le frontend)**
```bash
cd frontend
vercel --prod
```

### 4. Connecter les services

1. Dans le service **Backend** → **Variables**
2. Cliquer **+ New Variable**
3. Sélectionner **Reference** → Postgres → `DATABASE_URL`

### 5. Générer le domaine public

1. Backend service → **Settings** → **Generate Domain**
2. URL type: `gde-backend-production.up.railway.app`

### 6. Tester

```bash
curl https://your-backend-url.up.railway.app/health
```

Résultat attendu :
```json
{"status":"healthy","version":"2.0.0"}
```

### 7. Accéder depuis ton téléphone

Frontend sur Vercel : `https://gde-musique.vercel.app`
- Ouvre depuis Safari/Chrome
- Connecte-toi : `admin@gde-musique.fr` / `admin123`
- ✅ Fonctionne depuis n'importe où !

---

## 🔧 Troubleshooting

### "could not translate host name postgres"

❌ **Problème** : Railway n'utilise pas docker-compose, donc le hostname `postgres` n'existe pas.

✅ **Solution** : Assure-toi que `DATABASE_URL` est bien définie comme **Reference** depuis Postgres.

### Seed ne s'exécute pas

Vérifier les logs :
1. Backend service → Deployments
2. Cliquer sur le dernier deployment
3. Voir les logs

### CORS errors

Mettre à jour `backend/main.py` avec l'URL du frontend :
```python
allow_origins=[
    "https://your-frontend.vercel.app",
    "https://gde-musique.vercel.app"
]
```

---

## ✅ Checklist

- [ ] PostgreSQL créé sur Railway
- [ ] Backend déployé avec `DATABASE_URL` en référence
- [ ] `SECRET_KEY` défini
- [ ] Domaine généré pour le backend
- [ ] Frontend déployé (Vercel ou Railway)
- [ ] CORS configuré avec l'URL frontend
- [ ] Testé depuis le téléphone

**Temps total : 10 minutes** ⚡
