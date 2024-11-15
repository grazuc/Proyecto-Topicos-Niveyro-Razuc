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
    if db.movies.count_documents({}) == 0:  # Evita duplicados
        db.movies.insert_many(movies)
        print("Datos insertados correctamente en MongoDB.")
    else:
        print("Los datos ya existen en la base de datos.")
