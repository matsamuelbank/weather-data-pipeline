from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from db import get_engine, read_sql_query
from extract import fetch_weather_data, save_raw_data
from load import load_to_postgres
from transform import save_processed_data, transform_weather_data


st.set_page_config(
    page_title="Weather Data Pipeline",
    page_icon="🌦️",
    layout="wide",
)


CITIES = {
    "Dijon": {"latitude": 47.322, "longitude": 5.0415},
    "Paris": {"latitude": 48.8566, "longitude": 2.3522},
    "Lyon": {"latitude": 45.764, "longitude": 4.8357},
    "Marseille": {"latitude": 43.2965, "longitude": 5.3698},
    "Lille": {"latitude": 50.6292, "longitude": 3.0573},
}


def show_pipeline_summary(dataframe: pd.DataFrame) -> None:
    """Display a few quick indicators to make the pipeline easier to read."""
    if dataframe.empty:
        st.warning("Aucune ligne exploitable n'a ete produite apres la transformation.")
        return

    latest_row = dataframe.sort_values("observed_at").iloc[-1]

    metric_column_1, metric_column_2, metric_column_3 = st.columns(3)
    metric_column_1.metric("Temperature actuelle", f"{latest_row['temperature_c']:.1f} °C")
    metric_column_2.metric("Humidite actuelle", f"{latest_row['humidity_percent']:.0f} %")
    metric_column_3.metric("Vent actuel", f"{latest_row['wind_speed_kmh']:.1f} km/h")


def show_database_preview() -> None:
    """Try to read a few rows from PostgreSQL if the database is available."""
    try:
        engine = get_engine()

        recent_query = """
        SELECT city, observed_at, temperature_c, humidity_percent, wind_speed_kmh
        FROM weather_measurements
        ORDER BY observed_at DESC
        LIMIT 20;
        """
        averages_query = """
        SELECT
            city,
            ROUND(AVG(temperature_c), 2) AS avg_temperature_c
        FROM weather_measurements
        GROUP BY city
        ORDER BY city;
        """

        recent_df = read_sql_query(recent_query, engine)
        averages_df = read_sql_query(averages_query, engine)

        st.subheader("Apercu PostgreSQL")
        st.dataframe(recent_df, width="stretch")
        st.subheader("Temperature moyenne par ville")
        st.dataframe(averages_df, width="stretch")
    except Exception as error:
        st.info(
            "Connexion PostgreSQL non disponible pour le moment. "
            "Lancer Docker et verifier le fichier .env pour activer cette partie."
        )
        st.caption(f"Detail technique : {error}")


st.title("Weather Data Pipeline")
st.caption("Mini-interface Streamlit pour visualiser le pipeline ETL meteo.")

st.sidebar.header("Parametres")
selected_city = st.sidebar.selectbox("Ville", list(CITIES.keys()))
load_into_database = st.sidebar.checkbox("Charger aussi dans PostgreSQL", value=False)
show_database_data = st.sidebar.checkbox("Afficher les donnees de PostgreSQL", value=True)

city_config = CITIES[selected_city]

st.markdown(
    """
    Cette interface permet de :
    - recuperer les donnees meteo depuis Open-Meteo
    - transformer les donnees avec Pandas
    - sauvegarder les fichiers `raw` et `processed`
    - charger les donnees dans PostgreSQL si besoin
    """
)

if st.button("Lancer le pipeline", type="primary"):
    try:
        with st.spinner("Extraction des donnees meteo en cours..."):
            raw_data = fetch_weather_data(
                city_config["latitude"],
                city_config["longitude"],
            )

        raw_path = save_raw_data(raw_data, selected_city)
        dataframe = transform_weather_data(raw_data, selected_city)
        processed_path = save_processed_data(dataframe, selected_city)

        st.success("Pipeline execute avec succes.")
        show_pipeline_summary(dataframe)

        chart_column, data_column = st.columns([2, 3])

        with chart_column:
            st.subheader("Evolution de la temperature")
            temperature_chart_df = dataframe[["observed_at", "temperature_c"]].set_index("observed_at")
            st.line_chart(temperature_chart_df)

        with data_column:
            st.subheader("Apercu du DataFrame transforme")
            st.dataframe(dataframe.head(20), width="stretch")

        st.subheader("Fichiers generes")
        st.write(f"JSON brut: `{raw_path}`")
        st.write(f"CSV transforme: `{processed_path}`")
        st.write(f"Nombre de lignes Pandas: `{len(dataframe)}`")

        if load_into_database:
            with st.spinner("Chargement dans PostgreSQL..."):
                engine = get_engine()
                inserted_rows = load_to_postgres(dataframe, engine, "weather_measurements")
            st.success(f"{inserted_rows} ligne(s) inseree(s) dans PostgreSQL.")

    except Exception as error:
        st.error("Le pipeline a rencontre une erreur.")
        st.code(str(error))

if show_database_data:
    show_database_preview()
