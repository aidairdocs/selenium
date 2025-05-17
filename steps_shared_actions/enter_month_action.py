# E:\CRM\automation_project\steps_shared_actions\enter_month_action.py

import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementNotInteractableException, WebDriverException, NoSuchElementException
from steps_shared_utils.parse_ymd import parse_ymd
from steps_shared_utils.element_utils import find_element
from steps_shared_actions.alert_handler import handle_unexpected_alerts
from steps_shared_utils.wait_helpers import click_with_retry, wait_for_overlay_disappear  # type: ignore


MONTH_NAMES = {
    1: "January",   2: "February", 3: "March",     4: "April",
    5: "May",       6: "June",     7: "July",      8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}

def enter_month_action(driver, selector_type, selector_value, step_value, step):
    """
    enter_month_action(driver, selector_type, selector_value, step_value, step)

    1) parse "YYYY-MM-DD" => (yyyy, mm, dd)
    2) figure out how to represent the month:
       - if step["month_format"] == "words", we use "January", etc.
       - otherwise "10" for October, etc.
    3) if element is <select>, we do select_by_visible_text(...), but 
       also fallback to spelled-out months if numeric fails.
    4) if element is <input>, we do clear() + send_keys().
    """
    print("[DEBUG] enter_month_action started.")

    yyyy, mm, dd = parse_ymd(step_value)
    month_format = step.get("month_format", "leading_zero").lower()

    # Build the primary string for the month (the user-intended format)
    if month_format == "words":
        month_str = MONTH_NAMES.get(mm, f"{mm:02d}")
    else:
        # e.g. '03' for March
        month_str = f"{mm:02d}"

    print(f"[DEBUG] Determined month_str='{month_str}' from step_value='{step_value}' using format='{month_format}'")

    # 1) find the element
    element = find_element(driver, selector_type, selector_value)

    # 2) dismiss leftover alerts
    handle_unexpected_alerts(driver, action="dismiss")

    tag_name = element.tag_name.lower()
    if tag_name == "select":
        # use the <select> approach
        _select_dropdown_month(driver, element, month_str, mm)
    else:
        # fallback to text approach
        _enter_text_month(driver, element, month_str)

    print("[DEBUG] enter_month_action done.")


def _select_dropdown_month(driver, select_element, month_str, mm_numeric):
    """
    If the field is <select>, we do a select_by_visible_text approach.
    We'll attempt multiple fallbacks:
      1) direct: month_str (e.g. '10' or '03' or 'January')
      2) partial/fuzzy if that fails
      3) if numeric fails, we try spelled-out month from MONTH_NAMES[mm_numeric]
    """
    from selenium.webdriver.support.ui import Select
    from selenium.common.exceptions import NoSuchElementException

    spelled_out_month = MONTH_NAMES.get(mm_numeric, month_str)  # e.g. 'October' if mm_numeric=10

    try:
        # 1) click/focus
        # Possibly wait for an overlay to vanish first
        wait_for_overlay_disappear(driver, overlay_id="overlay-background", timeout=10)

        # Then attempt to click the <select> with retries
        click_with_retry(driver, select_element, max_retries=5, delay=1.0)
        # 2) accept any alert
        handle_unexpected_alerts(driver, action="accept")

        select_obj = Select(select_element)

        # Attempt #1: direct exact match for month_str
        try:
            select_obj.select_by_visible_text(month_str)
            print(f"[DEBUG] Chosen month '{month_str}' in dropdown (exact).")
        except NoSuchElementException:
            print(f"[WARNING] No exact match for '{month_str}' in <select>. Trying fallback approach...")

            # Attempt #2: partial or case-insensitive exact
            found_match = _try_fuzzy_match(select_obj, month_str)
            if not found_match:
                print(f"[WARNING] Could not match '{month_str}'. Trying spelled-out fallback '{spelled_out_month}'...")
                # Attempt #3: spelled-out fallback (e.g. "October")
                # This might succeed if the dropdown has "October" but our '10' was not found
                try:
                    select_obj.select_by_visible_text(spelled_out_month)
                    print(f"[DEBUG] Found spelled-out month '{spelled_out_month}' after fallback.")
                    found_match = spelled_out_month
                except NoSuchElementException:
                    print(f"[WARNING] No exact match for spelled-out month '{spelled_out_month}'. Trying partial on that...")

                    # Attempt #4: partial/fuzzy on spelled-out month
                    found_match = _try_fuzzy_match(select_obj, spelled_out_month)

            if not found_match:
                raise Exception(f"No matching month found for '{month_str}' or '{spelled_out_month}' in dropdown.")
            else:
                print(f"[DEBUG] Found match '{found_match}' after fallback.")

        handle_unexpected_alerts(driver, action="accept")
    except Exception as e:
        print(f"[ERROR] Could not select month in <select>: {e}")
        raise


def _try_fuzzy_match(select_obj, desired_str):
    """
    Attempts a case-insensitive exact match or partial substring match
    in the <option> text for 'desired_str'.
    If found, do select_by_visible_text(...) and return the matched text.
    If not found, return None.
    """
    user_lower = desired_str.strip().lower()
    for option in select_obj.options:
        opt_text = option.text.strip()
        if opt_text.lower() == user_lower:
            # Perfect case-insensitive match
            select_obj.select_by_visible_text(opt_text)
            return opt_text
        # or partial substring check
        if user_lower in opt_text.lower():
            select_obj.select_by_visible_text(opt_text)
            return opt_text
    return None


def _enter_text_month(driver, element, month_str):
    """
    For an <input> or text-based field, we do the standard clear + send_keys approach.
    """
    try:
        element.click()
        alert_found = handle_unexpected_alerts(driver, action="dismiss")
        if alert_found:
            element.click()

        element.clear()
        element.send_keys(month_str)
        handle_unexpected_alerts(driver, action="dismiss")

        print(f"[DEBUG] Typed month_str='{month_str}' into text field.")
    except Exception as e:
        print(f"[ERROR] Could not enter month into text field: {e}")
        raise
