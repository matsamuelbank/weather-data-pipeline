# weather-data-pipeline

Pipeline ETL Python pour collecter, transformer et charger des donnees meteo.

## Structure

```text
weather-data-pipeline/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
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
