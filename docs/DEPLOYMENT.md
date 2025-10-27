# 🚀 Guide de déploiement - GDE Music Platform

Ce guide vous accompagne dans le déploiement de l'application en production.

## 📋 Prérequis

- Serveur Linux (Ubuntu 20.04+ recommandé)
- Docker & Docker Compose installés
- Nom de domaine configuré (optionnel mais recommandé)
- Certificats SSL (Let's Encrypt recommandé)

## 🔧 Configuration

### 1. Préparer les variables d'environnement

Créez un fichier `.env` à la racine :

```bash
# Base de données
POSTGRES_DB=gde_music_prod
POSTGRES_USER=gde_admin
POSTGRES_PASSWORD=CHANGEZ_MOI_MOT_DE_PASSE_SECURISE

# Backend
SECRET_KEY=GENEREZ_UNE_CLE_SECRETE_AVEC_OPENSSL_RAND_HEX_32
DEBUG=False
ALLOWED_ORIGINS=https://votredomaine.com

# Ports (optionnel)
FRONTEND_PORT=80
BACKEND_PORT=8000
```

### 2. Générer une clé secrète

```bash
openssl rand -hex 32
```

Copiez le résultat dans `SECRET_KEY`.

## 🌐 Déploiement

### Option 1 : Déploiement simple (HTTP)

```bash
# Cloner le repo
git clone https://github.com/Riotic/GDEMusiqueWebsite.git
cd GDEMusiqueWebsite

# Créer le fichier .env (voir ci-dessus)
nano .env

# Lancer en production
docker-compose -f docker-compose.prod.yml up -d
```

### Option 2 : Déploiement avec HTTPS (Recommandé)

#### Installer Certbot

```bash
sudo apt update
sudo apt install certbot
```

#### Obtenir un certificat SSL

```bash
sudo certbot certonly --standalone -d votredomaine.com
```

#### Configurer Nginx pour HTTPS

Modifiez `nginx.conf` pour ajouter :

```nginx
server {
    listen 443 ssl http2;
    server_name votredomaine.com;

    ssl_certificate /etc/letsencrypt/live/votredomaine.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/votredomaine.com/privkey.pem;

    # ... reste de la configuration
}

server {
    listen 80;
    server_name votredomaine.com;
    return 301 https://$server_name$request_uri;
}
```

#### Lancer avec les certificats

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 🔒 Sécurité

### Pare-feu

```bash
# UFW (Ubuntu)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp  # SSH
sudo ufw enable
```

### Mise à jour automatique des certificats

```bash
# Ajouter au crontab
sudo crontab -e

# Ajouter cette ligne
0 0 * * * certbot renew --quiet && docker-compose -f /chemin/vers/docker-compose.prod.yml restart frontend
```

## 📊 Monitoring

### Voir les logs

```bash
# Tous les services
docker-compose -f docker-compose.prod.yml logs -f

# Un service spécifique
docker-compose -f docker-compose.prod.yml logs -f backend
```

### Vérifier l'état des services

```bash
docker-compose -f docker-compose.prod.yml ps
```

### Stats des ressources

```bash
docker stats
```

## 🔄 Mise à jour

```bash
# Récupérer les dernières modifications
git pull

# Reconstruire et redémarrer
docker-compose -f docker-compose.prod.yml up -d --build
```

## 💾 Sauvegarde

### Sauvegarder la base de données

```bash
# Exporter
docker exec gde_postgres_prod pg_dump -U gde_admin gde_music_prod > backup.sql

# Importer
docker exec -i gde_postgres_prod psql -U gde_admin gde_music_prod < backup.sql
```

### Sauvegarder les médias

```bash
# Créer une archive
docker run --rm -v gde_media_files:/data -v $(pwd):/backup ubuntu tar czf /backup/media-backup.tar.gz /data
```

## 🐛 Dépannage

### Le backend ne démarre pas

```bash
# Vérifier les logs
docker-compose -f docker-compose.prod.yml logs backend

# Vérifier la connexion à PostgreSQL
docker exec gde_postgres_prod pg_isready -U gde_admin
```

### Erreur de connexion à la base de données

```bash
# Recréer la base de données
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d
```

### Problème de certificats SSL

```bash
# Vérifier l'expiration
sudo certbot certificates

# Renouveler manuellement
sudo certbot renew
```

## 🎯 Optimisations pour la production

### 1. Activer la compression Nginx

Dans `nginx.conf`, ajoutez :

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;
```

### 2. Configurer les workers du backend

Dans `docker-compose.prod.yml`, ajustez le nombre de workers :

```yaml
command: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3. Limiter les ressources

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

## 📈 Scalabilité

Pour scaler l'application :

```bash
# Augmenter le nombre d'instances du backend
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

## 🔗 Services recommandés

- **Monitoring** : Prometheus + Grafana
- **Logs** : ELK Stack (Elasticsearch, Logstash, Kibana)
- **CDN** : Cloudflare
- **Backup** : AWS S3, Backblaze B2
- **CI/CD** : GitHub Actions (déjà configuré)

## ✅ Checklist de déploiement

- [ ] Variables d'environnement configurées
- [ ] Clé secrète générée et sécurisée
- [ ] Certificats SSL installés
- [ ] Pare-feu configuré
- [ ] Sauvegarde automatique configurée
- [ ] Monitoring en place
- [ ] DNS configuré
- [ ] Test de charge effectué

Bon déploiement ! 🚀
