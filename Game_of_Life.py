import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
from datetime import datetime
from game_of_life_core import get_prob_of_life

# Probability of life
probability_of_life = get_prob_of_life()

# Grid size
rows, cols = 100, 150

# Initialize the grid with random states
grid = np.random.choice([0, 1], size=(rows, cols), p=[1 - probability_of_life, probability_of_life])

# Create a unique Run ID (e.g., timestamp)
run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# Total generations to simulate
total_generations = 1750

# Open a .csv file to save the data
csv_filename = f"game_of_life_{run_id}.csv"
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow([
        "Run ID", "Grid Size", "Probability of Life", "Total Generations",
        "Generation", "Alive Cells", "Dead Cells", "Born Cells", "Died Cells",
        "Stability Index", "Density"
    ])
    
    # Write metadata (static for the entire run)
    writer.writerow([
        run_id, f"{rows}x{cols}", probability_of_life, total_generations,
        "", "", "", "", "", "", ""
    ])

    # Function to update the grid for each generation
    def update(frame_num, img, grid, rows, cols, text):
        global previous_grid  # Store the previous grid for calculations

        # Stop the animation after total_generations
        if frame_num >= total_generations:
            ani.event_source.stop()  # Stop the animation
            
            # Write final conditions to the .csv file
            alive_cells = np.sum(grid)
            dead_cells = grid.size - alive_cells
            writer.writerow([
                run_id, f"{rows}x{cols}", probability_of_life, total_generations,
                frame_num, alive_cells, dead_cells, "", "", "", ""
            ])
            return img, text

        # Log statistics every 100 generations (skip initialization call)
        if frame_num % 100 == 0 and frame_num != 0:  # Skip frame_num = 0
            alive_cells = np.sum(grid)  # Count alive cells (1s)
            dead_cells = grid.size - alive_cells  # Count dead cells (0s)

            # Calculate born and died cells
            born_cells = np.sum((previous_grid == 0) & (grid == 1))  # Dead -> Alive
            died_cells = np.sum((previous_grid == 1) & (grid == 0))  # Alive -> Dead

            # Calculate stability index
            stability_index = np.sum(grid != previous_grid) / grid.size

            # Calculate density of alive cells
            density = (alive_cells / grid.size) * 100

            # Print statistics
            print(
                f"Generation {frame_num}: "
                f"Alive = {alive_cells}, Dead = {dead_cells}, "
                f"Born = {born_cells}, Died = {died_cells}, "
                f"Stability = {stability_index:.2f}, Density = {density:.2f}%"
            )

            # Write generational data to the .csv file
            writer.writerow([
                run_id, f"{rows}x{cols}", probability_of_life, total_generations,
                frame_num, alive_cells, dead_cells, born_cells, died_cells,
                stability_index, density
            ])

        # Update the previous grid
        previous_grid = grid.copy()

        new_grid = grid.copy()
        for i in range(rows):
            for j in range(cols):
                # Count the number of live neighbors
                neighbors = (
                    grid[(i - 1) % rows, (j - 1) % cols]
                    + grid[(i - 1) % rows, j]
                    + grid[(i - 1) % rows, (j + 1) % cols]
                    + grid[i, (j - 1) % cols]
                    + grid[i, (j + 1) % cols]
                    + grid[(i + 1) % rows, (j - 1) % cols]
                    + grid[(i + 1) % rows, j]
                    + grid[(i + 1) % rows, (j + 1) % cols]
                )
                # Apply the rules of the Game of Life
                if grid[i, j] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[i, j] = 0
                else:
                    if neighbors == 3:
                        new_grid[i, j] = 1
        img.set_data(new_grid)
        grid[:] = new_grid[:]

        # Update the generation number
        text.set_text(f"Generation: {frame_num}")
        return img, text

    # Set up the animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation="nearest", cmap="binary")

    # Add a text annotation for the generation number
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes, color="red", fontsize=12)

    # Initialize the previous grid
    previous_grid = grid.copy()

    # Create the animation
    ani = animation.FuncAnimation(
        fig, update, fargs=(img, grid, rows, cols, text), frames=total_generations, interval=50, repeat=False
    )

    # Display the animation
    plt.show()