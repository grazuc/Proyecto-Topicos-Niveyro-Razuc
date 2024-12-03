import json
from pymongo import MongoClient
import os

# Conectar a la base de datos
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client["movies_db"]

# Cargar datos desde sample_data.json
with open("sample_data.json") as f:
    movies = json.load(f)

    # Elimina todos los documentos de la colección y carga los datos nuevos
    db.movies.delete_many({})  # Elimina todos los documentos existentes
    db.movies.insert_many(movies)  # Inserta los nuevos datos
    print("Datos reemplazados correctamente en MongoDB.")
