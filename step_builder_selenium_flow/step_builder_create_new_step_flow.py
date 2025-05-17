# E:\CRM\automation_project\step_builder_selenium_flow\step_builder_create_new_step_flow.py
"""
Provides a flow to interactively create a new step for the given form,
selecting an element first (if needed) and then deciding on the action.

This version will only run the newly created step if the user chooses
"Execute New Step?" at the end, by passing start_step=new_step_order 
to run_steps(...).
"""

import tkinter as tk
from tkinter import messagebox
from step_builder_repositories.step_builder_form_steps_repository import save_new_step, load_form_steps
from step_builder_selenium_flow.step_builder_step_executor import run_steps
from step_builder_selenium_flow.step_builder_create_step_helpers import (
    element_selection_gui,
    element_selection_title_gui,
    prompt_for_value,
    prompt_for_description,
    ask_if_skip_element_selection,
    get_possible_actions_for_element,
    prompt_for_element_action,
    extract_select_options  ### UPDATED: we import the new function here
)
from steps_shared_utils.pick_conditions_gui import pick_conditions_gui


def create_new_step_flow(form_id, driver=None, step_order=None):
    """
    Reordered logic for step creation:
      1) Determine next step_order
      2) Ask if user wants 'goto'/'manual' (no element) or pick an element
      3) If an element is selected, figure out possible actions
      4) (Optional) select a label/title
      5) If the chosen action requires text/URL, prompt for it
      6) Prompt for a description
      7) Save the new step (including element_type)
      8) Optionally re-run all steps now.

    :param form_id: The forms.id_uuid for which we add the step
    :param driver: Selenium WebDriver if we want real-time element selection
    """
    print("[DEBUG] create_new_step_flow() called (element-first approach).")

    # 1) Determine the next step_order
    steps_data = load_form_steps(form_id)
    steps_list = steps_data.get("steps", [])
    if step_order is None:
        if steps_list:
            last_step_order = max(s["step_number"] for s in steps_list)
            new_step_order = last_step_order + 1
        else:
            new_step_order = 1
    else:
        new_step_order = step_order

    # Provide a default so it's always defined
    element_info = {}  # or None if you prefer

    # 2) Ask if user wants to skip element selection (goto/manual) or pick an element
    skip_element = ask_if_skip_element_selection()
    if skip_element == "goto":
        # No element, user just wants 'goto' step
        action_type = "goto"
        selector_value = ""
        selector_type = ""
        selector_title = ""
        element_type = ""  # We set it to empty since no element
        insert_value = prompt_for_value("goto")  # user must provide a URL
        condition_expr_str = ""

    elif skip_element == "manual":
        # 'manual' step also doesn't need an element
        action_type = "manual"
        selector_value = ""
        selector_type = ""
        selector_title = ""
        element_type = ""  # no element
        insert_value = ""  # nothing to enter
        condition_expr_str = ""

    elif skip_element == "click_safe_area":
        # Our new path: no element selection needed
        # We'll do a step that calls the run-time action "click_safe_area"
        action_type = "click_safe_area"
        selector_value = ""
        selector_type = ""
        selector_title = ""
        element_type = ""
        insert_value = ""  # nothing to insert
        condition_expr_str = ""

    elif skip_element == "goto_from_email":
        # Our new path: no element selection needed
        # We'll do a step that calls the run-time action "goto_from_email"
        action_type = "goto_from_email"
        selector_value = ""
        selector_type = ""
        selector_title = ""
        element_type = ""
        insert_value = ""  # nothing to insert
        condition_expr_str = ""

    elif skip_element == "full_screenshot":
        # NEW branch for full page screenshot, no element needed
        action_type = "full_page_screenshot"
        selector_value = ""
        selector_type = ""
        selector_title = ""
        element_type = ""
        # optionally ask for the file path to save
        insert_value = prompt_for_value("Save Screenshot Path (leave blank for default)?")
        condition_expr_str = ""

    elif skip_element == "dismiss_modal":
        # New branch for dismissing a modal; no element selection is required.
        action_type = "dismiss_modal"
        selector_value = ""
        selector_type = ""
        selector_title = ""
        element_type = ""
        insert_value = ""  # No additional value required.
        condition_expr_str = ""

    elif skip_element == "safe_action":
        # New branch for safe action: sensitive manual intervention that uses a checklist.
        action_type = "safe_action"
        selector_value = ""
        selector_type = ""
        selector_title = ""
        element_type = ""
        insert_value = ""
        condition_expr_str = ""

    else:
        # 3) The user wants to pick an element first
        user_confirmed, element_info = element_selection_gui(driver)
        if not user_confirmed or not element_info:
            print("[INFO] User cancelled element selection or no element was chosen.")
            return

        print("[DEBUG] User selected element:", element_info)

        ### UPDATED: If it's a <select>, gather all <option> children now
        extract_select_options(driver, element_info)

        # 3.1) We'll store the basic XPATH for the DB
        selector_value = element_info.get("xpath", "")
        selector_type = "xpath"

        # 3.2) Retrieve element_type from the info. e.g. 'input', 'select'
        element_type = element_info.get("tag_name", "")
        # Instead of just element_info["attributes"], we might store the entire dict
        element_attributes_json = element_info.get("attributes", {})

        # 3.3) Figure out possible actions
        possible_actions = get_possible_actions_for_element(element_info)
        action_type = prompt_for_element_action(possible_actions)
        if not action_type:
            print("[INFO] User cancelled action type after element selection.")
            return
        
        # 4) new step: prompt for condition(s)
        chosen_conditions = pick_conditions_gui()
        # this returns a list of keys: e.g. ["IS_MINOR_TRUE", "HAS_SECOND_PASSPORT"]
        
        # 5) store them in the DB step definition
        if not chosen_conditions:
            condition_expr_str = ""
        else:
            # Approach A: combine them with ' and '
            # condition_expr_str = " and ".join(chosen_conditions)

            # Or Approach B: store as JSON array
            import json
            condition_expr_str = json.dumps(chosen_conditions)


        # 4) (Optional) ask if user wants to select a label near this element
        selector_title = ""
        wants_title = messagebox.askyesno(
            "Select a Title/Label?",
            "Do you want to select a label or text near the element?"
        )
        if wants_title:
            title_confirmed, title_info = element_selection_title_gui(driver)
            if title_confirmed and title_info:
                selector_title = title_info.get("text_content", "")
                print(f"[DEBUG] User selected label text: {selector_title}")
            else:
                print("[DEBUG] No label/title selected or user cancelled.")

        # 5) If the chosen action requires text/URL, prompt user
        insert_value = ""
        if action_type in ("enter_text", "select_option"):
            insert_value = prompt_for_value(action_type)

    # 6) Prompt for a description (applies to all step types)
    description = prompt_for_description()

    
    # 7) Save the new step, now with element_type
    print("[DEBUG] Inserting new step into DB...")
    save_new_step(
        form_id=form_id,
        step_order=new_step_order,
        action_type=action_type,
        selector_value=selector_value,
        selector_type=selector_type,
        insert_value=insert_value,
        description=description,
        selector_title=selector_title,
        element_type=element_type,
        element_attributes=element_info,
        condition=condition_expr_str
    )

    # 8) Ask how the user wants to proceed: stop, from_beginning, or continue
    run_mode = _ask_run_mode_after_new_step(new_step_order)
    if run_mode == "stop":
        print("[DEBUG] User chose to stop. Not re-running steps.")
        return
    elif run_mode == "from_beginning":
        print("[DEBUG] Re-loading steps to run from step #1.")
        updated_steps_data = load_form_steps(form_id)
        run_steps(updated_steps_data, driver=driver, start_step=1)
    elif run_mode == "continue":
        print(f"[DEBUG] Re-loading steps to run from step #{new_step_order}.")
        updated_steps_data = load_form_steps(form_id)
        # We'll call run_steps with start_step=new_step_order
        run_steps(updated_steps_data, driver=driver, start_step=new_step_order)
    else:
        # Just in case
        print("[DEBUG] Unrecognized run_mode. Doing nothing.")

def update_step_element_flow(step, driver):
    """
    Launches the standard element selection chain to allow the user to update the element for a failed step.
    Once the user re-selects and confirms the new element, this function updates the step record in the database.
    
    :param step: The step dictionary (must contain "id_uuid")
    :param driver: The active Selenium WebDriver instance.
    :return: True if the update was successful, False otherwise.
    """
    print(f"[DEBUG update_step_element_flow] Starting update for step id {step.get('id_uuid')}.")
    
    # Import element selection utilities
    from step_builder_selenium_flow.step_builder_create_step_helpers import element_selection_gui, confirm_element_selection
    # Launch the element selection GUI for the user to re-select the element.
    user_confirmed, new_element_info = element_selection_gui(driver)
    if not user_confirmed or not new_element_info:
        print("[INFO update_step_element_flow] User cancelled element selection.")
        return False

    # Show a confirmation window for the new element.
    if not confirm_element_selection(new_element_info):
        print("[INFO update_step_element_flow] User cancelled element confirmation.")
        return False

    # Update the step's element details in the database.
    try:
        from step_builder_repositories.step_builder_form_steps_repository import update_step_element_in_db
        update_step_element_in_db(step.get("id_uuid"), new_element_info)
        print(f"[DEBUG update_step_element_flow] Step element updated successfully in DB for step id {step.get('id_uuid')}.")
        return True
    except Exception as e:
        print(f"[ERROR update_step_element_flow] Failed to update step element in DB for step id {step.get('id_uuid')}: {e}")
        return False




def _ask_run_mode_after_new_step(new_step_order):
    """
    Creates a custom Tkinter window with three options:
      - Stop
      - Run from Beginning
      - Continue (from newly created step_order)

    Returns one of: "stop", "from_beginning", "continue"
    """
    root = tk.Tk()
    root.title("How do you want to continue?")

    label_text = (
        f"New step #{new_step_order} was created.\n\n"
        "How do you want to continue?\n\n"
        "1) Stop: End execution altogether.\n"
        "2) From Beginning: Run from step #1 again.\n"
        "3) Continue: Run from this newly created step.\n"
    )
    label = tk.Label(root, text=label_text, justify=tk.LEFT)
    label.pack(pady=10, padx=10)

    choice_var = tk.StringVar(value="stop")  # default

    def set_run_mode(mode):
        choice_var.set(mode)
        root.destroy()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    # "Stop" button
    stop_btn = tk.Button(btn_frame, text="Stop", width=15, command=lambda: set_run_mode("stop"))
    stop_btn.pack(side=tk.LEFT, padx=5)

    # "Run from Beginning" button
    restart_btn = tk.Button(btn_frame, text="From Beginning", width=15, command=lambda: set_run_mode("from_beginning"))
    restart_btn.pack(side=tk.LEFT, padx=5)

    # "Continue" button
    continue_btn = tk.Button(btn_frame, text="Continue", width=15, command=lambda: set_run_mode("continue"))
    continue_btn.pack(side=tk.LEFT, padx=5)

    root.mainloop()
    return choice_var.get()
