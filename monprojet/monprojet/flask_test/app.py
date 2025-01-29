from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")
INDEX_NAME = "recettes"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search']
        body = {
            "query": {
                "match": {
                    "titre": search_term
                }
            }
        }
        results = es.search(index=INDEX_NAME, body=body)
        return render_template('index.html', results=results['hits']['hits'])
    
    return render_template('index.html')

@app.route('/recette/<id>')
def recette(id):
    result = es.get(index=INDEX_NAME, id=id)
    return render_template('recette.html', recette=result['_source'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)