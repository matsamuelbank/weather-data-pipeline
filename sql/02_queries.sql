SELECT COUNT(*) AS total_rows
FROM weather_measurements;

SELECT city, observed_at, temperature_c, humidity_percent
FROM weather_measurements
ORDER BY observed_at DESC
LIMIT 20;
