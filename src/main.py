from extract import fetch_weather_data, save_raw_data


def main() -> None:
    city = "Dijon"
    latitude = 47.322
    longitude = 5.0415

    print(f"Extraction des donnees meteo pour {city}...")
    raw_data = fetch_weather_data(latitude, longitude)

    print("Sauvegarde du JSON brut...")
    output_path = save_raw_data(raw_data, city)

    print(f"Fichier cree: {output_path}")
    print(f"Cles racine: {list(raw_data.keys())}")
    print(f"Cles hourly: {list(raw_data['hourly'].keys())}")
    print(f"Nombre de mesures horaires: {len(raw_data['hourly']['time'])}")


if __name__ == "__main__":
    main()
