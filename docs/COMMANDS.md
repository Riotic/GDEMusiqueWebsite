# 📚 Commandes rapides - GDE Music Platform

## 🚀 Démarrage

```powershell
# Première installation
.\docker.ps1 init

# Démarrage normal
.\docker.ps1 start

# Avec logs visibles
docker-compose up
```

## 🔍 Monitoring

```powershell
# Voir tous les logs
.\docker.ps1 logs

# Logs du backend uniquement
.\docker.ps1 logs-backend

# Logs du frontend
.\docker.ps1 logs-frontend

# Logs de la base de données
.\docker.ps1 logs-db

# État des services
.\docker.ps1 ps
```

## 🔄 Gestion

```powershell
# Redémarrer tous les services
.\docker.ps1 restart

# Arrêter les services
.\docker.ps1 stop

# Reconstruire après modification du code
.\docker.ps1 rebuild
```

## 🧹 Nettoyage

```powershell
# Nettoyer (garde les images)
.\docker.ps1 clean

# Nettoyer complètement (supprime tout)
.\docker.ps1 clean-all
```

## 🐚 Accès aux shells

```powershell
# Shell du backend
.\docker.ps1 shell-backend

# Shell PostgreSQL
.\docker.ps1 shell-db
```

## 💾 Base de données

```powershell
# Accéder à PostgreSQL
docker exec -it gde_postgres psql -U gde_user -d gde_music

# Sauvegarder la DB
docker exec gde_postgres pg_dump -U gde_user gde_music > backup.sql

# Restaurer la DB
docker exec -i gde_postgres psql -U gde_user gde_music < backup.sql

# Réinitialiser la DB
docker-compose down -v
docker-compose up -d
```

## 🧪 Tests

```powershell
# Tester l'API
curl http://localhost:8000/health
curl http://localhost:8000/api/music/songs

# Exécuter les tests de santé
python test_health.py
```

## 🛠️ Développement

```powershell
# Reconstruire uniquement le backend
docker-compose up -d --build backend

# Reconstruire uniquement le frontend
docker-compose up -d --build frontend

# Voir les ressources utilisées
docker stats

# Nettoyer les images inutilisées
docker system prune -a
```

## 📦 Docker Compose (commandes brutes)

```powershell
# Démarrer
docker-compose up -d

# Démarrer avec build
docker-compose up -d --build

# Arrêter
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v

# Voir les logs
docker-compose logs -f

# Lister les containers
docker-compose ps

# Redémarrer un service
docker-compose restart backend
```

## 🌐 URLs d'accès

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **API Docs (Swagger)** : http://localhost:8000/docs
- **API Docs (ReDoc)** : http://localhost:8000/redoc
- **PostgreSQL** : localhost:5432

## 🔑 Credentials par défaut

- **PostgreSQL**
  - User: `gde_user`
  - Password: `gde_password`
  - Database: `gde_music`

- **Demo User**
  - Username: `demo_user`
  - Email: `demo@gde.music`
  - Password: `demo123`

## ⚡ Raccourcis Make (Linux/Mac)

```bash
make init          # Initialisation complète
make up            # Démarrer
make down          # Arrêter
make logs          # Voir les logs
make restart       # Redémarrer
make clean         # Nettoyer
make rebuild       # Reconstruire
```

## 🐛 Dépannage courant

### Port déjà utilisé

```powershell
# Changer les ports dans docker-compose.yml
ports:
  - "8080:80"  # Au lieu de 3000:80
```

### Erreur de permission

```powershell
# Windows : Exécuter PowerShell en admin
# Linux : Ajouter sudo devant les commandes
```

### Le container ne démarre pas

```powershell
# Voir les logs d'erreur
docker-compose logs backend

# Reconstruire depuis zéro
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### La base de données ne se connecte pas

```powershell
# Vérifier que PostgreSQL est démarré
docker-compose ps

# Vérifier la santé
docker exec gde_postgres pg_isready

# Redémarrer PostgreSQL
docker-compose restart postgres
```

## 📊 Commandes utiles

```powershell
# Voir la taille des volumes
docker system df

# Inspecter un container
docker inspect gde_backend

# Voir les processus dans un container
docker top gde_backend

# Copier un fichier depuis/vers un container
docker cp gde_backend:/app/file.txt ./
docker cp ./file.txt gde_backend:/app/
```

---

**Astuce** : Gardez cette page sous la main pour un accès rapide aux commandes ! 🚀
