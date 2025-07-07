Auto Dakar App est une application Streamlit qui permet de :

✅ Scraper des données de voitures sur plusieurs pages du site Dakar Auto avec nettoyage (BeautifulSoup).✅ Télécharger des données brutes issues du scraping (HTML brut).✅ Visualiser un tableau de bord des données nettoyées (tableau + graphique des prix).✅ Remplir un formulaire d’évaluation de l’application.

📂 Structure du projet

auto_dakar/
├── app_streamlit.py      # Application Streamlit principale
├── scraper_clean.py      # Scraper propre avec nettoyage
├── scraper_raw.py        # Scraper brut (HTML brut)
├── requirements.txt      # Dépendances Python
├── Dockerfile            # Image Docker
├── docker-compose.yml    # Configuration docker-compose
└── data/                 # Données exportées (nettoyées et brutes)

⚙️ Installation

Prérequis

Python 3.10+

Docker (optionnel)

Installation locale

pip install -r requirements.txt
streamlit run app_streamlit.py

Avec Docker

docker-compose up --build

Accès : http://localhost:8501

🚀 Fonctionnalités principales

Scraper propre

Lance un scraping des voitures avec nettoyage des données.

Sauvegarde un fichier data/voitures_clean.csv.

Télécharger brut

Scraping brut des pages HTML.

Téléchargement du fichier voitures_raw.html.

Dashboard

Affiche un tableau des données nettoyées.

Affiche un graphique des prix.

Évaluation

Permet de laisser un avis (enregistré dans data/evaluations.csv).

🐳 Docker Hub / Déploiement

Construire l’image :

docker build -t ton_dockerhub_username/auto_dakar_app .

Pousser sur Docker Hub :

docker push ton_dockerhub_username/auto_dakar_app

Déployer sur Render, Railway, etc. en utilisant l’image Docker.

✉️ Contact

Alioune Mbodji – Master IA - Dakar Institute of Technology
Email : ambodj92@gmail.com