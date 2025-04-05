from game_of_life_core import run_simulation, save_to_csv
import os

def run_multiple_simulations(num_runs=10, prob_of_life=0.1, generations=1000):
    """Run multiple simulations and save each to a CSV."""
    for run in range(num_runs):
        print(f"Running simulation {run + 1}/{num_runs}...")
        data = run_simulation(prob_of_life=prob_of_life, generations=generations)
        csv_path = save_to_csv(data)
        print(f"Saved data to {csv_path}")

if __name__ == "__main__":
    # Run 10 simulations at 10% probability
    run_multiple_simulations(num_runs=10, prob_of_life=0.1)