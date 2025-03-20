# Data to Include in the .csv File

## 1. Metadata (Static for Each Run)
- **Grid Size**: The dimensions of the grid (e.g., `rows` and `cols`).
- **Probability of Life**: The initial probability of a cell being alive (e.g., `p=[0.10, 0.90]`).
- **Run ID**: A unique identifier for each run (e.g., a timestamp or UUID).
- **Total Generations**: The total number of generations simulated (e.g., `1750`).

## 2. Generational Data (Dynamic for Each Generation)
- **Generation Number**: The current generation (e.g., `0`, `100`, `200`, etc.).
- **Alive Cells**: The number of alive cells in the grid.
  - Calculated as: `alive_cells = np.sum(grid)`
- **Dead Cells**: The number of dead cells in the grid.
  - Calculated as: `dead_cells = grid.size - alive_cells`
- **Born Cells**: The number of cells that changed from dead to alive.
  - Calculated as: `born_cells = np.sum((previous_grid == 0) & (grid == 1))`
- **Died Cells**: The number of cells that changed from alive to dead.
  - Calculated as: `died_cells = np.sum((previous_grid == 1) & (grid == 0))`
- **Stability Index**: The proportion of cells that changed state.
  - Calculated as: `stability_index = np.sum(grid != previous_grid) / grid.size`
- **Density**: The proportion of alive cells in the grid.
  - Calculated as: `density = (alive_cells / grid.size) * 100`

## 3. Additional Data (Optional)
- **Initial Alive Cells**: The number of alive cells at the start of the simulation.
- **Initial Dead Cells**: The number of dead cells at the start of the simulation.
- **Final Alive Cells**: The number of alive cells at the end of the simulation.
- **Final Dead Cells**: The number of dead cells at the end of the simulation.
- **Start Time**: The timestamp when the simulation started.
- **End Time**: The timestamp when the simulation ended.
- **Duration**: The total time taken to run the simulation.
- **Still Lifes**: The number of still lifes detected in the final grid.
- **Oscillators**: The number of oscillators detected in the final grid.
- **Spaceships**: The number of spaceships detected in the final grid.

---

# Structure of the .csv File

The .csv file will have the following columns:

| Run ID       | Grid Size | Probability of Life | Total Generations | Generation | Alive Cells | Dead Cells | Born Cells | Died Cells | Stability Index | Density |
|--------------|-----------|---------------------|-------------------|------------|-------------|------------|------------|------------|-----------------|---------|
| 20231025_1234| 100x150   | 0.10                | 1750              | 0          | 1500        | 13500      | 0          | 0          | 0.00            | 10.00   |
| 20231025_1234| 100x150   | 0.10                | 1750              | 100        | 780         | 14220      | 50         | 30         | 0.05            | 5.20    |
| 20231025_1234| 100x150   | 0.10                | 1750              | 200        | 542         | 14458      | 40         | 25         | 0.03            | 3.61    |

---

# Example Workflow

1. **At the Start of the Simulation**:
   - Create a .csv file and write the metadata (e.g., grid size, probability of life, run ID).

2. **During the Simulation**:
   - Every 100 generations, append a row to the .csv file with the generational data.

3. **At the End of the Simulation**:
   - Write final conditions (e.g., final alive cells, final dead cells).
   - Close the .csv file.

---

# Next Steps

1. **Implement the .csv Logging**:
   - Update the Game of Life script to log data to a .csv file.

2. **Design the Data Access Layer**:
   - Create a separate script to read the .csv file and import the data into the SQL database.

3. **Query and Analyze the Data**:
   - Use SQL queries to analyze the data (e.g., compare runs with different probabilities of life).

4. **Visualize the Data**:
   - Use libraries like `matplotlib` or `seaborn` to create plots of the data.