import os
import sqlite3

# Get the database path from an environment variable
db_directory = os.getenv("GAME_OF_LIFE_DB")
if not db_directory:
    raise ValueError("Environment variable GAME_OF_LIFE_DB is not set.")

# Construct the full path to the database file
db_path = os.path.join(db_directory, "game_of_life.db")

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a table to store the data
cursor.execute("""
CREATE TABLE IF NOT EXISTS generations (
    run_id TEXT,
    grid_size TEXT,
    probability_of_life REAL,
    total_generations INTEGER,
    generation INTEGER,
    alive_cells INTEGER,
    dead_cells INTEGER,
    born_cells INTEGER,
    died_cells INTEGER,
    stability_index REAL,
    density REAL
)
""")

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"Database created/updated at: {db_path}")