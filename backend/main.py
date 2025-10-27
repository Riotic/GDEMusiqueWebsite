from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine
from backend import models

# Créer les tables de la base de données
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GDE - Grande École de Musique",
    description="API pour le site vitrine de GDE",
    version="2.0.0"
)

# Configuration CORS
import os
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local Docker
        "http://localhost",       # Local Dev
        FRONTEND_URL,             # Railway Frontend
        "https://gdemusique-frontend-production.up.railway.app",  # Railway Frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import des routers (après la création de app)
from backend.routers import auth, courses, marketplace, schedule

# Inclure les routeurs
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(marketplace.router, prefix="/api/marketplace", tags=["Marketplace"])
app.include_router(schedule.router, prefix="/api/schedule", tags=["Schedule"])

@app.get("/")
async def root():
    return {"message": "Bienvenue sur le site de GDE - Grande École de Musique"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}
