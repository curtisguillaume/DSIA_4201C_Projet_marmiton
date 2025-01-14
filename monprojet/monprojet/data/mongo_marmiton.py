import pymongo
import json

# Connexion à MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Remplacez par l'URI de votre MongoDB si nécessaire
db = client["marmiton_db"]  # Remplacez par le nom de votre base de données
collection = db["collection_recette"]  # Remplacez par le nom de votre collection

# Chargement du fichier JSON avec encodage UTF-8
with open('recettes2.json', encoding='utf-8') as file:
    data = json.load(file)  # Charge le contenu du fichier JSON

# Insertion des documents JSON dans la collection
collection.insert_many(data)

print("Documents insérés avec succès!")
