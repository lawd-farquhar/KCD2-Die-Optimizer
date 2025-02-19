import itertools
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import collections

# --- Farkle Scoring and Probability Logic ---
def calculate_score(dice):
    score = 0
    counts = [dice.count(i) for i in range(1, 7)]

    if sorted(dice) == [1, 2, 3, 4, 5]:
        return 500
    if sorted(dice) == [2, 3, 4, 5, 6]:
        return 750

    for num, count in enumerate(counts, start=1):
        if count >= 3:
            base_score = 1000 if num == 1 else num * 100
            score += base_score * (2 ** (count - 3))
            counts[num - 1] = 0

    score += 100 * counts[0]
    score += 50 * counts[4]
    return score

DICE_PROBABILITIES = {
    "Aranka's die": [0.286, 0.048, 0.286, 0.048, 0.286, 0.048],
    "Cautious cheater's die": [0.238, 0.143, 0.095, 0.143, 0.238, 0.143],
    "Ci die": [0.13, 0.13, 0.13, 0.13, 0.13, 0.348],
    "Devil's head die": [0.167, 0.167, 0.167, 0.167, 0.167, 0.167],
    "Die of misfortune": [0.045, 0.227, 0.227, 0.227, 0.227, 0.045],
    "Even die": [0.067, 0.267, 0.067, 0.267, 0.067, 0.267],
    "Favourable die": [0.333, 0.0, 0.056, 0.056, 0.333, 0.222],
    "Fer die": [0.13, 0.13, 0.13, 0.13, 0.13, 0.348],
    "Greasy die": [0.176, 0.118, 0.176, 0.118, 0.176, 0.235],
    "Grimy die": [0.063, 0.313, 0.063, 0.063, 0.438, 0.063],
    "Grozav's lucky die": [0.067, 0.667, 0.067, 0.067, 0.067, 0.067],
    "Heavenly Kingdom die": [0.368, 0.105, 0.105, 0.105, 0.105, 0.211],
    "Holy Trinity die": [0.182, 0.227, 0.455, 0.045, 0.045, 0.045],
    "Hugo's Die": [0.167, 0.167, 0.167, 0.167, 0.167, 0.167],
    "King's die": [0.125, 0.188, 0.219, 0.25, 0.125, 0.094],
    "Lousy gambler's die": [0.1, 0.15, 0.1, 0.15, 0.35, 0.15],
    "Lu die": [0.13, 0.13, 0.13, 0.13, 0.13, 0.348],
    "Lucky Die": [0.273, 0.045, 0.091, 0.136, 0.182, 0.273],
    "Mathematician's Die": [0.167, 0.208, 0.25, 0.292, 0.042, 0.042],
    "Molar die": [0.167, 0.167, 0.167, 0.167, 0.167, 0.167],
    "Odd die": [0.267, 0.067, 0.267, 0.067, 0.267, 0.067],
    "Ordinary die": [0.167, 0.167, 0.167, 0.167, 0.167, 0.167],
    "Painted die": [0.188, 0.063, 0.063, 0.063, 0.438, 0.188],
    "Pie die": [0.462, 0.077, 0.231, 0.231, 0.0, 0.0],
    "Premolar die": [0.167, 0.167, 0.167, 0.167, 0.167, 0.167],
    "Sad Greaser's Die": [0.261, 0.261, 0.043, 0.043, 0.261, 0.13],
    "Saint Antiochus' die": [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
    "Shrinking die": [0.222, 0.111, 0.111, 0.111, 0.111, 0.333],
    "St. Stephen's die": [0.167, 0.167, 0.167, 0.167, 0.167, 0.167],
    "Strip die": [0.25, 0.125, 0.125, 0.125, 0.188, 0.188],
    "Three die": [0.125, 0.063, 0.563, 0.063, 0.125, 0.063],
    "Unbalanced Die": [0.25, 0.333, 0.083, 0.083, 0.167, 0.083],
    "Unlucky die": [0.091, 0.273, 0.182, 0.182, 0.182, 0.091],
    "Wagoner's Die": [0.056, 0.278, 0.333, 0.111, 0.111, 0.111],
    "Weighted die": [0.667, 0.067, 0.067, 0.067, 0.067, 0.067],
    "Wisdom tooth die": [0.167, 0.167, 0.167, 0.167, 0.167, 0.167],
    "Standard Die": [1/6, 1/6, 1/6, 1/6, 1/6, 1/6],
}

def calculate_ev_and_modal_roll(dice_combo):
    """EV, most likely roll, and highest scoring roll."""
    total_ev = 0
    roll_probabilities = {}
    all_possible_rolls = itertools.product(*[range(1, 7) for _ in dice_combo])

    for roll in all_possible_rolls:
        probability = 1.0
        for die, outcome in zip(dice_combo, roll):
            probability *= DICE_PROBABILITIES[die][outcome - 1]
        score = calculate_score(roll)
        total_ev += probability * score

        sorted_roll = tuple(sorted(roll))
        if sorted_roll in roll_probabilities:
            roll_probabilities[sorted_roll] += probability
        else:
            roll_probabilities[sorted_roll] = probability
    max_probability = 0
    most_likely_rolls = []

    for roll, prob in roll_probabilities.items():
        if prob > max_probability:
            max_probability = prob
            most_likely_rolls = [roll]
        elif prob == max_probability:
            most_likely_rolls.append(roll)
    max_score = -1
    highest_scoring_roll = None
    # Corrected Highest Scoring Roll Logic
    for roll in itertools.product(*[range(1, 7) for _ in dice_combo]):  # Iterate through ALL possible rolls
        valid_roll = True
        for i, die in enumerate(dice_combo):
            die_probs = DICE_PROBABILITIES[die]
            if die_probs[roll[i]-1] == 0:  # Check if this outcome is possible for this die
                valid_roll = False
                break  # No need to check other dice in this roll
        if valid_roll:
            score = calculate_score(roll)
            if score > max_score:
                max_score = score
                highest_scoring_roll = tuple(roll)

    return total_ev, most_likely_rolls, max_probability, highest_scoring_roll, max_score

def recommend_optimal_dice(user_dice_counts):
    """
    Recommends optimal dice, accounting for counts.  Fills with Standard Dice.
    """
    user_dice = []
    for die_type, count in user_dice_counts.items():
        user_dice.extend([die_type] * count)

    num_standard_dice = max(0, 6 - len(user_dice))
    full_dice_set = user_dice + ["Standard Die"] * num_standard_dice

    max_ev = -1
    optimal_combo = None
    best_modal_rolls = None
    best_modal_probability = 0
    best_high_roll = None
    best_high_score = -1

    for combo in itertools.combinations(full_dice_set, 6):
        ev, modal_rolls, modal_probability, high_roll, high_score = calculate_ev_and_modal_roll(combo)
        if ev > max_ev:
            max_ev = ev
            optimal_combo = combo
            best_modal_rolls = modal_rolls
            best_modal_probability = modal_probability
            best_high_roll = high_roll
            best_high_score = high_score

    return optimal_combo, max_ev, best_modal_rolls, best_modal_probability, best_high_roll, best_high_score

# --- GUI Setup ---

def ask_for_quantity(die_name, checkbox_vars, root):
    checkbox_vars[die_name]["checkbox"].config(state="disabled")
    quantity = simpledialog.askinteger("Quantity", f"How many '{die_name}' dice do you have?",
                                       parent=root, minvalue=0, maxvalue=10)
    checkbox_vars[die_name]["checkbox"].config(state="normal")
    if quantity is None:
        checkbox_vars[die_name]["var"].set(0)
        return

    checkbox_vars[die_name]["quantity"] = quantity
    if quantity == 0:
        checkbox_vars[die_name]["var"].set(0)
    else:
        checkbox_vars[die_name]["var"].set(1)

def on_checkbox_change(die_name, checkbox_vars, root):
    if checkbox_vars[die_name]["var"].get() == 1:
        ask_for_quantity(die_name, checkbox_vars, root)
    else:
        checkbox_vars[die_name]["quantity"] = 0

def recommend_combination_wrapper(checkbox_vars):
    user_dice_counts = {}
    for die_name, data in checkbox_vars.items():
        if data["var"].get() == 1:
            user_dice_counts[die_name] = data["quantity"]

    try:
        optimal_combo, max_ev, modal_rolls, modal_probability, high_roll, high_score = recommend_optimal_dice(user_dice_counts)

        if optimal_combo:
            modal_rolls_str = ", ".join(str(roll) for roll in modal_rolls)
            messagebox.showinfo("Optimal Combination",
                                f"Optimal Die Combination: {', '.join(optimal_combo)}\n"
                                f"Expected Value (EV): {max_ev:.2f}\n"
                                f"Most Likely Roll(s): {modal_rolls_str}\n"
                                f"Probability of Most Likely Roll: {modal_probability:.4f}\n"
                                f"Highest Scoring Roll: {high_roll}\n"
                                f"Score: {high_score}"
                                )
        else:
            messagebox.showinfo("No Combination Found", "No optimal 6-die combination could be formed.")

    except ValueError as e:
        messagebox.showerror("Selection Error", str(e))
    except Exception as e:
        messagebox.showerror("Unexpected Error", str(e))

root = tk.Tk()
root.title("Farkle Dice Optimizer")

checkbox_vars = {}
dice_names = sorted(DICE_PROBABILITIES.keys())
row = 0
col = 0

checkbox_frame = tk.Frame(root)
checkbox_frame.grid(row=0, column=0, sticky="nsew")
yscrollbar = ttk.Scrollbar(checkbox_frame, orient=tk.VERTICAL)
yscrollbar.grid(row=0, column=2, sticky='ns')

canvas = tk.Canvas(checkbox_frame, yscrollcommand=yscrollbar.set)
canvas.grid(row=0, column=0, columnspan = 2, sticky="nsew")
yscrollbar.config(command=canvas.yview)

inner_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor='nw')

for die_name in dice_names:
    var = tk.IntVar()
    checkbox = ttk.Checkbutton(inner_frame, text=die_name, variable=var,
                               command=lambda dn=die_name: on_checkbox_change(dn, checkbox_vars, root))
    checkbox.grid(row=row, column=col, sticky="w", padx=5, pady=2)

    checkbox_vars[die_name] = {"var": var, "checkbox": checkbox, "quantity": 0}
    col += 1
    if col > 2:
        col = 0
        row += 1

def configure_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

inner_frame.bind("<Configure>", configure_scroll_region)

recommend_button = ttk.Button(root, text="Recommend Optimal Combination",
                           command=lambda: recommend_combination_wrapper(checkbox_vars))
recommend_button.grid(row=1, column=0, pady=10)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
checkbox_frame.columnconfigure(0, weight=1)
checkbox_frame.rowconfigure(0, weight=1)
canvas.columnconfigure(0, weight = 1)

root.mainloop()
