# E:\CRM\automation_project\steps_shared_actions\handle_unknown_action.py

def handle_unknown_action(driver, selector_type, selector_value, step_value, step):
    step_order = step.get("step_order", "?")
    unknown_action = step.get("action_type", "?")
    print(f"[WARNING] Unknown action '{unknown_action}' at step #{step_order}. Doing nothing.")
