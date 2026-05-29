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
