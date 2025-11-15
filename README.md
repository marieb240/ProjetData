# **Airbnb Paris Dashboard - Projet Data ESIEE**
Projet pour l'unité Python : Programmation avancée.

## 1. User Guide
**Installation** 

*Clôner le dépot*  
git clone https://github.com/marieb240/ProjetData.git dataprojet  
cd dataprojet  

*Créer un environnement virtuel*  
python -m venv .venv  
.venv\Scripts\activate  

*Installer les dépendances*  
python -m pip install -r requirements.txt  

*Lancer le dashboard*  
python main.py  
Le dashboard s’ouvre à l’adresse suivante : http://127.0.0.1:8050/  

## 2. Data  
Le projet utilise le dataset “Airbnb Listings & Reviews” publié par Airbnb / Maven Analytics, sous licence CC BY 4.0.  

Lien : https://mavenanalytics.io/data-playground/airbnb-listings-reviews  

**Structure des données**  
Les données sont organisées en deux répertoires :  

data puis   
raw/ où il y a les données brutes téléchargées depuis Maven  
cleaned/ où il y a les données nettoyées, utilisées par le dashboard  

**Pipeline de traitement**  
Le projet comporte 3 scripts dédiés :  

``get_data.py``  
Récupère les données brutes en ligne et les stocke dans data/raw  

``clean_data.py``  
Supprime les valeurs manquantes, convertit les types, filtre les valeurs extrêmes, prépare un dataset exploitable  

``build_db.py``  
Génère une base SQLite locale pour le chargement rapide par le dashboard  

Le dashboard utilise ensuite ``load_dataframe()`` (dans src/utils/data_access.py) pour charger les données nettoyées.  

## 3. Developer Guide 

<img width="1883" height="284" alt="image" src="https://github.com/user-attachments/assets/0b7aa99e-9aac-496c-94c6-e6f467334188" />  

## 4. Rapport d’analyse  
Cette étude met en évidence plusieurs tendances du marché Airbnb parisien :  

**Distribution des prix**  
+ La plupart des annonces se situent entre **50** € et **150 €** par nuit,
+ Les prix supérieurs à **300 €** sont rares et concentrés dans les quartiers les plus prestigieux

**Types de logements**  
+ Les logements entiers (appartements) représentent la majorité de l’offre,
+ Les chambres privées (chez l'habitant) constituent la seconde catégorie la plus courante.

**Variations géographiques**  
+ Les arrondissements les plus chers sont :  
**1er, 6e, 7e, 8e, 16e**
+ Les arrondissements périphériques présentent des niveaux de prix plus abordables

Du fait de l’attractivité touristique de Paris, les arrondissements situés au centre de la capitale et à proximité des principaux monuments historiques (Louvre, Tour Eiffel, Notre-Dame, Champs-Élysées) concentrent une forte demande.  
Logiquement, ce sont également les quartiers où les prix des logements Airbnb sont les plus élevés car ils sont les plus recherchés par les visiteurs.  


## 5. Nos perspectives  
Si nous avions eu plus de temps, nous aurions ajouté à ce dashboard **une analyse comparative entre Paris et une autre grande ville** présente dans notre dataset, comme New York. Comparer deux métropoles touristiques majeures permet de mettre en lumière des tendances opposées ou similaires : niveaux de prix, types de logements, attractivité des quartiers ou  dynamiques de marché.  

C’est pour cette raison que nous avons choisi d’utiliser **un dataset initial de grande taille**, contenant plusieurs villes. Dès le début du projet, nous avons structuré notre code afin de pouvoir facilement charger une seconde ville : la fonction **``load_dataframe()`` peut être adaptée pour filtrer les données** par ville, et la structure multipage du dashboard permet déjà d’ajouter rapidement une page “New York” ou une page “Comparaison Paris vs New York”  

Ainsi, même si cette partie n’a pas pu être développée dans le temps imparti, le projet est déjà conçu pour évoluer naturellement vers une version multi villes plus complète.

## 6. Copyright  
Je déclare sur l’honneur que :  











