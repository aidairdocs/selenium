from steps_shared_utils.steps_shared_conditions_registry import CONDITION_EXPRESSIONS

def pick_conditions_gui():
    """
    Displays a small Tkinter window listing all available condition keys 
    (e.g. from conditions_registry.py). The user can select none, one, or multiple.

    Returns a list of condition keys, e.g. ["IS_MINOR_TRUE", "HAS_SECOND_PASSPORT"].
    If the user picks none, returns an empty list => means no condition.
    """
    import tkinter as tk

    # Suppose we have:
    
    all_keys = sorted(CONDITION_EXPRESSIONS.keys())

    root = tk.Tk()
    root.title("Select Conditions")
    root.geometry("400x400")
    root.resizable(False, False)

    label = tk.Label(root, text="Select zero or multiple conditions for this step:")
    label.pack(pady=5)

    listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50, height=10)
    for key in all_keys:
        listbox.insert(tk.END, key)
    listbox.pack(pady=5)

    chosen = []

    def on_ok():
        selection = listbox.curselection()
        for i in selection:
            key = listbox.get(i)
            chosen.append(key)
        root.destroy()

    btn = tk.Button(root, text="OK", command=on_ok)
    btn.pack(pady=10)

    root.mainloop()
    return chosen
