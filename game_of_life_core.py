import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
from datetime import datetime

def visualize_simulation(initial_grid, generations=1000, interval=100, writer=None, run_id=None):
    """Run and visualize the Game of Life simulation.
    
    Args:
        initial_grid (np.ndarray): Starting grid (1=alive, 0=dead)
        generations (int): Total generations to simulate
        interval (int): Milliseconds between frames
        run_id (str): Optional unique identifier
        
    Returns:
        matplotlib.animation.FuncAnimation
    """
    fig, ax = plt.subplots()
    img = ax.imshow(initial_grid, interpolation='nearest', cmap='binary')
    text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='red')
    grid = initial_grid.copy()
    previous_grid = initial_grid.copy()
    
    def update_frame(frame_num, img, grid, text):
        nonlocal previous_grid
        
        # Stop condition
        if frame_num >= generations:
            plt.close(fig)
            return img, text
        
        # Update the grid using the core function
        new_grid = update_grid(grid)
        
        # Visualization update
        img.set_array(new_grid)
        
        # Update stats every 100 gens (skipping generation 0)
        if frame_num % 100 == 0 and frame_num != 0:
            alive = np.sum(new_grid)
            dead = new_grid.size - alive
            born = np.sum((previous_grid == 0) & (new_grid == 1))
            died = np.sum((previous_grid == 1) & (new_grid == 0))
            stability = np.sum(new_grid != previous_grid) / new_grid.size
            density = (alive / new_grid.size) * 100
            
            # Update display text
            stats_text = (
                f'Gen: {frame_num}')
            text.set_text(stats_text)
            
            # Print to console (optional)
            print(f"Generation {frame_num}: Alive={alive} | Dead={dead}| Born={born} | Died={died} | stability ={stability} | density={density}")
            writer.writerow([
                "", "", "", "",  # skip repeating run_id, grid size, etc.
                frame_num,
                alive,
                dead,
                born,
                died,
                stability,
                density
                ])
        
        # Maintain state for next frame
        previous_grid[:] = grid
        grid[:] = new_grid
        return img, text
    
    ani = animation.FuncAnimation(
        fig, 
        update_frame, 
        fargs=(img, grid, text),
        frames=generations + 1,
        interval=interval,
        blit=True,
        repeat=False
    )
    plt.show()
    return ani


def init_logging(run_id, rows, cols, prob_of_life, generations, filename=None):
    """Initialize CSV logging for a simulation run.
    
    Args:
        run_id (str): Unique run identifier
        rows, cols (int): Grid dimensions
        prob_of_life (float): Initial probability
        generations (int): Total generations
        filename (str): Optional custom filename
        
    Returns:
        tuple: (csv.writer, file_handle) for writing data
    """
    if filename is None:
        filename = f"game_of_life_{run_id}.csv"
    
    file = open(filename, mode="w", newline="")
    writer = csv.writer(file)
    
    # Write header
    writer.writerow([
        "Run ID", "Grid Size", "Probability of Life", "Total Generations",
        "Generation", "Alive Cells", "Dead Cells", "Born Cells", "Died Cells",
        "Stability Index", "Density"
    ])
    
    # Write metadata
    writer.writerow([
        run_id, f"{rows}x{cols}", prob_of_life, generations,
        "", "", "", "", "", "", ""
    ])
    
    return writer, file

def log_generation_stats(writer, generation, alive, dead, born, died, stability, density):
    """Write per-generation stats to the CSV log created for the visualization script."""
    writer.writerow([
        "", "", "", "",  # Leave metadata columns empty
        generation,
        alive,
        dead,
        born,
        died,
        stability,
        density
    ])

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

def get_prob_of_life():
    """Prompt user for probability of life value with validation."""
    while True:
        try:
            user_input = input("Enter probability of life (0.0 to 1.0, default 0.1): ")
            if not user_input.strip():  # If user just presses Enter
                return 0.1  # Return default value
            prob = float(user_input)
            if 0.0 <= prob <= 1.0:
                return prob
            print("Error: Probability must be between 0.0 and 1.0")
        except ValueError:
            print("Error: Please enter a valid number")

def get_num_runs():
    """Prompt for getting number of simulations run in this batch
    Returns int: Number of runs (default 5, max 30)"""
    while True:
        try:
            user_input = input("Enter the number of runs for this batch (Default = 5): ") 
            if not user_input.strip():
                return 5 # default value
            num = int(user_input)
            if 0 < num < 31:
                return num
            print("Error: please pick a number between 1 and 30")
        except ValueError:
            print("Error:Please enter a valid number")