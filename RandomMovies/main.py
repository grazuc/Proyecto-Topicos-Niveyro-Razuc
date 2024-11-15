from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import random

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir solicitudes desde el frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

MOVIES_SERVICE_URL = "http://movies:8000/movies"

@app.get("/random")
async def get_random_movies(count: int = 5):
    async with httpx.AsyncClient() as client:
        response = await client.get(MOVIES_SERVICE_URL)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error fetching movies")

        movies = response.json()
        if len(movies) < count:
            raise HTTPException(status_code=400, detail="Not enough movies available")

        return random.sample(movies, count)
