# E:\CRM\automation_project\steps_shared_actions\enter_day_action.py

import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementNotInteractableException, WebDriverException, NoSuchElementException
from steps_shared_utils.parse_ymd import parse_ymd
from steps_shared_utils.element_utils import find_element
from steps_shared_actions.alert_handler import handle_unexpected_alerts

def enter_day_action(driver, selector_type, selector_value, step_value, step):
    """
    enter_day_action(driver, selector_type, selector_value, step_value, step)

    Expects step_value in "YYYY-MM-DD". We'll parse it and pick only the day (DD).
    If it's a <select>, we do select_by_visible_text. 
    If it's an <input>, we do clear() + send_keys().
    """
    print("[DEBUG] enter_day_action started.")
    yyyy, mm, dd = parse_ymd(step_value)
    day_str = f"{dd:02d}"

    # 1) find the element
    element = find_element(driver, selector_type, selector_value)

    handle_unexpected_alerts(driver, action="dismiss")

    tag_name = element.tag_name.lower()
    if tag_name == "select":
        _select_dropdown_day(driver, element, day_str)
    else:
        _enter_text_day(driver, element, day_str)

    print("[DEBUG] enter_day_action done.")


# def _select_dropdown_day(driver, select_element, day_str):
#     from selenium.webdriver.support.ui import Select
#     from selenium.common.exceptions import NoSuchElementException

#     try:
#         select_element.click()
#         handle_unexpected_alerts(driver, action="accept")

#         select_obj = Select(select_element)
#         try:
#             select_obj.select_by_visible_text(day_str)
#             print(f"[DEBUG] Selected day '{day_str}' in dropdown (exact).")
#         except NoSuchElementException:
#             # fallback approach
#             found_match = None
#             for option in select_obj.options:
#                 opt_text = option.text.strip()
#                 if opt_text.lower() == day_str.lower():
#                     found_match = opt_text
#                     break
#             if found_match:
#                 select_obj.select_by_visible_text(found_match)
#                 print(f"[DEBUG] Found fallback day match '{found_match}'.")
#             else:
#                 raise Exception(f"No matching day found for '{day_str}' in dropdown.")
#         handle_unexpected_alerts(driver, action="accept")
#     except Exception as e:
#         print(f"[ERROR] Could not select day in <select>: {e}")
#         raise

def _select_dropdown_day(driver, select_element, day_str):
    from selenium.webdriver.support.ui import Select
    from selenium.common.exceptions import NoSuchElementException

    try:
        select_element.click()
        handle_unexpected_alerts(driver, action="accept")

        select_obj = Select(select_element)
        try:
            # First, try selecting using the padded day_str (e.g., "01")
            select_obj.select_by_visible_text(day_str)
            print(f"[DEBUG] Selected day '{day_str}' in dropdown (exact match).")
            return
        except NoSuchElementException:
            # Fallback: Try selecting using the day without leading zero
            day_without_zero = str(int(day_str))  # converts "01" to "1"
            try:
                select_obj.select_by_visible_text(day_without_zero)
                print(f"[DEBUG] Selected day '{day_without_zero}' in dropdown (fallback without leading zero).")
                return
            except NoSuchElementException:
                # If still not found, iterate over options as a final fallback
                found_match = None
                for option in select_obj.options:
                    opt_text = option.text.strip()
                    if opt_text.lower() == day_str.lower() or opt_text.lower() == day_without_zero.lower():
                        found_match = opt_text
                        break
                if found_match:
                    select_obj.select_by_visible_text(found_match)
                    print(f"[DEBUG] Found fallback day match '{found_match}'.")
                else:
                    raise Exception(f"No matching day found for '{day_str}' in dropdown.")
        handle_unexpected_alerts(driver, action="accept")
    except Exception as e:
        print(f"[ERROR] Could not select day in <select>: {e}")
        raise



def _enter_text_day(driver, element, day_str):
    try:
        element.click()
        alert_found = handle_unexpected_alerts(driver, action="dismiss")
        if alert_found:
            element.click()

        element.clear()
        element.send_keys(day_str)
        handle_unexpected_alerts(driver, action="dismiss")

        print(f"[DEBUG] Typed day_str='{day_str}' into text field.")
    except Exception as e:
        print(f"[ERROR] Could not enter day into text field: {e}")
        raise
