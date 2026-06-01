from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import requests

from config import API_BASE_URL, API_TIMEOUT, API_TIMEZONE, RAW_DATA_DIR


def fetch_weather_data(latitude: float, longitude: float) -> dict:
    """Fetch hourly weather data from Open-Meteo."""
    # On demande uniquement les champs utiles pour la suite du pipeline.
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": API_TIMEZONE,
    }

    response = requests.get(API_BASE_URL, params=params, timeout=API_TIMEOUT)
    response.raise_for_status()
    return response.json()


def save_raw_data(payload: dict, city: str, output_dir: Path = RAW_DATA_DIR) -> Path:
    """Persist raw API payload to a timestamped JSON file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Le nom du fichier reste lisible et permet de retrouver facilement la ville et l'heure.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_city = city.lower().replace(" ", "_")
    output_path = output_dir / f"weather_{safe_city}_{timestamp}.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)

    return output_path
