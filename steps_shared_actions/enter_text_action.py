# E:\CRM\automation_project\steps_shared_actions/enter_text_action.py

import time
from selenium.common.exceptions import ElementNotInteractableException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from steps_shared_utils.element_utils import find_element
from steps_shared_actions.alert_handler import handle_unexpected_alerts

def enter_text_action(driver, selector_type, selector_value, step_value, step):
    """
    Finds an element (ideally an <input> or <textarea>) and types 'step_value' into it.
    If the found element is not directly editable (e.g. a container <div>),
    it will attempt to locate a descendant <input> element.
    Retries if an alert appears at the moment of clicking/focusing the field.
    """
    print("[DEBUG] enter_text_action() called (robust version).")

    max_retries = 2
    attempt = 0

    while attempt < max_retries:
        attempt += 1
        try:
            # STEP A: Find the element using the helper.
            element = find_element(driver, selector_type, selector_value)
            if not element:
                raise Exception(f"No element found using {selector_type} '{selector_value}'.")

            # Check if the located element is an input or textarea.
            tag = element.tag_name.lower()
            if tag not in ["input", "textarea"]:
                print(f"[DEBUG] Located element tag is '{tag}', not directly editable. Attempting to find a descendant <input>.")
                try:
                    element = element.find_element(By.TAG_NAME, "input")
                    print("[DEBUG] Found descendant <input> element.")
                except NoSuchElementException:
                    print("[ERROR] No descendant <input> element found within the located element.")
                    raise Exception("Element is not editable and no descendant input was found.")

            # STEP B: Click/focus the element in case the site triggers an alert on focus.
            element.click()

            # STEP C: Check for alert and retry click if needed.
            alert_found = handle_unexpected_alerts(driver, action="dismiss")
            if alert_found:
                print("[DEBUG] Retrying element click after dismissing alert.")
                element = find_element(driver, selector_type, selector_value)
                # Again, check if this element is editable:
                if element.tag_name.lower() not in ["input", "textarea"]:
                    try:
                        element = element.find_element(By.TAG_NAME, "input")
                        print("[DEBUG] Found descendant <input> element on retry.")
                    except NoSuchElementException:
                        print("[ERROR] Retried element is still not editable.")
                        raise Exception("Retried element is not editable.")
                element.click()

            # STEP D: Clear and type the new text.
            element.clear()
            element.send_keys(step_value)
            print(f"[DEBUG] Successfully typed '{step_value}' into element.")

            # STEP E: Check again for any alerts.
            handle_unexpected_alerts(driver, action="dismiss")
            return  # Success, exit the function.

        except (ElementNotInteractableException, WebDriverException) as e:
            print(f"[WARNING] Attempt #{attempt} failed in enter_text_action: {e}")
            # Possibly an alert blocked the action.
            alert_found = handle_unexpected_alerts(driver, action="dismiss")
            time.sleep(1)  # Pause before retrying.
            if attempt >= max_retries and not alert_found:
                raise Exception(f"[ERROR] Could not complete enter_text_action after {attempt} attempts: {e}")
        except Exception as e:
            # Re-raise any other unexpected errors.
            raise e

    # If all attempts fail.
    raise Exception("[ERROR] enter_text_action failed after max retries.")
