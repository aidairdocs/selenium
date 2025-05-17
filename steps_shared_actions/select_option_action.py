# E:\CRM\automation_project\steps_shared_actions\select_option_action.py

import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from steps_shared_utils.element_utils import find_element
from steps_shared_actions.alert_handler import handle_unexpected_alerts

def select_option_action(driver, selector_type, selector_value, step_value, step):
    """
    Attempts to select an <option> by visible text in a <select> element.
    Retries if an alert appears blocking the click/focus.

    Updated to always accept alerts (OK), so the selection is never cancelled.
    """
    print("[DEBUG] select_option_action() called (robust version).")

    max_retries = 2
    attempt = 0

    while attempt < max_retries:
        attempt += 1
        try:
            # STEP A: Find the <select> element
            element = find_element(driver, selector_type, selector_value)

            # Optional: click/focus it first, in case that triggers an alert
            element.click()

            # STEP B: Check if an alert popped up immediately, always accept
            alert_found = handle_unexpected_alerts(driver, action="accept")
            if alert_found:
                print("[DEBUG] Retrying <select> click after accepting alert.")
                element = find_element(driver, selector_type, selector_value)
                element.click()

            # STEP C: Do the actual selection logic
            select = Select(element)

            # 1) Attempt exact match
            try:
                select.select_by_visible_text(step_value)
                print(f"[DEBUG] Selected option '{step_value}' (exact match).")
                # Check for post-selection alert, always accept
                handle_unexpected_alerts(driver, action="accept")
                return  # success
            except Exception:
                print(f"[WARNING] Exact match not found for '{step_value}'. Trying fallback approaches...")

            # 2) Case-insensitive exact match
            user_input_lower = step_value.strip().lower()
            matched_text = None
            for opt in select.options:
                if opt.text.strip().lower() == user_input_lower:
                    matched_text = opt.text.strip()
                    break

            if matched_text:
                select.select_by_visible_text(matched_text)
                print(f"[DEBUG] Selected option '{matched_text}' (case-insensitive match).")
                handle_unexpected_alerts(driver, action="accept")
                return

            # 3) Title-case fallback
            title_case_value = step_value.strip().title()
            if title_case_value != step_value:
                print(f"[INFO] Trying title-case fallback: '{title_case_value}'")
                try:
                    select.select_by_visible_text(title_case_value)
                    print(f"[DEBUG] Selected option '{title_case_value}' (title-case fallback).")
                    handle_unexpected_alerts(driver, action="accept")
                    return
                except Exception:
                    pass

            # 4) Partial substring match (case-insensitive)
            partial_match = None
            for opt in select.options:
                opt_text_lower = opt.text.strip().lower()
                if user_input_lower in opt_text_lower:
                    partial_match = opt.text.strip()
                    break

            if partial_match:
                select.select_by_visible_text(partial_match)
                print(f"[DEBUG] Selected option '{partial_match}' (substring match).")
                handle_unexpected_alerts(driver, action="accept")
                return

            # 5) No match found with any approach
            msg = f"No matching option found for '{step_value}' in <select> (all attempts)."
            print(f"[ERROR] {msg}")
            raise Exception(msg)

        except (NoSuchElementException, WebDriverException) as e:
            print(f"[WARNING] Attempt #{attempt} failed in select_option_action: {e}")
            alert_found = handle_unexpected_alerts(driver, action="accept")

            if attempt >= max_retries and not alert_found:
                raise Exception(f"[ERROR] Could not complete select_option_action after {attempt} attempts. {e}")

        except Exception as e:
            raise e

        # Optional short sleep before retry
        time.sleep(1)

    raise Exception("[ERROR] select_option_action failed after max retries.")
