# E:\CRM\automation_project\steps_shared_actions\standard_dd_mm_yyyy.py

import time
from selenium.common.exceptions import ElementNotInteractableException, WebDriverException
from selenium.webdriver.common.keys import Keys  # <-- Import Keys for ESC/Tab
from steps_shared_utils.parse_ymd import parse_ymd
from steps_shared_utils.element_utils import find_element
from steps_shared_actions.alert_handler import handle_unexpected_alerts

def enter_date_dd_mm_yyyy_action(driver, selector_type, selector_value, step_value, step):
    print("[DEBUG] enter_date_dd_mm_yyyy_action started.")

    # 1) Parse "YYYY-MM-DD" into integers
    yyyy, mm, dd = parse_ymd(step_value)
    date_str = f"{dd:02d}/{mm:02d}/{yyyy}"
    print(f"[DEBUG] Converting '{step_value}' => '{date_str}' for the input field.")

    max_retries = 2
    attempt = 0

    while attempt < max_retries:
        attempt += 1
        try:
            element = find_element(driver, selector_type, selector_value)
            element.click()

            alert_found = handle_unexpected_alerts(driver, action="dismiss")
            if alert_found:
                print("[DEBUG] Retrying click after dismissing alert.")
                element = find_element(driver, selector_type, selector_value)
                element.click()

            element.clear()
            element.send_keys(date_str)

            # (A) Press Escape to close datepicker
            time.sleep(0.5)
            element.send_keys(Keys.ESCAPE)
            print("[DEBUG] Sent ESC to close datepicker pop-up (if any).")

            handle_unexpected_alerts(driver, action="dismiss")

            print(f"[DEBUG] Successfully typed date '{date_str}' into element.")
            return

        except (ElementNotInteractableException, WebDriverException) as e:
            print(f"[WARNING] Attempt #{attempt} failed in enter_date_dd_mm_yyyy_action: {e}")
            alert_found = handle_unexpected_alerts(driver, action="dismiss")
            if attempt >= max_retries and not alert_found:
                raise Exception(
                    f"[ERROR] Could not complete enter_date_dd_mm_yyyy_action after {attempt} attempts: {e}"
                )
        except Exception as e:
            # If it's some other logic error, re-raise
            raise e

        time.sleep(1)

    raise Exception("[ERROR] enter_date_dd_mm_yyyy_action failed after max retries.")
