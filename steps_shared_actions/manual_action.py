# E:\CRM\automation_project\steps_shared_actions\manual_action.py

import tkinter as tk
from tkinter import scrolledtext, messagebox
#from steps_shared_actions.alert_handler import handle_unexpected_alerts  # optional, if you want to check alerts

def manual_action(driver, selector_type, selector_value, step_value, step):
    """
    A run-time action for 'manual' steps. Displays a pop-up with the step's description,
    waits for user confirmation, then proceeds.

    Improvements:
    1) Properly imports tkinter as 'tk', removing the error about 'module 'tk' has no attribute 'Tk'.
    2) Two buttons: "Continue" (go next) or "Cancel" (stop execution).
    3) Optional text area for the user to leave notes.
    4) Scrollable text for long descriptions.
    5) Window stays on top, so user doesn't lose it behind the browser (optional).
    """
    print("[DEBUG manual_action] Called for a manual step.")
    
    description_text = step.get('description', 'No description provided.')

    # (A) Optional: Check for leftover alert before the manual step
    # handle_unexpected_alerts(driver, action="accept")

    # Create the Tk root window
    root = tk.Tk()
    root.title("Manual Step")
    root.geometry("600x300")
    root.resizable(False, False)

    # (Optional) Force window to stay on top of others
    root.attributes("-topmost", True)

    # Instructions label at the top
    instructions = (
        "This step requires manual intervention.\n\n"
        "Please read the description below, perform the required action in the browser, "
        "then click 'Continue' to proceed or 'Cancel' to stop execution."
    )
    header_label = tk.Label(root, text=instructions, wraplength=580, justify=tk.LEFT)
    header_label.pack(pady=10, padx=10)

    # A scrollable text area for the description (in case it's long)
    desc_frame = tk.Frame(root)
    desc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))

    desc_text = scrolledtext.ScrolledText(desc_frame, wrap=tk.WORD, width=70, height=4)
    desc_text.pack(fill=tk.BOTH, expand=True)
    desc_text.insert(tk.END, description_text)
    desc_text.config(state=tk.DISABLED)  # make it read-only

    # (Optional) Provide a text area for user notes or remarks about what they did manually
    notes_label = tk.Label(root, text="Notes / Comments (optional):")
    notes_label.pack(pady=(0,5), padx=10, anchor=tk.W)

    user_notes = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=3)
    user_notes.pack(fill=tk.X, padx=10, pady=(0,10))

    # We’ll store the user’s notes if needed
    user_notes_var = {"text": ""}

    # Button frame for Continue / Cancel
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    # This function is called when user clicks Continue
    def on_continue():
        user_notes_var["text"] = user_notes.get("1.0", tk.END).strip()
        root.destroy()

    # This function is called when user clicks Cancel
    def on_cancel():
        # If you want to confirm the user truly wants to stop:
        if messagebox.askyesno("Confirm Cancel", "Do you want to stop execution entirely?"):
            # We can raise an exception or set some global var to break out of the step flow
            root.destroy()
            raise Exception("[MANUAL ACTION] User cancelled automation.")
        # else do nothing, remain in the same window

    continue_btn = tk.Button(button_frame, text="Continue", width=12, command=on_continue)
    continue_btn.pack(side=tk.LEFT, padx=5)

    cancel_btn = tk.Button(button_frame, text="Cancel", width=12, command=on_cancel)
    cancel_btn.pack(side=tk.LEFT, padx=5)

    root.mainloop()

    # Once the user clicked Continue, the window is destroyed, and we proceed here
    # (B) If you want to do something with user_notes_var["text"], like:
    if user_notes_var["text"]:
        print(f"[DEBUG manual_action] User notes: {user_notes_var['text']}")

    print("[DEBUG manual_action] User clicked 'Continue'. Proceeding...")

    # (C) Optional: Check for any new alert after manual step
    # handle_unexpected_alerts(driver, action="accept")
