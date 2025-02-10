from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import time

app = Flask(__name__)
es = Elasticsearch("http://elasticsearch:9200/")
while not es.ping():
    print("Attente de la connexion à Elasticsearch...")
    time.sleep(5)

print("Connexion réussie à Elasticsearch!")

INDEX_NAME = "recettes"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search']
        difficulte = request.form.get('difficulte', '').strip().lower()
        prix = request.form.get('prix', '').strip().lower()

        # Construction de la requête Elasticsearch
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "titre": {
                                    "query": search_term,
                                    "fuzziness": "AUTO"
                                }
                            }
                        }
                    ],
                    "filter": []
                }
            }
        }

        # Ajout des filtres si ils sont spécifiés
        if difficulte:
            body["query"]["bool"]["filter"].append({"term": {"difficulte.keyword": difficulte}})
        if prix:
            body["query"]["bool"]["filter"].append({"term": {"prix.keyword": prix}})

        print(f"Requête Elasticsearch: {body}")  # Ajoutez cette ligne pour déboguer

        results = es.search(index=INDEX_NAME, body=body)
        return render_template('index.html', results=results['hits']['hits'])

    return render_template('index.html')

@app.route('/recette/<id>')
def recette(id):
    result = es.get(index=INDEX_NAME, id=id)
    return render_template('recette.html', recette=result['_source'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
