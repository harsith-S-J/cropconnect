DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS crops;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    location TEXT NOT NULL,
    contact TEXT NOT NULL
);

CREATE TABLE crops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    crop_name TEXT NOT NULL,
    planted_date DATE,
    area_size TEXT,
    protection_strategy TEXT NOT NULL,
    status TEXT NOT NULL,
    quantity_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
