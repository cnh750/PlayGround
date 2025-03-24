# Game of Life Database Setup

This guide explains how to create the SQLite database for the Game of Life project in a custom location using an environment variable.

---

## Prerequisites

- Python 3.x
- `sqlite3` module (included with Python)

---

## Steps to Create the Database

### 1. Set the Environment Variable

Set the `GAME_OF_LIFE_DB` environment variable to specify the directory where the database should be created.

#### On Windows:
1. Open the Start Menu and search for "Environment Variables."
2. Click on **Edit the system environment variables**.
3. In the System Properties window, click on the **Environment Variables** button.
4. Under **User variables** or **System variables**, click **New**.
5. Set the variable name to `GAME_OF_LIFE_DB` and the value to the desired directory (e.g., `C:\Users\YourName\Documents\GameOfLife`).
6. Click **OK** to save the changes.

#### On macOS/Linux:
1. Open a terminal.
2. Add the environment variable to your shell configuration file (e.g., `.bashrc`, `.zshrc`, or `.bash_profile`):
   ```bash
   export GAME_OF_LIFE_DB="/path/to/your/directory"