# weather-data-pipeline

Pipeline ETL Python pour recuperer des donnees meteo depuis une API, les transformer avec Pandas, les charger dans PostgreSQL avec SQLAlchemy, puis les analyser avec SQL.

## Objectif

Ce projet sert de mini pipeline de data engineering pour pratiquer les bases suivantes :
- extraction de donnees depuis une API REST
- transformation d'un JSON en DataFrame Pandas
- chargement des donnees dans PostgreSQL
- analyse SQL simple a partir des donnees chargees

## Architecture

```text
Open-Meteo API
    ->
requests
    ->
Pandas
    ->
PostgreSQL
    ->
SQL analysis
```

## Technologies

- Python
- Pandas
- Requests
- SQLAlchemy
- PostgreSQL
- Docker

## Structure

```text
weather-data-pipeline/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── docker-compose.yml
├── sql/
│   ├── 01_create_tables.sql
│   └── 02_queries.sql
├── data/
│   ├── raw/
│   └── processed/
└── src/
    ├── main.py
    ├── config.py
    ├── extract.py
    ├── transform.py
    ├── load.py
    └── db.py
```

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
cp .env.example .env
```

Renseigner ensuite les variables locales dans `.env`.

## Variables d'environnement

Le fichier `.env` doit etre renseigne avant le lancement de PostgreSQL et du pipeline. Des valeurs vides empechent le demarrage du conteneur PostgreSQL.

Exemple minimal de configuration :

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=weather_db
POSTGRES_PORT_INTERNAL=5432
POSTGRES_PORT_EXTERNAL=5432

API_TIMEZONE=Europe/Paris
API_TIMEOUT=10

DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=weather_db
```

Sans `POSTGRES_PASSWORD`, le conteneur PostgreSQL s'arrete immediatement au demarrage.

## Lancer PostgreSQL

`docker-compose.yml` lit les variables depuis `.env`.

```bash
docker compose up -d
docker compose ps
```

Verification attendue :
- le conteneur `weather_postgres` doit etre en statut `running`
- le port `5432` doit etre expose si `POSTGRES_PORT_EXTERNAL=5432`

En cas d'echec, consulter les logs :

```bash
docker logs weather_postgres
```

## Creer la table SQL

Executer le script :

```bash
psql -h localhost -U "$DB_USER" -d "$DB_NAME" -f sql/01_create_tables.sql
```

Alternative sans client `psql` local :

```bash
docker exec -i weather_postgres psql -U postgres -d weather_db -f /dev/stdin < sql/01_create_tables.sql
```

## Lancer le pipeline

```bash
python3 src/main.py
```

Le pipeline effectue les etapes suivantes :
1. recupere les donnees meteo de Dijon depuis Open-Meteo
2. sauvegarde le JSON brut dans `data/raw/`
3. transforme les donnees en DataFrame propre
4. exporte un CSV dans `data/processed/`
5. charge les donnees dans PostgreSQL
6. execute une requete d'analyse simple depuis Python

## Visualisation simple avec Streamlit

Une interface simple permet de visualiser le pipeline en execution :

```bash
python3 -m streamlit run app.py
```

Cette interface permet :
- choisir une ville
- lancer l'extraction et la transformation
- visualiser le DataFrame et une courbe de temperature
- charger les donnees en base si PostgreSQL tourne
- afficher un apercu des donnees stockees

## Fonctionnement de l'option PostgreSQL dans Streamlit

L'option `Charger aussi dans PostgreSQL` declenche l'insertion des donnees transformees dans la table `weather_measurements`.

Conditions prealables :
- le fichier `.env` doit contenir des identifiants valides
- le conteneur PostgreSQL doit etre demarre
- la table `weather_measurements` doit exister

Si ces conditions ne sont pas remplies, l'interface peut afficher une erreur de connexion du type :
- `connection refused`
- `database is uninitialized and superuser password is not specified`

Pour un test sans base de donnees :
- laisser l'option `Charger aussi dans PostgreSQL` decochee
- laisser l'affichage PostgreSQL desactive si la base n'est pas disponible
