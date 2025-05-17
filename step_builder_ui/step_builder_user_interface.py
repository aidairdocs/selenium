# E:\CRM\automation_project\step_builder_ui\step_builder_user_interface.py
"""
Holds the user interface logic for selecting forms, creating steps, etc.
"""

import tkinter as tk
from tkinter import messagebox

def pick_form_gui(forms_list):
    """
    Displays a Tkinter window listing the forms in 'forms_list'.
    Returns the user-chosen form's id_uuid or None if cancelled.

    forms_list is expected to be something like:
    [
      { "id_uuid": "123...", "form_name": "My Form", "status": "development" },
      ...
    ]
    """

    print("[DEBUG] user_interface.pick_form_gui() called.")

    if not forms_list:
        print("[INFO] No forms to display.")
        return None

    # Create root window
    root = tk.Tk()
    root.title("Select a Form")
    root.geometry("900x900")
    root.resizable(False, False)

    chosen_form_var = tk.StringVar(value="")

    # Instructions label
    label = tk.Label(root, text="Select a form to automate:", font=("Arial", 12))
    label.pack(pady=10)

    # Listbox to display forms
    listbox = tk.Listbox(root, height=10, width=50)
    for idx, form in enumerate(forms_list):
        # e.g. "1. My Form (dev)"
        entry_text = f"{idx+1}. {form['form_name']} [{form.get('status','???')}]"
        listbox.insert(tk.END, entry_text)
    listbox.pack(pady=5)

    def on_submit():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a form.")
            return
        index = selection[0]
        chosen_form = forms_list[index]
        chosen_form_var.set(chosen_form["id_uuid"])
        root.destroy()

    # Submit button
    submit_btn = tk.Button(root, text="OK", command=on_submit)
    submit_btn.pack(pady=10)

    # Cancel button
    def on_cancel():
        chosen_form_var.set("")
        root.destroy()

    cancel_btn = tk.Button(root, text="Cancel", command=on_cancel)
    cancel_btn.pack()

    # Start Tk event loop
    root.mainloop()

    chosen_form_id = chosen_form_var.get()
    if chosen_form_id:
        print(f"[DEBUG] User selected form_id={chosen_form_id}")
        return chosen_form_id
    else:
        print("[DEBUG] User cancelled form selection.")
        return None
