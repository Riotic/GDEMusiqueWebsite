"""
Healthcheck endpoint pour Docker
"""
from fastapi import status

@app.get("/health", status_code=status.HTTP_200_OK, tags=["health"])
async def health_check():
    """Vérifier l'état de santé de l'application"""
    return {
        "status": "healthy",
        "service": "GDE Music Platform API",
        "version": "1.0.0"
    }

@app.get("/readiness", status_code=status.HTTP_200_OK, tags=["health"])
async def readiness_check():
    """Vérifier si l'application est prête à recevoir du trafic"""
    try:
        # Vérifier la connexion à la base de données
        from backend.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {
            "status": "ready",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "not_ready",
            "database": "disconnected",
            "error": str(e)
        }
