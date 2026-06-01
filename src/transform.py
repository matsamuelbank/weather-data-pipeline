from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from config import PROCESSED_DATA_DIR


def transform_weather_data(data: dict, city: str) -> pd.DataFrame:
    """Convert the raw API payload into a clean tabular dataset."""
    hourly = data["hourly"]

    # On construit un DataFrame simple avec uniquement les colonnes utiles pour l'analyse.
    dataframe = pd.DataFrame(
        {
            "time": hourly["time"],
            "temperature": hourly["temperature_2m"],
            "humidity": hourly["relative_humidity_2m"],
            "wind_speed": hourly["wind_speed_10m"],
        }
    )

    # La conversion en datetime sera indispensable pour les filtres et les aggregations plus tard.
    dataframe["time"] = pd.to_datetime(dataframe["time"])
    dataframe["city"] = city

    # Pour ce premier pipeline, on prefere enlever les lignes incompletes plutot que les garder.
    dataframe = dataframe.dropna().reset_index(drop=True)

    return dataframe


def save_processed_data(
    dataframe: pd.DataFrame,
    city: str,
    output_dir: Path = PROCESSED_DATA_DIR,
) -> Path:
    """Export the cleaned dataframe to CSV for manual inspection."""
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_city = city.lower().replace(" ", "_")
    output_path = output_dir / f"weather_{safe_city}_{timestamp}.csv"

    dataframe.to_csv(output_path, index=False)
    return output_path
