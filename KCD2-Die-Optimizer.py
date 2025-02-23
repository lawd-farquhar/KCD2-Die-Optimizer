import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import itertools
import collections
import json
import sys
import os
import time
import threading
import queue

# --- Core Calculation Functions --- (No changes here)
def calculate_score(dice):
    score = 0
    counts = [dice.count(i) for i in range(1, 7)]

    sorted_dice = sorted(dice)
    if sorted_dice in ([1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]):
        if sorted_dice == [1, 2, 3, 4, 5]: return 500
        if sorted_dice == [2, 3, 4, 5, 6]: return 750
        return 1500

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
    total_ev = 0
    roll_counts = collections.Counter()

    for roll in itertools.product(*[range(6) for _ in dice_combo]):
        probability = 1.0
        dice_outcomes = []
        for die_index, outcome_index in zip(dice_combo, roll):
            probability *= DICE_PROBABILITIES[die_index][outcome_index]
            dice_outcomes.append(outcome_index + 1)

        score = calculate_score(dice_outcomes)
        total_ev += probability * score
        roll_counts[tuple(sorted(dice_outcomes))] += probability

    most_likely_rolls = []
    max_probability = 0
    if roll_counts:
        max_probability = roll_counts.most_common(1)[0][1]
        most_likely_rolls = [roll for roll, prob in roll_counts.items() if prob == max_probability]

    max_score = -1
    highest_scoring_roll = None
    highest_scoring_roll_probability = 0

    for roll_indices in itertools.product(*[range(6) for _ in dice_combo]):
        roll = [i + 1 for i in roll_indices]
        valid_roll = True
        roll_prob = 1.0
        for i, die in enumerate(dice_combo):
            die_probs = DICE_PROBABILITIES[die]
            if die_probs[roll[i] - 1] == 0:
                valid_roll = False
                break
            roll_prob *= die_probs[roll[i] - 1]

        if valid_roll:
            score = calculate_score(roll)
            if score > max_score:
                max_score = score
                highest_scoring_roll = tuple(roll)
                highest_scoring_roll_probability = roll_prob
            elif score == max_score and highest_scoring_roll_probability < roll_prob:
                highest_scoring_roll = tuple(roll)
                highest_scoring_roll_probability = roll_prob

    prob_at_least_one_scoring_die = 1.0 - (
        1.0 - max(sum(DICE_PROBABILITIES[die][i] for i in (0, 4)) for die in dice_combo)
    )

    return (total_ev, most_likely_rolls, max_probability,
            highest_scoring_roll, max_score, highest_scoring_roll_probability,
            prob_at_least_one_scoring_die)


# --- GUI and Persistence Functions ---

def save_selections(checkbox_vars):
    selections = {}
    for die_name, data in checkbox_vars.items():
        selections[die_name] = {
            "selected": data["var"].get(), "quantity": data["quantity"]
        }
    try:
        with open("kc2_die_selections.json", "w") as f:
            json.dump(selections, f)
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save selections:\n{e}")

def load_selections(checkbox_vars, root):
    try:
        with open("kc2_die_selections.json", "r") as f:
            selections = json.load(f)
        for die_name, data in checkbox_vars.items():
            if die_name in selections:
                data["var"].set(selections[die_name]["selected"])
                data["quantity"] = selections[die_name]["quantity"]
                if data["var"].get() and die_name != "Standard Die":
                    data["checkbox"].config(state="disabled")
                    data["checkbox"].config(state="normal")
            else:
                data["var"].set(0)
                data["quantity"] = 0
                data["checkbox"].config(state="normal")

    except FileNotFoundError:
        pass
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not load previous selections:\n{e}")

def ask_for_quantity(die_name, checkbox_vars, root):
    checkbox_vars[die_name]["checkbox"].config(state="disabled")
    quantity = simpledialog.askinteger("Quantity", f"How many '{die_name}' dice do you have?", parent=root)
    checkbox_vars[die_name]["checkbox"].config(state="normal")

    if quantity is None:
        checkbox_vars[die_name]["var"].set(0)
        checkbox_vars[die_name]["quantity"] = 0
        return

    if not 0 <= quantity <= 10:
        messagebox.showerror("Invalid Quantity", "Quantity must be between 0 and 10.")
        checkbox_vars[die_name]["var"].set(0)
        checkbox_vars[die_name]["quantity"] = 0
        return

    checkbox_vars[die_name]["quantity"] = quantity
    checkbox_vars[die_name]["var"].set(1 if quantity > 0 else 0)
    save_selections(checkbox_vars)

def on_checkbox_change(die_name, checkbox_vars, root):
    if checkbox_vars[die_name]["var"].get() == 1:
        ask_for_quantity(die_name, checkbox_vars, root)
    else:
        checkbox_vars[die_name]["quantity"] = 0
        save_selections(checkbox_vars)


def calculate_optimal_combination_heuristic(user_dice_counts, progress_queue):
    """Calculates the optimal dice combination (heuristic, threaded)."""

    start_time = time.time()
    die_evs = {die_type: calculate_ev_and_modal_roll([die_type])[0] for die_type in DICE_PROBABILITIES}

    user_dice = []
    for die_type, count in user_dice_counts.items():
        user_dice.extend([die_type] * count)
    num_standard_dice = max(0, 6 - len(user_dice))
    user_dice.extend(["Standard Die"] * num_standard_dice)

    available_dice = sorted(user_dice, key=lambda die: die_evs.get(die, 0), reverse=True)
    current_combination = available_dice[:6]
    best_combination = list(current_combination)
    best_ev = calculate_ev_and_modal_roll(current_combination)[0]

    max_iterations = 500  # Or your preferred value
    progress_update_interval = 10
    improved_in_iteration = True

    for i in range(max_iterations):
        if not improved_in_iteration:
            break
        improved_in_iteration = False

        for j in range(6):
            for die_type in user_dice:
                if die_type not in current_combination:
                    new_combination = list(current_combination)
                    new_combination[j] = die_type
                    new_ev = calculate_ev_and_modal_roll(new_combination)[0]
                    if new_ev > best_ev:
                        best_ev = new_ev
                        best_combination = list(new_combination)
                        current_combination = list(new_combination)[:]
                        improved_in_iteration = True
        if (i + 1) % progress_update_interval == 0:
            elapsed_time = time.time() - start_time
            calculation_text = (
                f"Iteration: {i + 1}/{max_iterations}\n"
                f"Current Best EV: {best_ev:.2f}\n"
                f"Elapsed: {elapsed_time:.2f}s"
            )
            # Calculate percent *inside* the thread
            percent = int(((i + 1) / max_iterations) * 100)
            progress_queue.put(("progress", percent, calculation_text))  # Simplified message

    best_results = calculate_ev_and_modal_roll(best_combination)
    progress_queue.put(("result", best_combination, best_results, best_ev))


def recommend_combination_wrapper(checkbox_vars, result_label, ev_diff_label, progress_var, status_label, calculation_label):
    recommend_button.config(state="disabled")
    user_dice_counts = {die_name: data["quantity"] for die_name, data in checkbox_vars.items() if data["var"].get() == 1}
    progress_queue = queue.Queue()
    calculation_thread = threading.Thread(target=calculate_optimal_combination_heuristic, args=(user_dice_counts, progress_queue))
    calculation_thread.start()

    # Start checking the queue with a short initial delay
    root.after(10, lambda: check_queue(progress_queue, result_label, ev_diff_label, progress_var, status_label, calculation_label, calculation_thread, check_interval=10))


def check_queue(progress_queue, result_label, ev_diff_label, progress_var, status_label, calculation_label, calculation_thread, check_interval):
    """Checks the queue (with adaptive interval)."""
    try:
        message = progress_queue.get_nowait()
        if message[0] == "progress":
            percent, calculation_text = message
            progress_var.set(percent)
            status_label.config(text=f"Optimizing... {percent}%")
            calculation_label.config(text=calculation_text)

        elif message[0] == "result":
            _, optimal_combo, best_results, max_ev = message
            # (Result handling logic - same as before)
            try:
                if optimal_combo:
                    modal_rolls = best_results[1]
                    modal_probability = best_results[2]
                    high_roll = best_results[3]
                    high_score = best_results[4]
                    high_roll_prob = best_results[5]
                    scoring_die_prob = best_results[6]
                    modal_rolls_str = ", ".join(str(roll) for roll in modal_rolls)
                    has_duplicates = False
                    for die, count in collections.Counter(optimal_combo).items():
                        if die != "Standard Die" and count > 1:
                            has_duplicates = True
                            break

                    avg_ev_with_duplicates = 584.39
                    avg_ev_no_duplicates = 576.86
                    if has_duplicates:
                        comparison_ev = avg_ev_with_duplicates
                    else:
                        comparison_ev = avg_ev_no_duplicates

                    ev_difference = max_ev - comparison_ev
                    ev_diff_str = f"{'+' if ev_difference >= 0 else ''}{ev_difference:.2f}"
                    result_text = (
                        f"Optimal: {', '.join(optimal_combo)}\n"
                        f"EV: {max_ev:.2f}\n"
                        f"Most Likely: {modal_rolls_str}\n"
                        f"Probability: {modal_probability * 100:.2f}%\n"
                        f"Highest Roll: {high_roll}\n"
                        f"Score: {high_score}\n"
                        f"Probability: {high_roll_prob * 100:.6f}%\n"
                        f"P(1 or 5): {scoring_die_prob * 100:.2f}%\n"
                        f"EV vs. Avg: {ev_diff_str}"
                    )
                    result_label.config(text=result_text)
                    #set label colors
                    if ev_difference > 0:
                        style.configure("Positive.TLabel", foreground=positive_color)
                        ev_diff_label.config(style="Positive.TLabel")
                    elif ev_difference < 0:
                        style.configure("Negative.TLabel", foreground=negative_color)
                        ev_diff_label.config(style="Negative.TLabel")
                    else:
                        style.configure("Neutral.TLabel", foreground=neutral_color)
                        ev_diff_label.config(style="Neutral.TLabel")
                    ev_diff_label.config(text=ev_diff_str)
                else:
                    result_label.config(text="No optimal combination.")
                    ev_diff_label.config(text="")

            except (TypeError, ValueError, Exception) as e:
                result_label.config(text=f"Error: {e}")
                ev_diff_label.config(text="")

            progress_var.set(100)
            recommend_button.config(state="enabled")
            status_label.config(text="Calculation complete!")
            calculation_label.config(text="")

    except queue.Empty:
        pass

    # Increase check_interval gradually, up to a maximum
    if calculation_thread.is_alive():
        check_interval = min(check_interval + 5, 100)  # Increase, but cap at 100ms
        root.after(check_interval, lambda: check_queue(progress_queue, result_label, ev_diff_label, progress_var, status_label, calculation_label, calculation_thread, check_interval))



bg_color = "#362c28"
button_color = "#A97B65"
text_color = "#F2E8C6"
positive_color = "#6B8E23"
negative_color = "#8B0000"
neutral_color = "#F2E8C6"
highlight_color = "#e69d45"
check_on_color = "#ffd700"
check_off_color = "#4d4d4d"

def get_image_path(filename):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)

# --- Main App Setup ---

root = tk.Tk()
root.title("KC2 Die Optimizer")
root.configure(bg=bg_color)

# --- UI Setup (Styles, Checkboxes, Buttons, etc.) ---

style = ttk.Style()
style.theme_use('default')

style.configure(".", background=bg_color, foreground=text_color, font=("Georgia", 10))
style.configure("TButton", background=button_color, foreground=text_color, borderwidth=2, relief="ridge", font=("Georgia", 10, "bold"))
style.map("TButton",
        background=[("active", highlight_color), ("pressed", button_color)],
        foreground=[("active", text_color), ("pressed", text_color)])
style.configure("TCheckbutton", background=bg_color, foreground=text_color, font=("Georgia", 10),
            indicatorcolor=check_off_color)
style.map("TCheckbutton",
        foreground=[("active", highlight_color)],
        indicatorcolor=[("selected", check_on_color), ("active", highlight_color)]
        )
style.configure("TLabel", background=bg_color, foreground=text_color, padding=5)
style.configure("Neutral.TLabel", foreground=neutral_color, font=("Georgia", 12, "bold"))
style.configure("TProgressbar", troughcolor=bg_color, borderwidth=2, background=highlight_color)
style.configure("TScrollbar", troughcolor=bg_color, borderwidth=2, arrowcolor=button_color)
style.configure("Vertical.TScrollbar", background=button_color)

checkbox_vars = {}
dice_names = sorted(DICE_PROBABILITIES.keys())
row = 0
col = 0

button_frame = ttk.Frame(root)
button_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

load_button = ttk.Button(button_frame, text="Load Previous Dice", command=lambda: load_selections(checkbox_vars, root))
load_button.grid(row=0, column=0, padx=5, sticky="ew")
recommend_button = ttk.Button(button_frame,text="Recommend Optimal Combination",state="normal")

recommend_button.grid(row=0, column=1, padx=5, sticky="ew")

checkbox_frame = ttk.Frame(root)
checkbox_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

yscrollbar = ttk.Scrollbar(checkbox_frame, orient=tk.VERTICAL, style="Vertical.TScrollbar")
yscrollbar.grid(row=0, column=2, sticky='ns')

canvas = tk.Canvas(checkbox_frame, yscrollcommand=yscrollbar.set, bg=bg_color, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2, sticky="nsew")
yscrollbar.config(command=canvas.yview)

inner_frame = ttk.Frame(canvas, style="TFrame")
canvas.create_window((0, 0), window=inner_frame, anchor='nw')

for die_name in dice_names:
    var = tk.IntVar()
    checkbox = ttk.Checkbutton(inner_frame, text=die_name, variable=var,
                            command=lambda dn=die_name: on_checkbox_change(dn, checkbox_vars, root),
                            style="TCheckbutton")
    checkbox.grid(row=row, column=col, sticky="w", padx=5, pady=2)
    checkbox_vars[die_name] = {"var": var, "checkbox": checkbox, "quantity": 0}
    col += 1
    if col > 2:
        col = 0
        row += 1

def configure_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.config(height=min(inner_frame.winfo_reqheight(), 400))
inner_frame.bind("<Configure>", configure_scroll_region)

tavern_frame = tk.Frame(root, bg=bg_color)
tavern_frame.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)

try:
    torch_image = tk.PhotoImage(file=get_image_path("torch.gif"))
    smaller_torch = torch_image.subsample(3, 3)

    left_torch = tk.Label(tavern_frame, image=smaller_torch, bg=bg_color, bd=0)
    left_torch.image = smaller_torch
    left_torch.grid(row=0, column=0, padx=(20, 0), pady=10, sticky="w")

    right_torch = tk.Label(tavern_frame, image=smaller_torch, bg=bg_color, bd=0)
    right_torch.image = smaller_torch
    right_torch.grid(row=0, column=2, padx=(0, 20), pady=10, sticky="e")

    label_frame = tk.Frame(tavern_frame, bg=bg_color)
    label_frame.grid(row=0, column=1, sticky="nsew")
    result_label = ttk.Label(label_frame, text="", justify="left", font=("Georgia", 10), style="TLabel")
    result_label.pack(pady=(10, 5))

    ev_diff_label = ttk.Label(label_frame, text="", style="Neutral.TLabel")
    ev_diff_label.pack(pady=(5, 10))

    tavern_frame.columnconfigure(0, weight=0)
    tavern_frame.columnconfigure(1, weight=1)
    tavern_frame.columnconfigure(2, weight=0)

except Exception as e:
    print(f"Error loading torch image: {e}")
    result_label = ttk.Label(tavern_frame, text="", justify="left", font=("Georgia", 10))
    result_label.pack()
    ev_diff_label = ttk.Label(tavern_frame, text="", style="Neutral.TLabel")
    ev_diff_label.pack()

progress_frame = tk.Frame(root, bg=bg_color)
progress_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate", variable=progress_var, style="TProgressbar")
progress_bar.pack(pady=5)

status_label = ttk.Label(progress_frame, text="", justify="center", style="TLabel")
status_label.pack(pady=5)

calculation_label = ttk.Label(progress_frame, text="", justify="left", style="TLabel")  # New label
calculation_label.pack(pady=5)

root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=0)
root.rowconfigure(3, weight=0)
checkbox_frame.columnconfigure(0, weight=1)
checkbox_frame.rowconfigure(0, weight=1)
canvas.columnconfigure(0, weight=1)

# --- Event Handlers ---

recommend_button.config(command=lambda: recommend_combination_wrapper(checkbox_vars, result_label, ev_diff_label, progress_var, status_label, calculation_label))

if __name__ == "__main__":
    root.mainloop()

