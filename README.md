# BFSCORE

BFSCORE est un projet conçu pour analyser les scores des matchs de football. Ce projet utilise des technologies telles que Java, Hadoop, Spark et Python pour traiter et analyser les données de matchs de football stockées dans un fichier CSV.

Table des matières

    1.  Introduction
    2.  Technologies utilisées
    3.  Étapes pour lancer l'application
    4.  Structure du projet
    5.  Auteurs


### Introduction

BFSCORE est un projet qui permet d'analyser les scores des matchs de football de la Bundesliga. Le projet utilise un backend Flask pour servir des pages web et des API, et Spark pour le traitement et l'analyse des données.
Technologies utilisées

- Java : Utilisé pour les composants nécessitant des performances élevées et une gestion efficace de la mémoire.

- Hadoop : Utilisé pour le stockage et le traitement distribué de grandes quantités de données.

- Spark : Utilisé pour le traitement distribué rapide des données et l'analyse avancée.

- Python : Utilisé pour le développement de scripts d'analyse et de traitement des données, ainsi que pour le backend Flask.

- Flask : Framework web utilisé pour développer l'application backend.


Prérequis

    Python 
    Java 
    Apache Hadoop
    Apache Spark
    Flask




### Étapes pour lancer l'application

Exécutez les commandes suivantes pour construire l'image Docker, lancer un conteneur à partir de cette image, et vérifier que le conteneur est en cours d'exécution :

```sh
# 1. Construire l'image Docker et le container  à partir du dossier Projet_final
docker compose up -d

# 3. Vérifier que le conteneur est en cours d'exécution
docker ps

# 4. Acceder a l'application
http://localhost:5000


```






### Structure du projet

    Projet_final
           |_app
           |     |_results
           |     |        |_football_matches.csv
           |     |_static
           |     |        |_css
           |     |        |    |_details.css
           |     |        |    |_info.css
           |     |        |    |_style.css
           |     |        |_img
           |     |        |    |_imgfootball.jpeg
           |     |        |    |_logo_PSG.jpeg
           |     |        |    |_logo_real_madrid.jpeg
           |     |        |    |_logo.jpeg
           |     |        |_js
           |     |            |_script.js
           |     |_templates
           |     |          |_index.html
           |     |          |_match_info.html       
           |     |          |_team_details.html        
           |     |_app.py
           |     |_requirements.txt
           |
           |_docker-compose.yml
           |_Dockerfile

  

### Auteurs

   * KUICHEU Berol  : Developpeur Full-Stack 
   * AMENOUGLO Fabrice : Developpeur Frontend 
   * NGOUBE Joël : Devops et infrastructure 
   * BAMBA Aboubakar :  Developpeur Frontend 



