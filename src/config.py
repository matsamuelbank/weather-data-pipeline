from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# On centralise ici les chemins et variables utiles pour eviter de les disperser.
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

API_BASE_URL = "https://api.open-meteo.com/v1/forecast"
API_TIMEZONE = os.getenv("API_TIMEZONE", "Europe/Paris")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
