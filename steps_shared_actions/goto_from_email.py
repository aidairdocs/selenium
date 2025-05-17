# E:\CRM\automation_project\steps_shared_actions\goto_from_email_now_action.py

import tkinter as tk
from steps_shared_actions.alert_handler import handle_unexpected_alerts

def goto_from_email(driver, selector_type, selector_value, step_value, step):
    """
    goto_from_email_now_action(...)

    This action displays a Tk popup at runtime, asking the user to paste
    the new URL from their email (which contains a dynamic TOKEN, etc.).
    Then we do driver.get(...) to that URL in the same Selenium session.

    The 'selector_type'/'selector_value' aren't used. 'step_value' is ignored
    because the user link might be new each time. 
    """
    print("[DEBUG] goto_from_email_now_action started.")

    # 1) Check if any leftover alert
    handle_unexpected_alerts(driver, action="accept")

    # 2) Show a small Tk window to prompt user for the dynamic URL
    link = _prompt_for_email_link()

    # 3) If user gave something, navigate to it
    if link.strip():
        print(f"[DEBUG] Navigating to user-provided link => {link}")
        driver.get(link.strip())
    else:
        print("[WARNING] No link provided. Doing nothing.")

    print("[DEBUG] goto_from_email_now_action done.")


def _prompt_for_email_link():
    """
    Displays a Tkinter dialog asking user to paste the unique link
    from their email. Returns the string that user typed.
    """
    root = tk.Tk()
    root.title("Goto from Email")
    root.geometry("600x200")
    root.resizable(False, False)

    link_var = tk.StringVar()

    label = tk.Label(root, text="Please paste the unique link from your email:", wraplength=550, justify=tk.LEFT)
    label.pack(pady=10)

    entry = tk.Entry(root, textvariable=link_var, width=80)
    entry.pack(pady=5)

    user_closed = {"closed": True}  # track if user clicked "Cancel" or closed window

    def on_ok():
        user_closed["closed"] = False
        root.destroy()

    def on_cancel():
        root.destroy()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)

    ok_btn = tk.Button(btn_frame, text="OK", width=10, command=on_ok)
    ok_btn.pack(side=tk.LEFT, padx=5)

    cancel_btn = tk.Button(btn_frame, text="Cancel", width=10, command=on_cancel)
    cancel_btn.pack(side=tk.LEFT, padx=5)

    root.mainloop()

    if user_closed["closed"]:
        # user closed or canceled => return empty string
        return ""
    return link_var.get()
