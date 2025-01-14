from flask import Flask, render_template, request, jsonify
import pymongo
import json
import os
from math import ceil  
from pymongo import MongoClient

# Configurer la connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["marmiton_db"]
collection = db["collection_recette"]

app = Flask(__name__)

# Chemin absolu vers le fichier JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'data', 'recettes2.json')

# Connexion à MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  # URL de votre MongoDB Docker
db = client["marmiton_db"]  # Remplacez par le nom de votre base de données
collection = db["recettes"]  # Remplacez par le nom de votre collection

# Route pour la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

# Route pour afficher les recettes
@app.route('/recettes')
def recettes():
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as file:
            recettes_data = json.load(file)
        return jsonify(recettes_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour interagir avec MongoDB (exécution de mongo_marmiton.py)
@app.route('/mongo')
def mongo_action():
    try:
        # Appel du script MongoDB (mongo_marmiton.py)
        from data.mongo_marmiton import insert_data  # Assurez-vous que insert_data est défini dans mongo_marmiton.py
        insert_data()  # Fonction à définir dans mongo_marmiton.py
        return jsonify({"message": "Données insérées avec succès dans MongoDB"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     query = request.form.get('query', '') if request.method == 'POST' else request.args.get('query', '')
#     page = int(request.args.get('page', 1))
#     per_page = 5
#     results = []

#     if query:
#         with open(JSON_PATH, 'r', encoding='utf-8') as file:
#             recettes_data = json.load(file)
        
#         # Filtrer par 'titre' au lieu de 'nom'
#         filtered_results = [recette for recette in recettes_data if query.lower() in recette.get('titre', '').lower()]
#         total_results = len(filtered_results)

#         # Pagination logic
#         start = (page - 1) * per_page
#         end = start + per_page
#         results = filtered_results[start:end]

#         total_pages = ceil(total_results / per_page)

#         return render_template('search.html', query=query, results=results, page=page, total_pages=total_pages)

#     return render_template('search.html', query=query, results=results, page=1, total_pages=1)



@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query', '')  # Récupérer le terme de recherche
    page = int(request.args.get('page', 1))  # Page actuelle (par défaut page 1)
    per_page = 5  # Nombre de résultats par page

    results = []
    total_pages = 1

    if query:

        # Affichage pour vérifier la requête
        print(f"Requête de recherche : {query}")

        # Requête MongoDB avec expression régulière (insensible à la casse)
        filtered_results = collection.find(
            { "titre": { "$regex": query, "$options": "i" } }
        )
        
        # Vérification du nombre de résultats
        filtered_results_list = list(filtered_results)
        print(f"Nombre de résultats trouvés : {len(filtered_results_list)}")
        
        # Nombre total de résultats
        total_results = len(filtered_results_list)

        # Pagination : Découper les résultats pour afficher ceux de la page actuelle
        start = (page - 1) * per_page
        end = start + per_page
        results = filtered_results_list[start:end]

        # Calculer le nombre total de pages
        total_pages = (total_results // per_page) + (1 if total_results % per_page else 0)

        # Construire une requête MongoDB pour chercher dans le champ 'titre'
        search_query = {"titre": {"$regex": query, "$options": "i"}}

        # Récupérer les résultats paginés
        total_results = collection.count_documents(search_query)
        cursor = collection.find(search_query).skip((page - 1) * per_page).limit(per_page)
        
        # Transformer les résultats en une liste de dictionnaires
        results = list(cursor)

        # Calculer le nombre total de pages
        total_pages = ceil(total_results / per_page)

        return render_template('search.html', query=query, results=results, page=page, total_pages=total_pages)

    return render_template('search.html', query=query, results=results, page=1, total_pages=1)


if __name__ == '__main__':
    app.run(debug=True)





