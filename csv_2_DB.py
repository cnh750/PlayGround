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
def import_csv_to_db(csv_path):
    """Import CSV data to SQLite database with proper error handling."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Skip header row
        
        for row in reader:
            try:
                # Validate row has enough columns
                if len(row) < 11:  # Your schema requires 11 columns
                    print(f"Skipping incomplete row: {row}")
                    continue
                    
                # Convert empty strings to None for database
                processed_row = [
                    value if value.strip() else None 
                    for value in row
                ]
                
                cursor.execute("""
                    INSERT INTO generations 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, processed_row)
                
            except Exception as e:
                print(f"Error processing row {row}: {str(e)}")
                continue
    
    conn.commit()
    conn.close()
    print(f"Successfully imported {csv_path}")

    # Option 1: Delete the .csv file after processing
    # os.remove(csv_filename)
    # print(f"Deleted {csv_filename}")

    # Option 2: Move the .csv file to a new folder after processing
    processed_dir = os.path.join(os.path.dirname(csv_path), "processed")
    os.makedirs(processed_dir, exist_ok=True)  # Create the "processed" folder if it doesn't exist
    shutil.move(csv_path, os.path.join(processed_dir, os.path.basename(csv_path)))
    print(f"Moved {csv_path} to {processed_dir}")

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