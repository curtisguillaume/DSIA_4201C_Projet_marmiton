from flask import Flask, render_template, request, jsonify
import pymongo
import json
import os
from math import ceil  

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

    return render_template('search.html', query=query, results=results, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)





