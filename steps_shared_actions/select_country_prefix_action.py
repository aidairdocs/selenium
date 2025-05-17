# E:\CRM\automation_project\steps_shared_actions\select_country_prefix_action.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from steps_shared_utils.element_utils import find_element


def select_country_prefix_action(driver, selector_type, selector_value, step_value, step):
    """
    select_country_prefix_action(...)

    This action selects a country prefix (like "Israel") from an intl-tel-input style
    phone dropdown. The typical process:

    1) Find and click the `.selected-flag` element to open the .country-list.
    2) Wait for the list to be visible.
    3) Search the <li> items for one that contains the text e.g. "Israel".
    4) Click that item.

    'step_value' is the country name to match (e.g. "Israel").
    'selector_type/selector_value' should locate the .selected-flag container.
    """
    print("[DEBUG] select_country_prefix_action started.")
    country_name = step_value.strip()
    if not country_name:
        print("[ERROR] No country name provided in step_value. Doing nothing.")
        return

    # 1) Locate .selected-flag
    selected_flag_el = find_element(driver, selector_type, selector_value)
    if not selected_flag_el:
        print("[ERROR] Could not locate .selected-flag element. Exiting action.")
        return

    # 2) Click .selected-flag to open the list
    selected_flag_el.click()
    print("[DEBUG] Clicked the .selected-flag element, expecting the country list to appear.")

    # 3) Wait for the .country-list to become visible
    #    We assume the .country-list is a sibling or in the same container
    #    Often the 'ul.country-list' is next sibling. Adjust as needed.
    try:
        country_list_el = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.country-list:not(.hide)"))
        )
        print("[DEBUG] Found visible country list.")
    except Exception as e:
        print(f"[ERROR] Timed out waiting for country list to appear: {e}")
        return

    # 4) Find the <li> item that contains the user-provided country name
    li_items = country_list_el.find_elements(By.CSS_SELECTOR, "li.country")
    match_li = None
    for li in li_items:
        li_text = li.text.strip()
        # Check if the user provided name is in li_text
        if country_name.lower() in li_text.lower():
            match_li = li
            break

    if match_li:
        print(f"[DEBUG] Found matching country: {match_li.text}")
        match_li.click()
        print("[DEBUG] Clicked the matching country <li>.")
    else:
        print(f"[ERROR] Could not find any <li> containing '{country_name}'.")
        # optionally raise an exception or do something else

    print("[DEBUG] select_country_prefix_action done.")

