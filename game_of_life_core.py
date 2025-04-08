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

def run_simulation(rows=100, cols=150, prob_of_life=0.1, generations=1000, 
                  log_interval=100, run_id=None):
    """
    Run the Game of Life simulation.
    
    Args:
        run_id: If None, will generate a new one. Pass this to maintain consistency
                across multiple saves/exports.
    """
    # Generate run_id if not provided
    run_id = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
    
    grid = initialize_grid(rows, cols, prob_of_life)
    previous_grid = np.copy(grid)
    data = []
    # Generate run_id if not provided
    run_id = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for gen in range(generations + 1):
        if gen % log_interval == 0:
            alive_cells = np.sum(grid)
            dead_cells = grid.size - alive_cells
            born_cells = np.sum((previous_grid == 0) & (grid == 1))
            died_cells = np.sum((previous_grid == 1) & (grid == 0))
            stability_index = np.sum(grid != previous_grid) / grid.size
            density = (alive_cells / grid.size) * 100
            
            data.append({
                'run_id': run_id,
                'grid_size': f"{rows}x{cols}",
                'probability_of_life': prob_of_life,
                'total_generations': generations,
                'generation': gen,
                'alive_cells': alive_cells,
                'dead_cells': dead_cells,
                'born_cells': born_cells,
                'died_cells': died_cells,
                'stability_index': stability_index,
                'density': density
            })
        
        
        previous_grid = np.copy(grid)
        grid = update_grid(grid)
    
    return data, run_id  # Return both data and ID 

def save_to_csv(data, filename_prefix="game_of_life", run_id=None):
    """Save simulation data to CSV using consistent run_id in filename."""
    run_id = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{run_id}.csv"  # Use the same ID
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    return filename