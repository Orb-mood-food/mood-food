-- Delete tables if they exist to start fresh
DROP TABLE IF EXISTS foods;
DROP TABLE IF EXISTS moods;

-- Create a table for moods
CREATE TABLE moods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    emoji TEXT NOT NULL
);

-- Create a table for foods with a link to the moods table
CREATE TABLE foods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    imageUrl TEXT NOT NULL,
    mood_id INTEGER NOT NULL,
    FOREIGN KEY (mood_id) REFERENCES moods (id) ON DELETE CASCADE
);