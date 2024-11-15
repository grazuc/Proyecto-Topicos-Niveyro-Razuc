from fastapi import FastAPI
import pika
import random
import requests
from collections import Counter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir solicitudes desde el frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recomendar")
def recomendar():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='movie_history')

    method_frame, header_frame, body = channel.basic_get(queue='movie_history', auto_ack=True)
    historial = []

    while body:
        historial.append(body.decode())
        method_frame, header_frame, body = channel.basic_get(queue='movie_history', auto_ack=True)

    connection.close()

    if not historial:
        return {"message": "No hay historial para generar recomendaciones."}

    # Obtener información de películas desde el microservicio de películas
    response = requests.get("http://movies:8000/movies")
    if response.status_code != 200:
        return {"message": "Error al comunicarse con el microservicio de películas."}

    all_movies = response.json()

    # Evitar recomendar las últimas 5 películas vistas
    peliculas_recientes = historial[-5:]

    # Filtrar películas vistas según el historial
    peliculas_vistas = [pelicula for pelicula in all_movies if pelicula['id'] in historial]
    generos_vistos = [pelicula['genre'] for pelicula in peliculas_vistas]

    if not generos_vistos:
        return {"message": "No se encontraron géneros en el historial para generar recomendaciones."}

    # Encontrar los géneros más frecuentemente vistos
    genero_preferido = Counter(generos_vistos).most_common(1)[0][0]

    # Filtrar películas no vistas del género más frecuente
    peliculas_recomendadas = [
        pelicula for pelicula in all_movies 
        if pelicula['id'] not in historial and pelicula['id'] not in peliculas_recientes and pelicula['genre'] == genero_preferido
    ]

    # Si no hay suficientes del género preferido, buscar en otros géneros
    if not peliculas_recomendadas:
        segundo_genero = Counter(generos_vistos).most_common(2)[1][0] if len(Counter(generos_vistos)) > 1 else None
        peliculas_recomendadas = [
            pelicula for pelicula in all_movies 
            if pelicula['id'] not in historial and pelicula['id'] not in peliculas_recientes and pelicula['genre'] == segundo_genero
        ]

    # Cómo última instancia, recomendar aleatoriamente
    if not peliculas_recomendadas:
        peliculas_recomendadas = [
            pelicula for pelicula in all_movies if pelicula['id'] not in historial and pelicula['id'] not in peliculas_recientes
        ]

    if peliculas_recomendadas:
        recomendacion = random.choice(peliculas_recomendadas)
        return {"recomendacion": recomendacion}
    else:
        return {"message": "No hay más películas para recomendar."}
