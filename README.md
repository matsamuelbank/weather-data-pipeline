# weather-data-pipeline

Pipeline ETL Python pour collecter, transformer et charger des donnees meteo.

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

## Demarrage

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Renseigne ensuite tes variables locales dans `.env`.

## PostgreSQL avec Docker

`docker-compose.yml` lit les variables depuis `.env`.

```bash
docker compose up -d
docker ps
```

Le mapping de ports est defini par `POSTGRES_PORT_EXTERNAL` et `POSTGRES_PORT_INTERNAL`.

## Bloc 3 - Etape 1: API Extract

Objectif de cette branche: recuperer des donnees meteo depuis l'API Open-Meteo et sauvegarder le JSON brut dans `data/raw/`.

```bash
python src/main.py
```

Sur cette etape, tu dois verifier:
- la requete HTTP
- le code de retour API
- la structure du JSON recu
- les cles utiles dans `data["hourly"]`

## Bloc 3 - Etape 2: Pandas Transform

Objectif de cette branche: transformer le JSON brut en DataFrame propre puis exporter le resultat dans `data/processed/`.

Points a verifier sur cette etape:
- creation du DataFrame a partir de `data["hourly"]`
- conversion de la colonne `time` en date
- ajout de la colonne `city`
- suppression des lignes nulles
- export CSV pour controler le resultat

## Bloc 3 - Etape 3: SQLAlchemy Load

Objectif de cette branche: connecter Python a PostgreSQL puis charger le DataFrame transforme dans la table `weather_measurements`.

Points a verifier sur cette etape:
- construction de l'URL de connexion PostgreSQL
- creation du moteur SQLAlchemy
- insertion du DataFrame avec `to_sql`
- verification du nombre de lignes chargees

## Bloc 3 - Etape 4: SQL Analysis

Objectif de cette branche: analyser les donnees chargees avec des requetes SQL simples et lisibles.

Points a verifier sur cette etape:
- compter les lignes inserees
- afficher les mesures recentes
- calculer une temperature moyenne par ville
- calculer une temperature max par jour
- lire une requete SQL depuis Python avec Pandas
