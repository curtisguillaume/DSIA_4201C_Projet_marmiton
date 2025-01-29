from flask import render_template, request
from elasticsearch import Elasticsearch

from app import app

# Connexion à Elasticsearch
es = Elasticsearch("http://localhost:9200")

@app.route("/", methods=["GET", "POST"])
def index():
    recipes = []
    query = ""

    if request.method == "POST":
        query = request.form.get("query")
        
        # Rechercher les recettes par titre
        body = {
            "query": {
                "match": {
                    "titre": query
                }
            }
        }
        
        res = es.search(index="recettes", body=body)
        
        # Extraire les résultats
        recipes = [hit["_source"] for hit in res["hits"]["hits"]]
    
    return render_template("index.html", recipes=recipes, query=query)


