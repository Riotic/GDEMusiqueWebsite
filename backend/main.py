from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="GDE - Grande École de Musique",
    description="API pour le site vitrine de GDE",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monter les fichiers statiques
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/")
async def root():
    return {"message": "Bienvenue sur le site de GDE - Grande École de Musique"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
