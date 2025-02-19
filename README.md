# Farkle Dice Optimizer

This Python script helps you optimize your dice selection in the game of Farkle in KCD2. It calculates the expected value (EV) of different dice combinations and recommends the optimal 6-die combination based on your available dice. It also identifies the most likely roll and the highest-scoring possible roll for a given combination.

## Features

*   **Comprehensive Dice Database:** Includes a wide variety of dice with different probability distributions, based on u/Nigi_1's reddit post https://www.reddit.com/r/kingdomcome/comments/1ijaac0/kcd2_dice_weight_table/.  Also includes a "Standard Die" for fair comparisons.
*   **Expected Value (EV) Calculation:**  Accurately calculates the expected value of any 6-die combination.
*   **Optimal Combination Recommendation:**  Determines the optimal 6-die combination from a user-specified set of dice (or fills in with standard dice if fewer than 6 are selected).
*   **Most Likely Roll Analysis:** Identifies the most likely roll(s) for a given die combination and their probability.
*   **Highest Scoring Roll Identification:** Finds the highest-scoring roll that is *possible* with the selected dice (even if that roll has a very low probability).
*   **Multiple Dice of Same Type:** Allows the user to specify how many of each type of die they have.
*   **Scrollable GUI:**  User-friendly graphical interface (GUI) built with Tkinter, featuring a scrollable list of checkboxes for die selection.
*   **Error Handling:** Includes error handling for invalid user input.

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

1.  **Run the Script:**
    ```bash
    python KCD2-Die-Optimizer.py
    ```
2.  **Select Your Dice:**  The GUI will appear, showing a list of dice.  Check the boxes next to the dice you have.
3.  **Enter Quantities:**  If you select a die, a dialog box will pop up, asking you how many of that die you have.  Enter the quantity (0-10) and press Enter.  If you enter 0, the checkbox will automatically uncheck.
4.  **Click "Recommend Optimal Combination":**  After selecting your dice, click this button. The program will calculate the best 6-die combination from your selection (adding "Standard Dice" if you selected fewer than 6). The results will be displayed in a message box, including:
    *   The optimal die combination.
    *   The expected value (EV) of that combination.
    *   The most likely roll(s) for that combination.
    *   The probability of the most likely roll(s).
    *   The highest possible score for that combination.
    *   Roll associated with highest possible score.

## Dice Probabilities

The `DICE_PROBABILITIES` dictionary in the code defines the probability distribution for each die.  Each entry is a list of six probabilities, corresponding to the chances of rolling a 1, 2, 3, 4, 5, or 6, respectively.  For example:

```python
DICE_PROBABILITIES = {
    "Ordinary die": [1/6, 1/6, 1/6, 1/6, 1/6, 1/6],
    "Weighted die": [0.667, 0.067, 0.067, 0.067, 0.067, 0.067],
    # ... other dice ...
}


