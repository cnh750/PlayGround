import matplotlib.pyplot as plt
import matplotlib.animation as animation
from game_of_life_core import initialize_grid, update_grid

def animate_run(rows=100, cols=150, prob_of_life=0.1, generations=1000):
    """Run the Game of Life with visualization."""
    grid = initialize_grid(rows, cols, prob_of_life)
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest', cmap='binary')
    
    def update(frame):
        nonlocal grid
        grid = update_grid(grid)
        img.set_array(grid)  # Update the image data
        return [img]  # Must return a sequence of Artists
    
    ani = animation.FuncAnimation(
        fig, 
        update, 
        frames=generations, 
        interval=50, 
        blit=True
    )
    plt.show()

if __name__ == "__main__":
    animate_run(prob_of_life=0.25)