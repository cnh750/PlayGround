import matplotlib.pyplot as plt
import matplotlib.animation as animation
from game_of_life_core import initialize_grid, update_grid

def animate_run(rows=100, cols=150, prob_of_life=0.1, generations=1000):
    """Run the Game of Life with visualization and generation counter."""
    grid = initialize_grid(rows, cols, prob_of_life)
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest', cmap='binary')
    
    # Add generation counter text
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes, 
                  color='red', fontsize=12, 
                  bbox=dict(facecolor='white', alpha=0.7))
    
    def update(frame):
        nonlocal grid
        grid = update_grid(grid)
        img.set_array(grid)
        text.set_text(f"Generation: {frame}")
        return [img, text]  # Return both Artists for blitting
    
    ani = animation.FuncAnimation(
        fig, 
        update, 
        frames=generations, 
        interval=50, 
        blit=True, 
        repeat=False  # Stop after reaching 'generations'
    )
    plt.show()

if __name__ == "__main__":
    animate_run(prob_of_life=0.25, generations=500)  # Example: 500 generations