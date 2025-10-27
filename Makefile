# Makefile pour GDE - Grande École de Musique
# Facilite l'utilisation de Docker Compose

.PHONY: help build up down logs clean restart shell-backend shell-db

# Couleurs pour les messages
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

# Fichier docker-compose
COMPOSE_FILE := docker/docker-compose.yml

help: ## Afficher cette aide
	@echo "$(GREEN)GDE - Commandes Docker$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

build: ## Construire les images Docker
	@echo "$(GREEN)🏗️  Construction des images...$(NC)"
	docker-compose -f $(COMPOSE_FILE) build

up: ## Démarrer tous les services
	@echo "$(GREEN)🚀 Démarrage des services...$(NC)"
	docker-compose -f $(COMPOSE_FILE) up -d
	@echo "$(GREEN)✅ Services démarrés!$(NC)"
	@echo "Site Web: http://localhost:3000"
	@echo "Backend API: http://localhost:8000"
	@echo "Health Check: http://localhost:8000/health"

down: ## Arrêter tous les services
	@echo "$(YELLOW)⏹️  Arrêt des services...$(NC)"
	docker-compose -f $(COMPOSE_FILE) down

logs: ## Afficher les logs de tous les services
	docker-compose -f $(COMPOSE_FILE) logs -f

logs-backend: ## Afficher les logs du backend
	docker-compose -f $(COMPOSE_FILE) logs -f backend

logs-frontend: ## Afficher les logs du frontend
	docker-compose -f $(COMPOSE_FILE) logs -f frontend

logs-db: ## Afficher les logs de PostgreSQL
	docker-compose -f $(COMPOSE_FILE) logs -f postgres

restart: ## Redémarrer tous les services
	@echo "$(YELLOW)🔄 Redémarrage...$(NC)"
	docker-compose -f $(COMPOSE_FILE) restart

restart-backend: ## Redémarrer le backend
	docker-compose -f $(COMPOSE_FILE) restart backend

restart-frontend: ## Redémarrer le frontend
	docker-compose -f $(COMPOSE_FILE) restart frontend

shell-backend: ## Accéder au shell du backend
	docker exec -it gde_backend sh

shell-db: ## Accéder au shell PostgreSQL
	docker exec -it gde_postgres psql -U gde_user -d gde_music

clean: ## Nettoyer (supprimer containers et volumes)
	@echo "$(YELLOW)🧹 Nettoyage...$(NC)"
	docker-compose -f $(COMPOSE_FILE) down -v
	@echo "$(GREEN)✅ Nettoyage terminé$(NC)"

clean-all: ## Nettoyer tout (containers, volumes, images)
	@echo "$(YELLOW)🧹 Nettoyage complet...$(NC)"
	docker-compose -f $(COMPOSE_FILE) down -v --rmi all
	@echo "$(GREEN)✅ Nettoyage complet terminé$(NC)"

rebuild: clean build up ## Reconstruire complètement

rebuild-backend: ## Reconstruire uniquement le backend
	docker-compose -f $(COMPOSE_FILE) up -d --build backend

rebuild-frontend: ## Reconstruire uniquement le frontend
	docker-compose -f $(COMPOSE_FILE) up -d --build frontend

ps: ## Afficher l'état des services
	docker-compose -f $(COMPOSE_FILE) ps

dev: ## Démarrer en mode développement avec logs
	@echo "$(GREEN)🚀 Démarrage en mode développement...$(NC)"
	docker-compose -f $(COMPOSE_FILE) up --build

init: build up ## Initialisation complète du projet
	@echo "$(GREEN)✅ Projet initialisé!$(NC)"
	@echo ""
	@echo "Accédez au site:"
	@echo "  Site Web: http://localhost:3000"
	@echo "  Backend API: http://localhost:8000"
	@echo "  Health Check: http://localhost:8000/health"
