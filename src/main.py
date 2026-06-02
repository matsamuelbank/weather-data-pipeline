from db import get_engine, read_sql_query
from extract import fetch_weather_data, save_raw_data
from load import load_to_postgres
from transform import save_processed_data, transform_weather_data


def main() -> None:
    # On commence simple avec une seule ville pour bien voir chaque etape.
    city = "Dijon"
    latitude = 47.322
    longitude = 5.0415

    print(f"Extraction des donnees meteo pour {city}...")
    raw_data = fetch_weather_data(latitude, longitude)

    print("Sauvegarde du JSON brut...")
    output_path = save_raw_data(raw_data, city)

    # Ces impressions servent surtout a comprendre la structure du JSON avant Pandas.
    print(f"Fichier cree: {output_path}")
    print(f"Cles racine: {list(raw_data.keys())}")
    print(f"Cles hourly: {list(raw_data['hourly'].keys())}")
    print(f"Nombre de mesures horaires: {len(raw_data['hourly']['time'])}")

    print("Transformation avec Pandas...")
    dataframe = transform_weather_data(raw_data, city)

    # On exporte un CSV pour pouvoir verifier visuellement les donnees nettoyees.
    processed_path = save_processed_data(dataframe, city)

    print("Apercu du DataFrame transforme:")
    print(dataframe.head())
    print(f"CSV cree: {processed_path}")

    print("Connexion a PostgreSQL...")
    engine = get_engine()

    print("Chargement en base...")
    inserted_rows = load_to_postgres(dataframe, engine, "weather_measurements")
    print(f"{inserted_rows} ligne(s) inseree(s) dans weather_measurements.")

    analysis_query = """
    SELECT
        city,
        ROUND(AVG(temperature_c), 2) AS avg_temperature_c
    FROM weather_measurements
    GROUP BY city
    ORDER BY city;
    """

    print("Petit apercu SQL depuis Python:")
    analysis_df = read_sql_query(analysis_query, engine)
    print(analysis_df)


if __name__ == "__main__":
    main()
