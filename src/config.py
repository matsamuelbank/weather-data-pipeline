from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

RAW_DATA_DIR = BASE_DIR / "data" / "raw"

API_BASE_URL = "https://api.open-meteo.com/v1/forecast"
API_TIMEZONE = os.getenv("API_TIMEZONE", "Europe/Paris")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
