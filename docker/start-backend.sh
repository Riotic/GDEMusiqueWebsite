#!/bin/sh
# Script de démarrage pour le backend Railway

echo "🎵 Starting GDE Backend..."

# Exécuter le seed
echo "📦 Running database seed..."
python seed_data.py

# Démarrer uvicorn
echo "🚀 Starting uvicorn on port ${PORT:-8000}..."
exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
