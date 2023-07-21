CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    team_name VARCHAR(255),
    mustache_count INTEGER,
    telegram_id INTEGER,
    balance DECIMAL(10, 2)
);
