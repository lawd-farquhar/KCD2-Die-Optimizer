# KCD2 Dice Optimizer (Farkle)

This Python script helps you optimize your dice selection in the game of Farkle in KCD2. It calculates the expected value (EV) of different dice combinations and recommends the optimal 6-die combination based on your available dice. It also identifies the most likely roll and the highest-scoring possible roll for a given combination.

## Features

*   **Dice Selection:** Choose from a comprehensive list of Farkle dice with varying probabilities gathered from u/Nigi_1 on Reddit via [https://www.reddit.com/r/kingdomcome/comments/1ijaac0/kcd2_dice_weight_table/](https://www.reddit.com/r/kingdomcome/comments/1ijaac0/kcd2_dice_weight_table/). You can specify the *quantity* of each die type you have.
*   **Optimal Combination Recommendation:** The program uses a heuristic search to quickly find a near-optimal 6-dice combination from your selected dice, aiming to maximize the expected value (EV).  It's not guaranteed to be *perfectly* optimal in all cases, but it's significantly faster than a brute-force search and provides excellent results.
*   **Detailed Statistics:** For the recommended combination, the program displays:
    *   Expected Value (EV)
    *   Most Likely Roll(s) and their probability
    *   Highest Scoring Roll and its probability
    *   Probability of rolling at least one 1 or 5 (scoring probability)
    *   Comparison of the selected combination's EV to the average EV of all dice combinations (with and without duplicates, as appropriate), displayed in:
        *   **Green:** Your combination's EV is above average.
        *   **Red:** Your combination's EV is below average.
        *   **Black:** Your combination's EV is exactly average.
*   **User-Friendly GUI:** A graphical interface (built with Tkinter) makes it easy to select dice and view results.
*   **Handles Duplicates:** The program correctly handles duplicate dice selections.  The "Standard Die" is allowed to have duplicates; any other dice will prompt the user for the quantity.
*   **Average EV Benchmarks:** The comparison uses the following benchmarks:
    *   Average EV with Duplicates: 584.39
    *   Average EV without Duplicates (except Standard): 576.86
*   **Progress Indicator:**  A progress bar and status messages show the progress of the optimization process.
*   **Persistent Selections:** Your dice selections and quantities are saved between sessions.
*   **Error Handling:** The program handles potential errors gracefully, displaying informative messages within the GUI.



## Installation

1.  **Prerequisites:** You need Python 3 installed on your system.  The script uses the `tkinter` library, which is usually included with standard Python installations. If you're missing it, you may separately install `tkinter`.
2.  **Clone the Repository:**

    ```bash
    git clone https://github.com/lawd-farquhar/KCD2-Die-Optimizer
    cd KCD2-Die-Optimizer
    ```

    Alternatively, you can download the script directly as a ZIP file and extract it.
3.  **No Dependencies to Install:** The necessary libraries should be part of base Python.  You do not need any other libraries.

## Usage

1.  **Run the Script:** Execute the Python script (`KCD2-Die-Optimizer.py`).  If you have a bundled executable version, run that instead.
2.  **Select Dice:** Check the boxes next to the dice types you have available.
3.  **Enter Quantities:** When you select a die (other than "Standard Die"), a dialog box will appear, prompting you to enter the quantity of that die you possess. Enter the number (0-10) and click "OK". If you make a mistake, uncheck and re-check the die to re-enter the quantity.  You can also load previously saved selections.
4.  **Recommend Combination:** Click the "Recommend Optimal Combination" button.
5.  **View Results:** The program will display the recommended 6-dice combination (or a message if no combination is possible), along with the detailed statistics mentioned above, in the GUI.  The calculation may take a few moments; a progress bar and status labels will indicate its progress.
	**Green:** Your combination's EV is above average.
	**Red:** Your combination's EV is below average.
	**Black:** Your combination's EV is exactly average.
6.  **Load Previous:** Click the 'Load Previous Dice' to select your previous dice.

## Changes from Previous Version

*   **Heuristic Optimization:** The core calculation is now a heuristic search instead of an exhaustive one. This drastically improves performance, especially with many different dice types.  The previous version's exhaustive search became incredibly slow with more than a few dice types.
*   **Progress Updates:**  The GUI now includes a progress bar and status labels to provide feedback during the calculation.
*   **Persistent Selections:**  Dice selections and quantities are saved to a `kc2_die_selections.json` file, so your choices are remembered between sessions.
*   **Improved Error Handling:** More robust error handling and user feedback.
*   **Refactored Code:**  The code has been reorganized and made more modular.
*   **Adaptive Queue Checking:** Queue checking interval increases gradually.


## Dice Probabilities

The `DICE_PROBABILITIES` dictionary in the code defines the probability distribution for each die.  Each entry is a list of six probabilities, corresponding to the chances of rolling a 1, 2, 3, 4, 5, or 6, respectively.  For example:

```python
DICE_PROBABILITIES = {
    "Ordinary die": [1/6, 1/6, 1/6, 1/6, 1/6, 1/6],
    "Weighted die": [0.667, 0.067, 0.067, 0.067, 0.067, 0.067],
    # ... other dice ...
}



