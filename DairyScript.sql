CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    registration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE diary_metadata (
    meta_id SERIAL PRIMARY KEY,
    entry_id INT REFERENCES diary_entries(entry_id),
    mood VARCHAR(50),
    tags TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE diary_entries (
    entry_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),  -- Foreign key linking to the user
    entry_date DATE NOT NULL,
    content TEXT,  -- This can be large text, like the diary entry
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
