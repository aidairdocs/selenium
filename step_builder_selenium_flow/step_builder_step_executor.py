import time
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import messagebox

from steps_shared_actions import handle_unknown_action
from steps_shared_actions.alert_handler import handle_unexpected_alerts
from steps_shared_utils.wait_helpers import wait_for_page_ready
from steps_shared_utils.steps_shared_actions_registry import ACTION_HANDLERS

# Import adaptive wait functionality and configuration retrieval
from steps_shared_utils.adaptive_wait import adaptive_wait_for_action
from steps_shared_utils.step_wait_config import get_step_config

def prompt_for_recovery(step):
    """
    Displays a TK window showing details of the failed step and asks the user:
    "Do you want to update the element or delete the step and create a new one?"
    It shows the step's description (form_steps::description) and selector_title,
    and provides two buttons:
      - "Update Element"
      - "Delete and Create New Step"
      
    Returns:
      "update" if the user chooses to update the element,
      "replace" if the user chooses to delete and create a new step.
    """
    root = tk.Tk()
    root.title("Step Execution Failed")
    root.geometry("500x300")
    root.resizable(False, False)

    # Extract details from the failed step
    step_number = step.get("step_number", "Unknown")
    description = step.get("description", "No description provided")
    selector_title = step.get("selector_title", "No selector title provided")

    message = (
        f"Step #{step_number} has failed.\n\n"
        f"Description: {description}\n"
        f"Selector Title: {selector_title}\n\n"
        "Choose one of the following options:"
    )

    label = tk.Label(root, text=message, padx=20, pady=20, justify=tk.LEFT)
    label.pack()

    # Variable to store the user's choice
    user_choice = tk.StringVar(value="")

    def update_element():
        user_choice.set("update")
        root.destroy()

    def replace_step():
        user_choice.set("replace")
        root.destroy()

    # Create a frame for the buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    btn_update = tk.Button(button_frame, text="Update Element", command=update_element, width=20)
    btn_update.pack(side=tk.LEFT, padx=10)

    btn_replace = tk.Button(button_frame, text="Delete and Create New Step", command=replace_step, width=25)
    btn_replace.pack(side=tk.LEFT, padx=10)

    root.mainloop()
    return user_choice.get()

def delete_failed_step(step_id):
    """
    Delete the failed step from the database.
    (You must implement delete_step_by_id in your repository.)
    """
    try:
        from step_builder_repositories.step_builder_form_steps_repository import delete_step_by_id
        delete_step_by_id(step_id)
        print(f"[DEBUG] Step with id {step_id} deleted successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to delete step with id {step_id}: {e}")

def update_element_for_failed_step(step, driver):
    """
    Prompt the user to reselect the element for the failed step and update the step's record.
    (You must implement update_step_element_flow in your step creation flow.)
    """
    try:
        from step_builder_selenium_flow.step_builder_create_new_step_flow import update_step_element_flow
        update_step_element_flow(step, driver)
        print(f"[DEBUG] Step with id {step.get('id_uuid')} updated successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to update step with id {step.get('id_uuid')}: {e}")

def run_steps(steps_data, driver, start_step=1, form_id=None, form_name=None):
    """
    run_steps(steps_data, driver, start_step=1, form_id=None, form_name=None)

    Iterates over steps_data["steps"], calling the corresponding action function
    on each step. If a step fails to execute, it prompts the user to either replace the step
    (delete and create a new one in the same location) or update the element selection for the failed step.
    """
    print(f"[DEBUG] run_steps: Called with existing driver and start_step={start_step}.")

    steps_list = steps_data.get("steps", [])
    if not steps_list:
        print("[INFO] No steps to execute.")
        return

    for step in steps_list:
        try:
            

            step_number = step.get("step_number", 1)
            if step_number < start_step:
                continue

            # Wait for page ready
            wait_for_page_ready(driver, timeout=10, spinner_css="#loadingOverlay", check_jquery=True)

            action_name = step.get("action")
            selector_type = (step.get("selector_type") or "xpath").lower()
            selector_value = step.get("selector_value", "")
            step_value = step.get("value", "")
            step_id = step.get("id_uuid")  # Unique identifier for this step

            print(f"[DEBUG] Step #{step_number}: Action='{action_name}', Selector='{selector_value}', Value='{step_value}'")

            # Check for alerts before the action
            handle_unexpected_alerts(driver, action="dismiss")

            # Adaptive wait if step has a unique id
            if step_id:
                if form_id and step_id and action_name:
                    existing_config = get_step_config(form_id, step_id, action_name, default_wait=7.0)
                    new_max_wait = existing_config.get("ema", 7.0)
                else:
                    new_max_wait = 7.0

                def test_action(drv):
                    try:
                        if selector_type == "xpath":
                            elem = drv.find_element(By.XPATH, selector_value)
                        else:
                            elem = drv.find_element(By.CSS_SELECTOR, selector_value)
                        return elem.is_displayed() and elem.is_enabled()
                    except Exception:
                        return False

                measured_wait = adaptive_wait_for_action(
                    driver,
                    action_test_fn=test_action,
                    max_wait=new_max_wait,
                    poll_interval=0.5,
                    step_id=step_id,
                    action_type=action_name,
                    form_id=form_id,
                    form_name=form_name
                )
                print(f"[DEBUG] Adaptive wait measured {measured_wait:.2f}s for step_id '{step_id}' and action '{action_name}'.")

            # Dispatch the action
            action_func = ACTION_HANDLERS.get(action_name, handle_unknown_action)
            action_func(driver, selector_type, selector_value, step_value, step)

            # Post-action: brief pause and check alerts
            time.sleep(1)
            handle_unexpected_alerts(driver, action="dismiss")
            time.sleep(1)

        except Exception as e:
            print(f"[ERROR] Step execution failed for step #{step.get('step_number')} (id: {step.get('id_uuid')}) with error: {e}")
            recovery_choice = prompt_for_recovery(step)
            if recovery_choice == "replace":
                delete_failed_step(step.get("id_uuid"))
                from step_builder_selenium_flow.step_builder_create_new_step_flow import create_new_step_flow
                # Create new step at the same step order
                create_new_step_flow(form_id, driver, step_order=step.get("step_number"))
            elif recovery_choice == "update":
                update_element_for_failed_step(step, driver)
            else:
                print("[INFO] No recovery option chosen; skipping the step.")

    print("[INFO] All steps completed successfully.")
