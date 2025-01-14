import pymongo
import json
import os

def insert_data():
    # Connexion à MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # URI de MongoDB
    db = client["marmiton_db"]
    collection = db["collection_recette"]

    # Chemin absolu vers le fichier JSON
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Chemin du fichier actuel
    JSON_PATH = os.path.join(BASE_DIR, 'recettes2.json')  # Chemin absolu vers recettes2.json

    # Chargement du fichier JSON
    with open(JSON_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Insertion des documents JSON dans la collection
    collection.insert_many(data)
    print("Documents insérés avec succès!")
