
# DSIA_4201C_Projet_Marmiton_scraper

Aller a la racine du projet et executer "docker-compose up --build "
aller à http://127.0.0.1:5000/ ou http://localhost:5000/ apres 1 minutes 

# Projet Web - Application de Recettes avec Elasticsearch

## Description du Projet

Le projet consiste à créer une application web pour explorer des recettes en utilisant des données scrapées sur le site Marmiton. Ces données sont stockées dans un cluster Elasticsearch et sont affichées via une interface web construite avec Flask. L'application permet de rechercher des recettes en utilisant un moteur de recherche basé sur Elasticsearch, et de consulter les détails d'une recette au clic.

## Technologies utilisées

- **Python** : Langage de programmation pour le backend.
- **Flask** : Framework web léger pour le serveur.
- **Scrapy** : Framework pour le scraping de données.
- **Elasticsearch** : Moteur de recherche pour l'indexation et la recherche des recettes.
- **Docker** : Conteneurisation des services avec Docker et Docker Compose.
- **Kibana** : Interface de gestion et de visualisation pour Elasticsearch.

## Structure du projet

. 
├── app.py 
├── docker-compose.yml 
├── elastic 
│ └── Dockerfile.elastic 
├── flask 
│ └── Dockerfile.flask 
├── data/ 
│ └── recettes2.json 
├── scrapy_spider/ 
│ └── marmiton_spider.py 
├── templates/ 
│ ├── index.html 
│ └── recette.html 
└── README.md

## Détails des composants

### Docker Compose

Le fichier `docker-compose.yml` permet de définir et de lancer les services nécessaires à l'application. Il contient les services suivants :

- **Elasticsearch** : Service principal pour l'indexation et la recherche des données.
- **Kibana** : Interface web permettant de visualiser et gérer les données dans Elasticsearch.
- **Elastic-loader** : Service personnalisé pour charger les données dans Elasticsearch à partir d'un fichier JSON.
- **Flask** : Application web qui expose une interface utilisateur permettant d'interagir avec les données Elasticsearch.

### Scrapy Spider

Le fichier `marmiton_spider.py` contient un spider Scrapy qui scrape des recettes du site Marmiton. Les informations récupérées comprennent :

- Titre de la recette
- Difficulté
- Note
- Temps de préparation
- Prix
- Liste des ingrédients
- Liste des ustensiles
- Étapes de la recette
- Commentaire (si disponible)

Les données sont sauvegardées dans un fichier `recettes2.json` et sont ensuite chargées dans Elasticsearch.

### Elastic Loader

Le fichier `elastic.py` est utilisé pour charger les données dans Elasticsearch. Il attend que le service Elasticsearch soit disponible, puis charge les données depuis `recettes2.json` et les insère dans un index Elasticsearch nommé `recettes`.

### Application Flask

Le fichier `app.py` contient l'application Flask qui gère les routes suivantes :

- `/` : La page d'accueil qui permet de rechercher des recettes par titre. Les résultats sont récupérés via une requête Elasticsearch et affichés dans une liste.
- `/recette/<id>` : Affiche les détails d'une recette spécifique, récupérée de Elasticsearch par son ID.

### Templates HTML

- **index.html** : Formulaire de recherche des recettes et affichage des résultats sous forme de cartes cliquables.
- **recette.html** : Affiche les détails d'une recette, y compris les ingrédients, les étapes, et autres informations.


## Instructions de lancement

### Pré-requis

- Docker et Docker Compose doivent être installés sur votre machine.
- Le service Elasticsearch et Kibana doivent être disponibles via Docker.

### Lancer l'application

1. **Cloner le repository** :

   Clonez le repository sur votre machine locale.

   ```bash
   git clone <url_du_repository>
   cd <dossier_du_repository>

### Construire les images Docker :

Utilisez Docker Compose pour construire et démarrer les services.

docker-compose up --build


Cela va lancer les services Elasticsearch, Kibana, Flask et Elastic-loader dans des conteneurs Docker.

---

### Scraper les données :

Lancez le spider Scrapy pour récupérer les données de recettes depuis Marmiton et les stocker dans un fichier JSON.

scrapy crawl marmit


---

### Charger les données dans Elasticsearch :

Une fois les données récupérées, elles doivent être insérées dans Elasticsearch.

python elastic.py


---

### Accéder à l'application web :

- L'application web sera disponible à l'adresse suivante : [http://localhost:5000](http://localhost:5000).
- Kibana sera accessible à l'adresse suivante pour visualiser et gérer les données : [http://localhost:5601](http://localhost:5601).
