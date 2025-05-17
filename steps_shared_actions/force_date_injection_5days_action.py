# E:\CRM\automation_project\steps_shared_actions/force_date_injection_5days_action.py

import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from steps_shared_actions.alert_handler import handle_unexpected_alerts
from steps_shared_utils.element_utils import find_element  # use your unified find_element if desired

def force_date_injection_5days_action(driver, selector_type, selector_value, step_value, step):
    """
    force_date_injection_5days_action(driver, selector_type, selector_value, step_value, step)
    
    This action disables the read-only attribute of a date input field and writes a date that is 5 days
    from the current day. It formats the date as dd/MM/yyyy and dispatches input and change events so that
    Angular (or other frameworks) update their models accordingly.
    
    Workflow:
      1. Compute the date 5 days from now.
      2. Format the date as dd/MM/yyyy.
      3. Locate the date input element using the provided selector.
      4. Inject JavaScript to remove the readonly attribute, set the element's value to the computed date,
         and dispatch the input and change events.
      5. Optionally wait a brief moment to allow the page to react.
    
    Example usage:
      action_type = "force_date_injection_5days"
      selector_value might be the dynamic selector saved from element selection,
      and step_value can be ignored (or used as a placeholder).
    """
    print("[DEBUG] force_date_injection_5days_action started.")

    # 1. Calculate the date 5 days from now.
    target_date = datetime.now() + timedelta(days=5)
    # 2. Format the date as dd/MM/yyyy.
    formatted_date = target_date.strftime("%d/%m/%Y")
    print(f"[DEBUG] Calculated target date: {formatted_date}")

    # 3. Locate the date input element.
    try:
        element = find_element(driver, selector_type, selector_value)
        print("[DEBUG] force_date_injection_5days_action: Date input element located.")
    except Exception as e:
        print(f"[ERROR] force_date_injection_5days_action: Could not locate the date input element: {e}")
        return

    # 4. Use JavaScript to remove the readonly attribute, set the value, and dispatch events.
    js_script = """
        // Remove readonly and set the new value
        arguments[0].readOnly = false;
        arguments[0].removeAttribute('readonly');
        arguments[0].value = arguments[1];
        // Dispatch events to notify any frameworks (like Angular)
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """
    try:
        handle_unexpected_alerts(driver)  # In case an alert is blocking
        driver.execute_script(js_script, element, formatted_date)
        print(f"[DEBUG] force_date_injection_5days_action: Force-injected date '{formatted_date}' into the date field.")
    except Exception as e:
        print(f"[ERROR] force_date_injection_5days_action: Error during JS injection: {e}")
        return

    # 5. Optionally wait for the page to process the change.
    time.sleep(1)
    print("[DEBUG] force_date_injection_5days_action completed.")
