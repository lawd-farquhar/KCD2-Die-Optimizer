# KCD2 Dice Optimizer (Farkle)

This tool helps you optimize your dice selection in the game of Farkle in Kingdom Come: Deliverance (KCD). It calculates the expected value (EV) of different dice combinations and recommends the best 6-die combination based on your available dice. It also identifies the most likely roll, the highest-scoring possible roll, and more.

## Features

*   **Dice Selection:** Choose from a comprehensive list of Farkle dice with varying probabilities gathered from u/Nigi_1 on Reddit via [https://www.reddit.com/r/kingdomcome/comments/1ijaac0/kcd2_dice_weight_table/](https://www.reddit.com/r/kingdomcome/comments/1ijaac0/kcd2_dice_weight_table/). You can specify the *quantity* of each die type you have.
*   **Optimal Combination Recommendation:** The program uses a heuristic search to quickly find a near-optimal 6-dice combination, aiming to maximize expected value (EV). It's significantly faster than a brute-force search and provides excellent results.
*   **Detailed Statistics:** For the recommended combination, the program displays:
    *   Expected Value (EV)
    *   Most Likely Roll(s) and their probability
    *   Highest Scoring Roll and its probability
    *   Probability of rolling at least one 1 or 5 (scoring probability)
    *   Comparison of the selected combination's EV to the average EV:
        *   **Green:** Your combination's EV is above average.
        *   **Red:** Your combination's EV is below average.
        *   **Black:** Your combination's EV is exactly average.
*   **User-Friendly GUI:** A graphical interface makes it easy to select dice and view results.
*   **Handles Duplicates:** Correctly handles duplicate dice. "Standard Die" allows duplicates; others prompt for quantity.
*   **Average EV Benchmarks:**
    *   Average EV with Duplicates: **584.39**
    *   Average EV without Duplicates (except Standard): **576.86**
*   **Progress Indicator:** A progress bar and status messages show the optimization process.
*   **Persistent Selections:** Dice selections and quantities are saved between sessions.
*   **Error Handling:** Handles potential errors gracefully, displaying informative messages.

## Installation

**For ease of use, it's recommended to download the pre-built executable:**

1.  **Download the Executable:** Go to the [Releases](https://github.com/lawd-farquhar/KCD2-Die-Optimizer/releases) section of this GitHub repository.  Download the latest `.exe` file (e.g., `KCD2-Die-Optimizer.exe`).  No other files are needed.  This is a standalone executable.

**Alternatively, to run from source code (requires Python):**

1.  **Prerequisites:** You need Python 3 installed. The script uses `tkinter`, which is usually included with Python.  If missing, install it separately.
2.  **Clone the Repository:**

    ```bash
    git clone https://github.com/lawd-farquhar/KCD2-Die-Optimizer
    cd KCD2-Die-Optimizer
    ```

    Or download the ZIP file and extract it.

3.  **No Dependencies to Install:** The necessary libraries are part of base Python.

## Usage

1.  **Run the Program:**
    *   **Executable:** Double-click the downloaded `.exe` file.
    *   **Source Code:** Execute the `KCD2-Die-Optimizer.py` script.
2.  **Select Dice:** Check the boxes next to the dice you have.
3.  **Enter Quantities:** When you select a die (other than "Standard Die"), enter the quantity (0-10) and click "OK".  Uncheck and re-check to re-enter.  You can also load previous selections.
4.  **Recommend Combination:** Click "Recommend Optimal Combination".
5.  **View Results:** The program will display the recommended combination (or a message if none is possible), along with detailed statistics. The calculation may take a few moments; a progress bar will show progress.
6.  **Load Previous:** Click 'Load Previous Dice' to load your previous selections.

## Changes from Previous Version

*   **Heuristic Optimization:** Uses a heuristic search instead of an exhaustive one, drastically improving performance.
*   **Progress Updates:** GUI includes a progress bar and status labels.
*   **Persistent Selections:** Saves selections to `kc2_die_selections.json`.
*   **Improved Error Handling:** More robust error handling and feedback.
*   **Refactored Code:** Reorganized and more modular.
*   **Adaptive Queue Checking:** Queue checking interval increases gradually.
*   **Standalone Executable**: The project is now easily accessible as a downloadable executable.

## Dice Probabilities

The `DICE_PROBABILITIES` dictionary in the code defines the probability distribution for each die.  Each entry is a list of six probabilities (for rolling 1, 2, 3, 4, 5, or 6). For example:

```python
DICE_PROBABILITIES = {
    "Ordinary die": [1/6, 1/6, 1/6, 1/6, 1/6, 1/6],
    "Weighted die": [0.667, 0.067, 0.067, 0.067, 0.067, 0.067],
    # ... other dice ...
}


