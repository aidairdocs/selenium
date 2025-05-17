# E:\CRM\automation_project\step_builder_main_controller.py

import sys
import tkinter as tk
from tkinter import messagebox

from step_builder_db_manager import get_connection
from step_builder_repositories.step_builder_forms_repository import load_forms
from step_builder_repositories.step_builder_form_steps_repository import load_form_steps
from step_builder_ui.step_builder_user_interface import pick_form_gui
from steps_shared_utils.steps_shares_browser_manager import init_browser, close_browser
from step_builder_selenium_flow.step_builder_step_executor import run_steps
from step_builder_selenium_flow.step_builder_create_new_step_flow import create_new_step_flow

def main():
    print("[DEBUG] main_controller.py started.")
    print("[DEBUG] Attempting to connect to the database...")

    # 1) Verify DB connection:
    try:
        with get_connection() as conn:
            print("[DEBUG] Successfully connected to the database.")
    except Exception as e:
        print(f"[ERROR] Failed to connect to DB: {e}")
        sys.exit(1)

    # 2) Load forms
    try:
        print("[DEBUG] Fetching available forms...")
        forms_list = load_forms()
        print(f"[DEBUG] Found {len(forms_list)} form(s).")
    except Exception as e:
        print(f"[ERROR] Failed to load forms: {e}")
        sys.exit(1)

    if not forms_list:
        print("[INFO] No forms found. Exiting.")
        sys.exit(0)

    # 3) Pick a form
    print("[DEBUG] Invoking form selection UI...")
    chosen_form_id = pick_form_gui(forms_list)
    if not chosen_form_id:
        print("[INFO] User cancelled. Exiting.")
        sys.exit(0)

    # Lookup the chosen form's details (ID and form_name)
    chosen_form = None
    for form in forms_list:
        if form["id_uuid"] == chosen_form_id:
            chosen_form = form
            break

    if not chosen_form:
        print("[ERROR] Chosen form not found in the forms list. Exiting.")
        sys.exit(1)

    print(f"[DEBUG] User selected form_id={chosen_form['id_uuid']}, form_name={chosen_form['form_name']}.")

    # 4) Load steps for that form
    try:
        print(f"[DEBUG] Loading steps for form_id={chosen_form['id_uuid']}...")
        steps_data = load_form_steps(chosen_form['id_uuid'])
        print(f"[DEBUG] Loaded {len(steps_data.get('steps', []))} step(s).")
    except Exception as e:
        print(f"[ERROR] Failed to load steps: {e}")
        sys.exit(1)

    # 5) Initialize browser (keep it open for the entire session)
    driver = init_browser(headless=False)

    try:
        # 6) Run the existing steps (all from step #1 by default)
        print("[DEBUG] Running initial steps from step #1.")
        # Pass form_id and form_name to run_steps
        run_steps(steps_data, driver=driver, start_step=1, form_id=chosen_form['id_uuid'], form_name=chosen_form['form_name'])

        # 7) Repeatedly ask if user wants to create more steps
        while True:
            user_choice = messagebox.askyesno(
                "Create a New Step?",
                "Do you want to create a new step for this form?\n\n(Click 'No' to finish and close the browser.)"
            )
            if not user_choice:
                print("[INFO] User chose NOT to create a new step. Breaking loop.")
                break

            print("[INFO] User wants to create a new step.")
            # Create new step, using the same driver so user can select elements
            create_new_step_flow(chosen_form['id_uuid'], driver)

    finally:
        # 8) Close the browser after the user is truly done
        print("[DEBUG] Closing the browser after user is done.")
        close_browser(driver)

    print("[DEBUG] main_controller.py finished.")

if __name__ == "__main__":
    main()
