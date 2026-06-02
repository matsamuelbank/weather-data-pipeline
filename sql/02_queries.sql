-- Nombre total de lignes chargees
SELECT COUNT(*) AS total_rows
FROM weather_measurements;

-- Dernieres mesures inserees
SELECT city, observed_at, temperature_c, humidity_percent, wind_speed_kmh
FROM weather_measurements
ORDER BY observed_at DESC
LIMIT 20;

-- Temperature moyenne par ville
SELECT
    city,
    ROUND(AVG(temperature_c), 2) AS avg_temperature_c
FROM weather_measurements
GROUP BY city
ORDER BY city;

-- Temperature maximale par jour
SELECT
    city,
    DATE(observed_at) AS weather_date,
    MAX(temperature_c) AS max_temperature_c
FROM weather_measurements
GROUP BY city, DATE(observed_at)
ORDER BY weather_date, city;

-- Vitesse du vent moyenne par jour
SELECT
    city,
    DATE(observed_at) AS weather_date,
    ROUND(AVG(wind_speed_kmh), 2) AS avg_wind_speed_kmh
FROM weather_measurements
GROUP BY city, DATE(observed_at)
ORDER BY weather_date, city;

-- Heures ou il fait plus de 25 degres
SELECT
    city,
    observed_at,
    temperature_c
FROM weather_measurements
WHERE temperature_c > 25
ORDER BY observed_at;
