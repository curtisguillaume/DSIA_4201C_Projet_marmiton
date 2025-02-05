from elasticsearch import Elasticsearch, helpers
import json
import time

# Connexion à Elasticsearch
es_client = Elasticsearch("http://elasticsearch:9200/")  # Utilise le nom du service Docker, pas localhost

# Attendre que le service Elasticsearch soit prêt
while not es_client.ping():
    print("Attente de la connexion à Elasticsearch...")
    time.sleep(5)

print("Connexion réussie à Elasticsearch!")

# Chemin vers le fichier JSON
json_file_path = "data/recettes2.json"

# Charger le fichier JSON
with open(json_file_path, "r", encoding="utf-8") as file:
    recettes = json.load(file)

# Nom de l'index Elasticsearch
index_name = "recettes"

# Vérifier si l'index existe déjà, sinon le créer
if not es_client.indices.exists(index=index_name):
    es_client.indices.create(index=index_name)

# Vérifier si l'index contient déjà des documents
if es_client.count(index=index_name)["count"] > 0:
    print(f"L'index '{index_name}' contient déjà des données. Importation ignorée.")
else:
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