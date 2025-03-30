import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import os

def get_density_data():
    """Query density values from the database"""
    db_directory = os.getenv("GAME_OF_LIFE_DB")
    if not db_directory:
        raise ValueError("Environment variable GAME_OF_LIFE_DB is not set.")
    db_path = os.path.join(db_directory, "game_of_life.db")

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Get all density values
        cursor.execute("SELECT density FROM generations WHERE density IS NOT NULL")
        density_values = [row[0] for row in cursor.fetchall()]
        
        # Get sample data for plot title
        cursor.execute("""
            SELECT alive_cells, grid_size 
            FROM generations 
            WHERE density IS NOT NULL 
            LIMIT 1
        """)
        sample = cursor.fetchone()
        
    return density_values, sample

def plot_density_histogram(density_values, sample):
    """Create and display density histogram"""
    if not density_values:
        print("No density data found in the database!")
        return
    
    # Calculate grid size for title
    alive_cells, grid_size = sample if sample else (0, "100x100")
    grid_width, grid_height = map(int, grid_size.split('x'))
    total_cells = grid_width * grid_height
    
    plt.figure(figsize=(10, 6))
    plt.hist(density_values, bins=20, color='skyblue', 
             edgecolor='black', alpha=0.7)
    
    title = (f'Distribution of Cell Density (Alive Cells/Total Cells)\n'
             f'Sample: {alive_cells}/{total_cells} = {density_values[0]:.2f}%')
    plt.title(title)
    plt.xlabel('Density (%)')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.75)
    
    # Add statistical markers
    mean_density = np.mean(density_values)
    median_density = np.median(density_values)
    plt.axvline(mean_density, color='red', linestyle='dashed', 
                linewidth=1, label=f'Mean: {mean_density:.2f}%')
    plt.axvline(median_density, color='green', linestyle='dashed', 
                linewidth=1, label=f'Median: {median_density:.2f}%')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('density_histogram.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    density_values, sample = get_density_data()
    plot_density_histogram(density_values, sample)