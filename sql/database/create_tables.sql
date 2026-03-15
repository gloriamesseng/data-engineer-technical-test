CREATE TABLE IF NOT EXISTS earthquakes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude REAL,
    longitude REAL,
    magnitude REAL,
    date TEXT
);
CREATE TABLE IF NOT EXISTS locations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    latitude REAL,
    longitude REAL,
    value REAL
);
CREATE TABLE IF NOT EXISTS losses(
    earthquake_id INTEGER,
    location_id INTEGER,
    net_loss REAL,
    FOREIGN KEY(earthquake_id) REFERENCES earthquakes(id),
    FOREIGN KEY(location_id) REFERENCES locations(id),
    PRIMARY KEY (earthquake_id, location_id)
);