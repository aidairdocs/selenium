# E:\CRM\automation_project\steps_shared_actions\enter_year_action.py

import time
from selenium.common.exceptions import ElementNotInteractableException, WebDriverException
from selenium.webdriver.support.ui import Select

from steps_shared_utils.parse_ymd import parse_ymd
from steps_shared_utils.element_utils import find_element
from steps_shared_actions.alert_handler import handle_unexpected_alerts

def enter_year_action(driver, selector_type, selector_value, step_value, step):
    print("[DEBUG] enter_year_action started.")
    yyyy, mm, dd = parse_ymd(step_value)
    year_str = str(yyyy)

    # 1) Locate the <select>
    element = find_element(driver, selector_type, selector_value)
    # 2) Construct a Select object
    select_obj = Select(element)
    # 3) Attempt to select by visible text
    select_obj.select_by_visible_text(year_str)

    print(f"[DEBUG] Selected option '{year_str}' for the year dropdown.")
    print("[DEBUG] enter_year_action done.")


def _enter_split_value(driver, selector_type, selector_value, partial_str):
    """
    Common helper in this file, so each action is truly stand-alone.
    """
    element = find_element(driver, selector_type, selector_value)

    # click or focus
    element.click()
    # handle alert
    alert_found = handle_unexpected_alerts(driver, action="dismiss")
    if alert_found:
        element = find_element(driver, selector_type, selector_value)
        element.click()

    # clear, then type
    element.clear()
    element.send_keys(partial_str)

    # final alert check
    handle_unexpected_alerts(driver, action="dismiss")
