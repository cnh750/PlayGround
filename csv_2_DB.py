import os
import sqlite3
import csv
import shutil

# Get the database path from an environment variable
db_directory = os.getenv("GAME_OF_LIFE_DB")
if not db_directory:
    raise ValueError("Environment variable GAME_OF_LIFE_DB is not set.")

# Construct the full path to the database file
db_path = os.path.join(db_directory, "game_of_life.db")

# Function to import data from a .csv file into the database
def import_csv_to_db(csv_filename):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Open the .csv file
    with open(csv_filename, mode="r") as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row

        # Insert each row into the database
        for row in reader:
            # Skip metadata rows (rows with empty generation values)
            if row[4]:  # Check if the "Generation" column is not empty
                cursor.execute("""
                INSERT INTO generations (
                    run_id, grid_size, probability_of_life, total_generations,
                    generation, alive_cells, dead_cells, born_cells, died_cells,
                    stability_index, density
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, row)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print(f"Data from {csv_filename} has been imported into the database.")

    # Option 1: Delete the .csv file after processing
    # os.remove(csv_filename)
    # print(f"Deleted {csv_filename}")

    # Option 2: Move the .csv file to a new folder after processing
    processed_dir = os.path.join(os.path.dirname(csv_filename), "processed")
    os.makedirs(processed_dir, exist_ok=True)  # Create the "processed" folder if it doesn't exist
    shutil.move(csv_filename, os.path.join(processed_dir, os.path.basename(csv_filename)))
    print(f"Moved {csv_filename} to {processed_dir}")

# Function to process all .csv files in the directory
def process_all_csv_files(directory="."):
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            csv_path = os.path.join(directory, filename)
            import_csv_to_db(csv_path)

# Main function
if __name__ == "__main__":
    # Process all .csv files in the current directory
    process_all_csv_files()