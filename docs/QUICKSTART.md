# 🚀 Guide de démarrage rapide - GDE Music Platform

## Installation et lancement

### 1️⃣ Installer les dépendances

```powershell
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
.\venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt
```

### 2️⃣ Peupler la base de données (optionnel mais recommandé)

```powershell
python seed_data.py
```

Ceci créera :
- 2 utilisateurs de test
- 8 chansons de démo
- 4 playlists

### 3️⃣ Lancer le serveur

```powershell
python run.py
```

### 4️⃣ Accéder à l'application

Ouvrez votre navigateur et allez sur :
- **Frontend** : http://localhost:8000/static/index.html  
  (ou créez un raccourci vers `frontend/index.html`)

- **API Documentation** : http://localhost:8000/docs  
  (Documentation interactive Swagger)

## 🎯 Prochaines étapes

1. **Authentification JWT** - Système de connexion complet
2. **Upload de fichiers** - Permettre l'upload de fichiers audio
3. **Streaming audio** - Implémenter le streaming de fichiers audio
4. **Mode sombre** - Ajouter un toggle pour le mode sombre
5. **Favoris** - Système de favoris pour les chansons
6. **Lecteur avancé** - File d'attente, shuffle, repeat

## 📚 Endpoints API disponibles

- `GET /api/music/songs` - Liste des chansons
- `POST /api/music/songs` - Créer une chanson
- `GET /api/music/songs/{id}` - Détails d'une chanson
- `GET /api/music/songs/search/{query}` - Rechercher
- `PUT /api/music/songs/{id}/play` - Incrémenter lectures
- `GET /api/playlists` - Liste des playlists
- `POST /api/playlists` - Créer une playlist
- `POST /api/users/register` - Créer un compte

## 🎨 Animations incluses

- ✨ Animations au chargement (GSAP)
- 🎵 Wave musicale animée
- 🖱️ Effets hover sur les cartes
- 📱 Design responsive
- 🌊 Parallax sur le hero

Bon développement ! 🎉
