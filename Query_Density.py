import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import os


def get_db_connection():
    """Reusable database connection setup"""
    db_directory = os.getenv("GAME_OF_LIFE_DB")
    if not db_directory:
        raise ValueError("Environment variable GAME_OF_LIFE_DB is not set.")
    db_path = os.path.join(db_directory, "game_of_life.db")
    return sqlite3.connect(db_path)

def get_density_by_probability():
    """Returns a dictionary of {probability: [density_values]}"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get all probabilities in the database
        cursor.execute("SELECT DISTINCT probability_of_life FROM generations")
        probabilities = [row[0] for row in cursor.fetchall()]
        
        # Get densities grouped by probability
        density_groups = {}
        for prob in probabilities:
            cursor.execute(
                "SELECT density FROM generations WHERE probability_of_life = ? AND density IS NOT NULL",
                (prob,)
            )
            density_groups[prob] = [row[0] for row in cursor.fetchall()]
            
        return density_groups

def plot_comparison_histogram(density_groups):
    plt.figure(figsize=(12, 6))
    
    # Plot histograms for each probability group
    colors = ['skyblue', 'salmon', 'lightgreen']  # Different colors for each group
    for i, (prob, densities) in enumerate(density_groups.items()):
        plt.hist(
            densities,
            bins=20,
            alpha=0.6,
            color=colors[i % len(colors)],
            edgecolor='black',
            label=f'{int(prob*100)}% Initial Alive'
        )
    
    plt.title('Density Distribution by Initial Probability of Life')
    plt.xlabel('Density (%)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # Add mean markers
    for prob, densities in density_groups.items():
        plt.axvline(
            x=np.mean(densities),
            color=colors[list(density_groups.keys()).index(prob) % len(colors)],
            linestyle='--',
            linewidth=1
        )
    
    plt.tight_layout()
    plt.savefig('density_by_probability.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    density_groups = get_density_by_probability()
    plot_comparison_histogram(density_groups)