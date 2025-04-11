from game_of_life_core import run_simulation, save_to_csv
from datetime import datetime
import os

def run_batch_simulations(num_runs=5, prob_of_life=0.1):
    """Run multiple simulations with consistent parameters."""
    for _ in range(num_runs):
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")  # Generate once per run
        data, _ = run_simulation(
            run_id=run_id,
            prob_of_life=prob_of_life  # Pass the probability parameter
        )
        csv_path = save_to_csv(data, run_id=run_id)
        print(f"Saved simulation to: {csv_path}")  # Feedback for user

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

if __name__ == "__main__":
    # Get user input for probability
    prob = get_prob_of_life()
    num = get_num_runs()
    
    # Run simulation with user-specified probability
    print(f"\nRunning simulation with probability of life: {prob}")
    run_batch_simulations(num_runs=num, prob_of_life=prob)