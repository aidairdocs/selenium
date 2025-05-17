# E:\CRM\automation_project\steps_shared_actions/force_chosen_value_injection_action.py

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from steps_shared_utils.element_utils import find_element  # Use your unified find_element if desired
from steps_shared_actions.alert_handler import handle_unexpected_alerts

def force_chosen_value_injection_action(driver, selector_type, selector_value, step_value, step):
    """
    force_chosen_value_injection_action(driver, selector_type, selector_value, step_value, step)
    
    This action directly injects the desired value into a custom "chosen" widget.
    
    Workflow:
      1. Locate the widget's container element (e.g. a <ul> with class "chosen-choices").
      2. Construct the final HTML that represents the chosen value (e.g., an <li> element with a specific class).
      3. Use JavaScript injection to set the container's innerHTML to that final HTML.
      4. Optionally, update an underlying hidden input (if present) with the plain value.
      5. Dispatch an event (like 'change') to notify any frameworks (e.g. Angular or jQuery plugins) that the value has changed.
    
    Example:
      If step_value is "ALAND ISLANDS", the action will inject an HTML like:
         <li class="result-selected">ALAND ISLANDS</li>
      into the container.
    
    Note:
      - You may need to adjust the exact HTML structure based on how your widget renders selected options.
      - This method bypasses the normal user interactions (clicking, waiting for dropdowns, etc.).
    """
    print("[DEBUG] force_chosen_value_injection_action started.")
    
    # Dismiss any alerts that might interfere.
    handle_unexpected_alerts(driver)
    
    # Locate the container element (e.g., the <ul> with class "chosen-choices").
    try:
        container = find_element(driver, selector_type, selector_value)
        print("[DEBUG] force_chosen_value_injection_action: Found the widget container.")
    except Exception as e:
        print(f"[ERROR] force_chosen_value_injection_action: Could not locate the widget container: {e}")
        return

    # The desired final value, e.g., "ALAND ISLANDS"
    desired_value = step_value.strip()
    if not desired_value:
        print("[ERROR] force_chosen_value_injection_action: No value provided to inject.")
        return

    # Construct the final HTML to be injected.
    # Adjust the HTML structure as needed for your widget.
    new_html = f'<li class="result-selected">{desired_value}</li>'

    # JavaScript to update the widget:
    js_script = """
        var container = arguments[0];
        var new_html = arguments[1];
        // Replace the container's innerHTML with the new HTML.
        container.innerHTML = new_html;
        // If there is an underlying hidden input within the widget's parent, update its value.
        var hiddenInput = container.parentElement.querySelector("input[type='hidden']");
        if (hiddenInput) {
            // Remove any HTML tags from new_html (if needed).
            hiddenInput.value = new_html.replace(/<[^>]+>/g, '');
        }
        // Dispatch a change event on the container to notify any attached frameworks.
        var event = new Event('change', { bubbles: true });
        container.dispatchEvent(event);
    """
    try:
        driver.execute_script(js_script, container, new_html)
        print(f"[DEBUG] force_chosen_value_injection_action: Injected value '{desired_value}' into the widget.")
    except Exception as e:
        print(f"[ERROR] force_chosen_value_injection_action: Error during JS injection: {e}")
        return

    # Optionally, wait a short time for the widget to update.
    time.sleep(1)
    print("[DEBUG] force_chosen_value_injection_action completed.")
