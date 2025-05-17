import tkinter as tk
from tkinter import scrolledtext, messagebox

def safe_action(driver, selector_type, selector_value, step_value, step):
    """
    A manual "safe" action for sensitive steps that requires the user to complete a checklist before proceeding.
    
    The checklist items are:
      1. Request number saved
      2. Paid
      3. Receipt saved
      4. Recorded in CRM
      
    The window displays instructions, the step's description, and the checklist.
    The "Continue" button is disabled until all items are checked.
    If the user cancels, an exception is raised.
    """
    print("[DEBUG safe_action] Called for a safe (manual) step.")

    # Retrieve the step's description for user reference.
    description_text = step.get('description', 'No description provided.')

    # Create the main TK window with larger dimensions.
    root = tk.Tk()
    root.title("Safe Action - Manual Intervention Required")
    root.geometry("700x500")  # Increased window size
    root.resizable(False, False)
    root.attributes("-topmost", True)  # Keep the window on top

    # Instructions at the top.
    instructions = (
        "This step requires sensitive manual intervention.\n\n"
        "Please complete the required operation in the browser (e.g., enter your credit card number, "
        "take a screenshot, etc.).\n\n"
        "Before proceeding, please complete the following checklist by checking all items below."
    )
    inst_label = tk.Label(root, text=instructions, wraplength=680, justify=tk.LEFT)
    inst_label.pack(pady=10, padx=10)

    # Display the step description.
    desc_label = tk.Label(root, text="Step Description:", font=("Arial", 10, "bold"))
    desc_label.pack(padx=10, anchor=tk.W)
    
    desc_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=5)
    desc_text.pack(padx=10, pady=(0,10), fill=tk.BOTH, expand=True)
    desc_text.insert(tk.END, description_text)
    desc_text.config(state=tk.DISABLED)

    # Create a frame for the checklist.
    checklist_frame = tk.Frame(root)
    checklist_frame.pack(padx=10, pady=10, anchor=tk.W)

    # Define checklist items.
    items = [
        "Request number saved",
        "Paid",
        "Receipt saved",
        "Recorded in CRM"
    ]
    
    # Create a dictionary to hold the BooleanVars for each item.
    checklist_vars = {}
    
    # Function to check if all items are checked.
    def check_all():
        if all(var.get() for var in checklist_vars.values()):
            continue_btn.config(state=tk.NORMAL)
        else:
            continue_btn.config(state=tk.DISABLED)

    # Create checkboxes for each item.
    for item in items:
        var = tk.BooleanVar(value=False)
        checklist_vars[item] = var
        cb = tk.Checkbutton(checklist_frame, text=item, variable=var, command=check_all)
        cb.pack(anchor=tk.W)

    # Optional text area for user notes.
    notes_label = tk.Label(root, text="Additional Notes (optional):", font=("Arial", 10, "bold"))
    notes_label.pack(pady=(10,5), padx=10, anchor=tk.W)
    
    notes_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=4)
    notes_text.pack(fill=tk.BOTH, padx=10, pady=(0,10), expand=True)

    user_notes = {"text": ""}

    # Variable to store user's final choice.
    user_choice = tk.StringVar(value="")

    # Function for the Continue button.
    def on_continue():
        user_notes["text"] = notes_text.get("1.0", tk.END).strip()
        if not messagebox.askyesno("Confirm", "Are you sure you want to continue?"):
            return
        user_choice.set("continue")
        root.destroy()

    # Function for the Cancel button.
    def on_cancel():
        if messagebox.askyesno("Confirm Cancel", "Do you really want to stop execution entirely?"):
            user_choice.set("cancel")
            root.destroy()

    # Button frame (placed at the bottom).
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10, side=tk.BOTTOM)

    continue_btn = tk.Button(button_frame, text="Continue", width=15, command=on_continue, state=tk.DISABLED)
    continue_btn.pack(side=tk.LEFT, padx=5)

    cancel_btn = tk.Button(button_frame, text="Cancel", width=15, command=on_cancel)
    cancel_btn.pack(side=tk.LEFT, padx=5)

    root.mainloop()

    if user_choice.get() == "continue":
        if user_notes["text"]:
            print(f"[DEBUG safe_action] User notes: {user_notes['text']}")
        print("[DEBUG safe_action] User confirmed safe action; proceeding.")
        return  # Proceed with execution.
    else:
        print("[DEBUG safe_action] User cancelled safe action.")
        raise Exception("User cancelled safe action.")
