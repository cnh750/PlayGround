import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Grid size
rows, cols = 100, 150

# Initialize the grid with random states
grid = np.random.choice([0, 1], size=(rows, cols), p=[0.90, 0.10])

# Function to update the grid for each generation
def update(frame_num, img, grid, rows, cols, text):
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

# Create the animation
ani = animation.FuncAnimation(
    fig, update, fargs=(img, grid, rows, cols, text), frames=1000, interval=50, save_count=50
)

# Display the animation
plt.show()