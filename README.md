# weather-data-pipeline

Pipeline ETL Python pour recuperer des donnees meteo depuis une API, les transformer avec Pandas, les charger dans PostgreSQL avec SQLAlchemy, puis les analyser avec SQL.

## Objectif

Ce projet sert de mini pipeline data engineering pour pratiquer les bases suivantes :
- extraction de donnees depuis une API REST
- transformation de JSON en DataFrame Pandas
- chargement de donnees dans PostgreSQL
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
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Renseigne ensuite tes variables locales dans `.env`.

## Variables d'environnement

Exemple minimal :

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

## Lancer PostgreSQL

`docker-compose.yml` lit les variables depuis `.env`.

```bash
docker compose up -d
docker ps
```

## Creer la table SQL

Lancer le script :

```bash
psql -h localhost -U "$DB_USER" -d "$DB_NAME" -f sql/01_create_tables.sql
```

## Lancer le pipeline

```bash
python src/main.py
```

Le pipeline fait les etapes suivantes :
1. recupere les donnees meteo de Dijon depuis Open-Meteo
2. sauvegarde le JSON brut dans `data/raw/`
3. transforme les donnees en DataFrame propre
4. exporte un CSV dans `data/processed/`
5. charge les donnees dans PostgreSQL
6. execute une petite requete d'analyse depuis Python

## Requetes SQL disponibles

Dans [sql/02_queries.sql](/Users/samuelb/Workflow/formation-data/cours-docker/weather-data-pipeline/sql/02_queries.sql) :
- nombre total de lignes chargees
- dernieres mesures inserees
- temperature moyenne par ville
- temperature maximale par jour
- vitesse du vent moyenne par jour
- heures ou il fait plus de 25 degres

## Competences pratiquees

Ce projet montre que tu sais :
- appeler une API avec `requests`
- lire et comprendre un JSON
- transformer des donnees avec Pandas
- convertir des dates et nettoyer des lignes nulles
- connecter Python a PostgreSQL avec SQLAlchemy
- charger un DataFrame avec `to_sql`
- faire des requetes SQL simples pour analyser les donnees

## Branches du projet

- `setup-project`
- `feature-docker-postgres`
- `feature-api-extract`
- `feature-pandas-transform`
- `feature-sqlalchemy-load`
- `feature-sql-analysis`
- `docs-readme`
