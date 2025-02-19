# Farkle Dice Optimizer

This Python script helps you optimize your dice selection in the game of Farkle in KCD2. It calculates the expected value (EV) of different dice combinations and recommends the optimal 6-die combination based on your available dice. It also identifies the most likely roll and the highest-scoring possible roll for a given combination.

## Features

*   **Dice Selection:**  Choose from a comprehensive list of Farkle dice with varying probabilities gathered from u/Nigi_1 on Reddit via https://www.reddit.com/r/kingdomcome/comments/1ijaac0/kcd2_dice_weight_table/.  You can specify the *quantity* of each die type you have.
*   **Optimal Combination Recommendation:** The program calculates the optimal 6-dice combination from your selected dice, maximizing the expected value (EV).
*   **Detailed Statistics:**  For the recommended combination, the program displays:
    *   Expected Value (EV)
    *   Most Likely Roll(s) and their probability
    *   Highest Scoring Roll and its probability
    *   Probability of rolling at least one 1 or 5 (scoring probability)
    *   Comparison of the selected combination's EV to the average EV of all dice combinations (with and without duplicates, as appropriate), displayed in green (above average), red (below average), or black (average).
*   **User-Friendly GUI:**  A graphical interface (built with Tkinter) makes it easy to select dice and view results.
*   **Handles Duplicates:**  The program correctly handles duplicate dice selections. The "Standard Die" is allowed to have duplicates; any other dice will prompt user for the quantity.
*	 **Average EV benchmarks for the comparison:**
     *   Average EV with Duplicates is set at 584.39
	 *   Average EV without duplicates (except standard): 576.86
*   **Error Handling:**  The program handles potential errors gracefully, displaying informative messages within the GUI.



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

1.  **Run the Script:** Execute the Python script (`KCD2-Die-Optimizer.py`).
2.  **Select Dice:** Check the boxes next to the dice types you have available.
3.  **Enter Quantities:** When you select a die (other than "Standard Die"), a dialog box will appear, prompting you to enter the quantity of that die you possess.  Enter the number and click "OK".  If you make a mistake, uncheck and re-check the die to re-enter the quantity.
4.  **Recommend Combination:** Click the "Recommend Optimal Combination" button.
5.  **View Results:** The program will display the optimal 6-dice combination, along with the detailed statistics mentioned above, in the GUI. The EV comparison to the average will be color-coded:
    *   **Green:** Your combination's EV is above average.
    *   **Red:** Your combination's EV is below average.
    *   **Black:** Your combination's EV is exactly average.

## Dice Probabilities

The `DICE_PROBABILITIES` dictionary in the code defines the probability distribution for each die.  Each entry is a list of six probabilities, corresponding to the chances of rolling a 1, 2, 3, 4, 5, or 6, respectively.  For example:

```python
DICE_PROBABILITIES = {
    "Ordinary die": [1/6, 1/6, 1/6, 1/6, 1/6, 1/6],
    "Weighted die": [0.667, 0.067, 0.067, 0.067, 0.067, 0.067],
    # ... other dice ...
}


