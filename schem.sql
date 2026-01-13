CREATE TABLE IF NOT EXISTS areas (
    code TEXT PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_code TEXT,
    target_date TEXT,
    weather_text TEXT,
    get_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (area_code) REFERENCES areas(code)
);