# GDE Music Platform - Script de gestion Docker pour Windows
# Usage: .\docker.ps1 [commande]

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

# Configuration de l'encodage UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Show-Help {
    Write-ColorOutput Green "=== GDE Music Platform - Commandes Docker ===`n"
    Write-Host "Usage: .\docker.ps1 [commande]`n"
    Write-Host "Commandes disponibles:"
    Write-Host "  start          Demarrer tous les services"
    Write-Host "  stop           Arreter tous les services"
    Write-Host "  restart        Redemarrer tous les services"
    Write-Host "  build          Construire les images Docker"
    Write-Host "  rebuild        Reconstruire et redemarrer"
    Write-Host "  logs           Afficher les logs (tous)"
    Write-Host "  logs-backend   Afficher les logs du backend"
    Write-Host "  logs-frontend  Afficher les logs du frontend"
    Write-Host "  logs-db        Afficher les logs de la DB"
    Write-Host "  ps             Afficher l'etat des services"
    Write-Host "  clean          Nettoyer (containers + volumes)"
    Write-Host "  clean-all      Nettoyer tout (+ images)"
    Write-Host "  shell-backend  Acceder au shell du backend"
    Write-Host "  shell-db       Acceder au shell PostgreSQL"
    Write-Host "  init           Initialisation complete du projet"
    Write-Host "  help           Afficher cette aide"
}

function Start-Services {
    Write-ColorOutput Green "[*] Demarrage des services..."
    docker-compose -f docker/docker-compose.yml up -d
    Write-ColorOutput Green "`n[OK] Services demarres!"
    Write-Host "Frontend: http://localhost:3000"
    Write-Host "Backend API: http://localhost:8000"
    Write-Host "API Docs: http://localhost:8000/docs"
}

function Stop-Services {
    Write-ColorOutput Yellow "[*] Arret des services..."
    docker-compose -f docker/docker-compose.yml down
}

function Restart-Services {
    Write-ColorOutput Yellow "[*] Redemarrage des services..."
    docker-compose -f docker/docker-compose.yml restart
}

function Build-Images {
    Write-ColorOutput Green "[*] Construction des images..."
    docker-compose -f docker/docker-compose.yml build
}

function Rebuild-All {
    Write-ColorOutput Yellow "[*] Reconstruction complete..."
    docker-compose -f docker/docker-compose.yml down -v
    docker-compose -f docker/docker-compose.yml build
    docker-compose -f docker/docker-compose.yml up -d
    Write-ColorOutput Green "[OK] Reconstruction terminee!"
}

function Show-Logs {
    docker-compose -f docker/docker-compose.yml logs -f
}

function Show-LogsBackend {
    docker-compose -f docker/docker-compose.yml logs -f backend
}

function Show-LogsFrontend {
    docker-compose -f docker/docker-compose.yml logs -f frontend
}

function Show-LogsDB {
    docker-compose -f docker/docker-compose.yml logs -f postgres
}

function Show-Status {
    docker-compose -f docker/docker-compose.yml ps
}

function Clean-Environment {
    Write-ColorOutput Yellow "[*] Nettoyage de l'environnement..."
    docker-compose -f docker/docker-compose.yml down -v
    Write-ColorOutput Green "[OK] Nettoyage termine"
}

function Clean-All {
    Write-ColorOutput Yellow "[*] Nettoyage complet..."
    docker-compose -f docker/docker-compose.yml down -v --rmi all
    Write-ColorOutput Green "[OK] Nettoyage complet termine"
}

function Shell-Backend {
    docker exec -it gde_backend sh
}

function Shell-DB {
    docker exec -it gde_postgres psql -U gde_user -d gde_music
}

function Initialize-Project {
    Write-ColorOutput Green "=== Initialisation du projet GDE Music Platform ===`n"
    Build-Images
    Start-Services
    Write-ColorOutput Green "`n[OK] Projet initialise avec succes!`n"
    Write-Host "Accedez a l'application:"
    Write-Host "  Frontend: http://localhost:3000"
    Write-Host "  Backend API: http://localhost:8000"
    Write-Host "  API Docs: http://localhost:8000/docs"
}

# Exécution de la commande
switch ($Command.ToLower()) {
    "start" { Start-Services }
    "stop" { Stop-Services }
    "restart" { Restart-Services }
    "build" { Build-Images }
    "rebuild" { Rebuild-All }
    "logs" { Show-Logs }
    "logs-backend" { Show-LogsBackend }
    "logs-frontend" { Show-LogsFrontend }
    "logs-db" { Show-LogsDB }
    "ps" { Show-Status }
    "clean" { Clean-Environment }
    "clean-all" { Clean-All }
    "shell-backend" { Shell-Backend }
    "shell-db" { Shell-DB }
    "init" { Initialize-Project }
    "help" { Show-Help }
    default { 
        Write-ColorOutput Red "[ERROR] Commande inconnue: $Command`n"
        Show-Help 
    }
}
