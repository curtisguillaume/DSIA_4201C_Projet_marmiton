from elasticsearch import Elasticsearch, helpers
import json

# Connexion à Elasticsearch
es_client = Elasticsearch("http://localhost:9200")

es_client.ping()

# Chemin vers le fichier JSON
json_file_path = "D:/Moi/ESIEE/DSIA4201C/DSIAS1P2C/Projet/DSIA_4201C_Projet_marmiton/monprojet/monprojet/data/recettes2.json"


# Charger le fichier JSON
with open(json_file_path, "r", encoding="utf-8") as file:
    recettes = json.load(file)

# Nom de l'index Elasticsearch
index_name = "recettes"

# Vérifier si l'index existe déjà, sinon le créer
if not es_client.indices.exists(index=index_name):
    es_client.indices.create(index=index_name)

# Préparer les données pour Elasticsearch
actions = [
    {
        "_index": index_name,
        "_source": recette
    }
    for recette in recettes
]

# Insérer les données dans Elasticsearch
try:
    helpers.bulk(es_client, actions)
    print(f"Les données ont été insérées avec succès dans l'index '{index_name}'.")
except Exception as e:
    print(f"Une erreur est survenue lors de l'insertion des données : {e}")
