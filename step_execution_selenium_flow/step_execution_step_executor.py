# E:\CRM\automation_project\step_execution_selenium_flow\step_execution_step_executor.py

import time
from selenium.webdriver.common.by import By
import os
import json


# Example imports for your action functions
from steps_shared_actions import handle_unknown_action
from steps_shared_actions.alert_handler import handle_unexpected_alerts
from steps_shared_utils.steps_shared_actions_registry import ACTION_HANDLERS
from steps_shared_utils.steps_shared_conditions_registry import CONDITION_EXPRESSIONS

# Import the adaptive wait function
from steps_shared_utils.adaptive_wait import adaptive_wait_for_action

def evaluate_condition(expr_key, condition_context):
    """
    Evaluates the condition for a step using the provided condition_context.
    Logs detailed debug information to a file only if a condition is present,
    otherwise prints a minimal debug message.
    
    If expr_key is a string that looks like a JSON list, it will parse it.
    """
    debug_lines = []
    debug_lines.append("=== FULL DEBUG START ===")
    debug_lines.append("Timestamp: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    debug_lines.append("Received expr_key (type: {}): {}".format(type(expr_key), expr_key))
    debug_lines.append("Received condition_context (type: {}):".format(type(condition_context)))
    debug_lines.append(json.dumps(condition_context, indent=2))
    
    # If no condition is provided, log minimal info to console and return True.
    if not expr_key:
        print("\n".join(debug_lines))
        print("No condition provided. Returning True.")
        return True

    # Try to parse if expr_key is a string that represents a list.
    if isinstance(expr_key, str):
        expr_key_stripped = expr_key.strip()
        if expr_key_stripped.startswith('[') and expr_key_stripped.endswith(']'):
            try:
                parsed = json.loads(expr_key_stripped)
                debug_lines.append("Parsed expr_key into list: {}".format(parsed))
                expr_key = parsed
            except Exception as e:
                debug_lines.append("[WARNING] Could not parse expr_key as a list: {}".format(e))
    
    # If a list of conditions is provided, evaluate all (logical AND).
    if isinstance(expr_key, list):
        debug_lines.append("Condition is a list. Evaluating each condition (logical AND).")
        for key in expr_key:
            if not isinstance(key, str) or not key.strip():
                debug_lines.append("Skipping invalid condition key: {}".format(key))
                continue
            expr_code = CONDITION_EXPRESSIONS.get(key, "")
            debug_lines.append("Evaluating key: '{}' -> Expression: '{}'".format(key, expr_code))
            if not expr_code:
                debug_lines.append("[WARNING] Condition key '{}' not found in registry. Returning False.".format(key))
                write_and_open_debug_con(debug_lines)
                return False
            local_vars = dict(condition_context)
            try:
                result = bool(eval(expr_code, {"__builtins__": {}}, local_vars))
                debug_lines.append("Result of '{}' with context {}: {}".format(expr_code, local_vars, result))
                if not result:
                    debug_lines.append("One condition evaluated to False. Returning False.")
                    write_and_open_debug_con(debug_lines)
                    return False
            except Exception as e:
                debug_lines.append("[WARNING] Could not eval condition '{}' from key '{}': {}".format(expr_code, key, e))
                write_and_open_debug_con(debug_lines)
                return False
        debug_lines.append("All conditions in the list evaluated to True. Returning True.")
        write_and_open_debug_con(debug_lines)
        return True

    # Otherwise, if a single string condition is provided.
    if not isinstance(expr_key, str) or not expr_key.strip():
        print("expr_key is not a valid non-empty string. Returning True.")
        return True

    expr_code = CONDITION_EXPRESSIONS.get(expr_key, "")
    debug_lines.append("Single condition. Key: '{}' -> Expression: '{}'".format(expr_key, expr_code))
    if not expr_code:
        debug_lines.append("[WARNING] Condition key '{}' not found in registry. Returning False.".format(expr_key))
        write_and_open_debug_con(debug_lines)
        return False

    local_vars = dict(condition_context)
    try:
        result = bool(eval(expr_code, {"__builtins__": {}}, local_vars))
        debug_lines.append("Result of '{}' with context {}: {}".format(expr_code, local_vars, result))
        write_and_open_debug_con(debug_lines)
        return result
    except Exception as e:
        debug_lines.append("[WARNING] Could not eval condition '{}' from key '{}': {}".format(expr_code, expr_key, e))
        write_and_open_debug_con(debug_lines)
        return False

def write_and_open_debug_con(lines):
    """
    Writes the provided debug lines to 'evaluate_condition_debug.txt' and opens it automatically.
    This function is only called if a condition is being evaluated.
    """
    debug_file = os.path.join(os.path.dirname(__file__), "evaluate_condition_debug.txt")
    try:
        with open(debug_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        os.startfile(debug_file)
    except Exception as e:
        print(f"[ERROR] Could not write or open debug file: {e}")



def write_and_open_debug(lines, filename="run_steps_crm_format_debug.txt"):
    """
    Writes the provided debug lines to a file and opens it automatically.
    """
    debug_file = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(debug_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        # Automatically open the file (works on Windows)
        os.startfile(debug_file)
    except Exception as e:
        print(f"[ERROR] Could not write or open debug file: {e}")

def run_steps_crm_format(steps_data, driver, start_step=1, condition_context=None):
    """
    run_steps_crm_format(steps_data, driver, start_step=1, condition_context=None)

    Iterates over steps_data["steps"], each having DB-style fields:
      - step_order        (int)
      - action_type       (str)
      - selector_type     (str)
      - selector_value    (str)
      - client_value / insert_value  (str)
      - condition         (str)  <-- new for conditional logic
      - id_uuid           (str)  <-- unique identifier for the step
    """
    if condition_context is None:
        condition_context = {}



    # Build debug output for all received data
    debug_lines = []
    debug_lines.append("=== run_steps_crm_format DEBUG START ===")
    debug_lines.append("Timestamp: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    debug_lines.append("Received steps_data:")
    debug_lines.append(json.dumps(steps_data, indent=2))
    debug_lines.append("Received condition_context:")
    debug_lines.append(json.dumps(condition_context, indent=2))
    write_and_open_debug(debug_lines)


    print(f"[DEBUG] run_steps_crm_format() called with {len(steps_data.get('steps', []))} steps.")

    steps_list = steps_data.get("steps", [])
    if not steps_list:
        print("[INFO] No steps to execute.")
        return

    try:
        for step in steps_list:
            step_number = step.get("step_order", 1)
            if step_number < start_step:
                continue

            # Evaluate condition if present
            condition = step.get("condition", "")
            condition_result = evaluate_condition(condition, condition_context)
            if not condition_result:
                print(f"[DEBUG] Skipping step #{step_number} due to condition='{condition}'")
                continue

            # Get action information
            action_name = step.get("action_type", None)
            if not action_name:
                print(f"[WARNING] Step #{step_number} has no action_type. Skipping.")
                continue

            # Convert selector_type to lower-case if it exists; default to 'xpath'
            selector_type = (step.get("selector_type") or "xpath").lower()
            selector_value = step.get("selector_value", "")

            # Determine the value for typing or visiting a URL
            step_value = step.get("client_value") or step.get("insert_value") or ""
            step_id = step.get("id_uuid")  # Unique identifier for this step

            print(f"[DEBUG] Step #{step_number}: "
                  f"Action='{action_name}', Selector='{selector_value}', Value='{step_value}', "
                  f"Condition='{condition}' => PASSED.")

            # (1) Check for any leftover/unexpected alerts BEFORE the step
            handle_unexpected_alerts(driver, action="dismiss")

            # (2) Adaptive wait: if the step has a unique id, try to wait until the target element is available.
            # Define a test function to check for element presence and basic clickability.
            if step_id:
                def test_action(drv):
                    try:
                        if selector_type == "xpath":
                            elem = drv.find_element(By.XPATH, selector_value)
                        else:
                            elem = drv.find_element(By.CSS_SELECTOR, selector_value)
                        # Basic test: element is displayed and enabled.
                        return elem.is_displayed() and elem.is_enabled()
                    except Exception as ex:
                        return False

                measured_wait = adaptive_wait_for_action(
                    driver,
                    action_test_fn=test_action,
                    max_wait=5.0,       # Maximum wait time (adjust as needed)
                    poll_interval=0.5,  # Poll every 0.5 seconds
                    step_id=step_id,
                    action_type=action_name
                )
                print(f"[DEBUG] Adaptive wait measured {measured_wait:.2f}s for step_id '{step_id}' and action '{action_name}'.")

            # (3) Dispatch to the appropriate action function
            action_func = ACTION_HANDLERS.get(action_name, handle_unknown_action)
            action_func(driver, selector_type, selector_value, step_value, step)

            # (4) Optional small delay after the action
            time.sleep(1)

            # (5) Check again for alerts triggered BY the step
            handle_unexpected_alerts(driver, action="dismiss")

            # (6) Another small delay if desired
            time.sleep(1)

        print("[INFO] All steps completed successfully.")

    except Exception as e:
        print(f"[ERROR] An error occurred during step execution: {e}")

