from game_of_life_core import run_simulation, save_to_csv, get_prob_of_life, get_num_runs
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
    
if __name__ == "__main__":
    # Get user input for probability
    prob = get_prob_of_life()
    num = get_num_runs()
    
    # Run simulation with user-specified probability
    print(f"\nRunning simulation with probability of life: {prob}")
    run_batch_simulations(num_runs=num, prob_of_life=prob)