CREATE TABLE IF NOT EXISTS weather_measurements (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    observed_at TIMESTAMP NOT NULL,
    temperature_c NUMERIC(5, 2),
    humidity_percent NUMERIC(5, 2),
    wind_speed_kmh NUMERIC(6, 2),
    weather_code INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
