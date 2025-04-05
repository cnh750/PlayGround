import numpy as np
import csv
from datetime import datetime

def initialize_grid(rows, cols, prob_of_life):
    """Create a random grid with given probability of life."""
    return np.random.choice([0, 1], size=(rows, cols), p=[1-prob_of_life, prob_of_life])

def update_grid(grid):
    """Compute one generation of Game of Life."""
    rows, cols = grid.shape
    new_grid = grid.copy()
    for i in range(rows):
        for j in range(cols):
            neighbors = (
                grid[(i-1) % rows, (j-1) % cols] + grid[(i-1) % rows, j] +
                grid[(i-1) % rows, (j+1) % cols] + grid[i, (j-1) % cols] +
                grid[i, (j+1) % cols] + grid[(i+1) % rows, (j-1) % cols] +
                grid[(i+1) % rows, j] + grid[(i+1) % rows, (j+1) % cols]
            )
            if grid[i, j] == 1:
                new_grid[i, j] = 1 if neighbors in [2, 3] else 0
            else:
                new_grid[i, j] = 1 if neighbors == 3 else 0
    return new_grid

def run_simulation(rows=100, cols=150, prob_of_life=0.1, generations=1000, log_interval=100):
    """
    Run the Game of Life without visualization.
    Returns a list of dictionaries with simulation data.
    """
    grid = initialize_grid(rows, cols, prob_of_life)
    data = []
    
    for gen in range(generations + 1):
        if gen % log_interval == 0:
            alive_cells = np.sum(grid)
            density = (alive_cells / grid.size) * 100
            data.append({
                'generation': gen,
                'alive_cells': alive_cells,
                'density': density,
                'grid_size': f"{rows}x{cols}",
                'probability_of_life': prob_of_life
            })
        grid = update_grid(grid)
    
    return data

def save_to_csv(data, filename_prefix="game_of_life"):
    """Save simulation data to a CSV file."""
    filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return filename