# E:\CRM\automation_project\steps_shared_actions\force_date_injection_action.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from steps_shared_utils.parse_ymd import parse_ymd
from steps_shared_actions.alert_handler import handle_unexpected_alerts

def force_date_injection_action(driver, selector_type, selector_value, step_value, step):
    """
    force_date_injection_action(driver, selector_type, selector_value, step_value, step)

    1) The site expects dd/MM/yyyy format, but we receive "YYYY-MM-DD" from step_value,
       so we parse & reformat.
    2) We forcibly remove `readonly` from the <input> and set .value with JavaScript.
    3) We dispatch `input` & `change` events so Angular updates its model.
    4) This bypasses the datepicker UI entirely.

    Warnings:
    - This only works if the field truly accepts typed text once `readonly` is removed.
    - If the site strictly requires datepicker usage, it may ignore or reset the field later.
    - Use with caution.
    """
    print("[DEBUG] force_date_injection_action started.")
    handle_unexpected_alerts(driver)  # in case an alert is blocking

    # 1) Parse the "YYYY-MM-DD" => (yyyy, mm, dd)
    yyyy, mm, dd = parse_ymd(step_value)
    # 2) Reformat => "dd/MM/yyyy"
    #   e.g. 2024-06-23 => "23/06/2024"
    dd_str = f"{dd:02d}"
    mm_str = f"{mm:02d}"
    formatted_str = f"{dd_str}/{mm_str}/{yyyy}"
    print(f"[DEBUG] Reformat {step_value} => '{formatted_str}'")

    # 3) Locate the <input> via selector_type/selector_value
    input_el = _find_element_safely(driver, selector_type, selector_value)
    if not input_el:
        print("[ERROR] Could not locate the date <input> for force injection.")
        return

    # 4) Use JavaScript to remove readOnly, set .value, dispatch events
    js_script = """
        arguments[0].readOnly = false; 
        arguments[0].removeAttribute('readonly'); 
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """
    driver.execute_script(js_script, input_el, formatted_str)
    print(f"[DEBUG] Force-injected '{formatted_str}' into the date field, triggered Angular events.")

    # 5) Optionally wait a bit so the site can react
    time.sleep(1)

    print("[DEBUG] force_date_injection_action done.")


def _find_element_safely(driver: WebDriver, sel_type: str, sel_value: str):
    """
    Helper to locate element by (selector_type, selector_value).
    """
    try:
        if not sel_value:
            print("[WARNING] No selector_value provided. Doing nothing.")
            return None

        sel_type = sel_type.lower()
        if sel_type == 'xpath':
            return driver.find_element(By.XPATH, sel_value)
        elif sel_type == 'css':
            return driver.find_element(By.CSS_SELECTOR, sel_value)
        else:
            print(f"[ERROR] Unsupported selector_type '{sel_type}'. Use 'xpath' or 'css'.")
            return None
    except NoSuchElementException as e:
        print(f"[ERROR] Element not found: {e}")
        return None
