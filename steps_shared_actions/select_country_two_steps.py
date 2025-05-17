# E:\CRM\automation_project\steps_shared_actions\select_country_two_steps.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def select_country_two_steps(driver, selector_type, selector_value, step_value, step):
    """
    Action: SELECT_COUNTRY_TWO_STEPS
    This action selects a country in a two-step process.
    
    It now supports two types of DOM structures:
    
    1. The original "chosen" widget:
       - The widget is a <ul> element (e.g. with class "chosen-choices").
       - It clicks the widget, waits for an input inside the container,
         enters the country name, waits for an <em> element whose text matches,
         and clicks that result.
    
    2. A new autocomplete input:
       - The target is an <input> field (e.g. with id "autocomplete-applicant-address-country").
       - The code clears the input, sends the country name,
         waits for an <li> element (option) with text matching the country,
         clicks that option, and optionally waits for the input’s value to update.
    
    Parameters:
      driver         : Selenium WebDriver instance.
      selector_type  : "xpath" or "css" used to locate the widget or input.
      selector_value : The selector string for the element.
      step_value     : The country name to be typed (e.g. "ISRAEL" or "GERMANY").
      step           : The step dictionary (for logging/debugging).
    """
    print(f"[DEBUG select_country_two_steps] Called with country '{step_value}'.")

    # Detect new autocomplete input by checking if the selector_value contains a known substring.
    if "autocomplete-applicant-address-country" in selector_value or \
        "mat-input" in selector_value or \
        "mat-mdc-autocomplete-trigger" in input_field.get_attribute("class"):
        # New branch for autocomplete input.
        try:
            if selector_type.lower() == "xpath":
                input_field = driver.find_element(By.XPATH, selector_value)
            else:
                input_field = driver.find_element(By.CSS_SELECTOR, selector_value)
        except Exception as e:
            msg = f"[ERROR select_country_two_steps] Could not locate autocomplete input using {selector_type} '{selector_value}': {e}"
            print(msg)
            raise Exception(msg)
        
        input_field.clear()
        input_field.send_keys(step_value)
        print(f"[DEBUG select_country_two_steps] Entered country name: '{step_value}' in autocomplete input.")

        # Wait for the autocomplete result to appear (support mat-option)
        try:
            # Support both li and mat-option elements
            result = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((
                    By.XPATH, f"//mat-option[contains(normalize-space(.), '{step_value.upper()}')] | //li[normalize-space(text())='{step_value}']"
                ))
            )
            print("[DEBUG select_country_two_steps] Found autocomplete result element matching the country.")
        except Exception as e:
            msg = f"[ERROR select_country_two_steps] Could not find autocomplete result element for '{step_value}': {e}"
            print(msg)
            raise Exception(msg)

        try:
            result.click()
            print("[DEBUG select_country_two_steps] Clicked on the autocomplete result element.")
        except Exception as e:
            msg = f"[ERROR select_country_two_steps] Failed to click the autocomplete result element: {e}"
            print(msg)
            raise Exception(msg)
        
        # Optionally, wait for the input's value to update.
        try:
            WebDriverWait(driver, 5).until(
                lambda d: d.find_element(By.CSS_SELECTOR, selector_value).get_attribute("value").strip().lower() == step_value.lower()
            )
            print("[DEBUG select_country_two_steps] Autocomplete input value updated to the selected country.")
        except Exception as e:
            print(f"[WARNING select_country_two_steps] Timeout waiting for input value update: {e}")
        return


    else:
        # Original branch for the chosen widget (the <ul> element).
        try:
            if selector_type.lower() == "xpath":
                widget = driver.find_element(By.XPATH, selector_value)
            else:
                widget = driver.find_element(By.CSS_SELECTOR, selector_value)
        except Exception as e:
            msg = f"[ERROR select_country_two_steps] Could not locate country widget using {selector_type} '{selector_value}': {e}"
            print(msg)
            raise Exception(msg)
        
        widget.click()
        print("[DEBUG select_country_two_steps] Clicked on the country widget.")

        try:
            # Adjust the CSS selector as needed based on your page's DOM.
            search_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#country_visited_chosen input"))
            )
            print("[DEBUG select_country_two_steps] Search input located.")
        except Exception as e:
            msg = f"[ERROR select_country_two_steps] Search input not found: {e}"
            print(msg)
            raise Exception(msg)

        search_input.clear()
        search_input.send_keys(step_value)
        print(f"[DEBUG select_country_two_steps] Entered country name: '{step_value}'.")

        try:
            result = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f"//em[translate(normalize-space(text()), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='{step_value.lower()}']"))
            )
            print("[DEBUG select_country_two_steps] Found result element matching the country.")
        except Exception as e:
            msg = f"[ERROR select_country_two_steps] Could not find result element for '{step_value}': {e}"
            print(msg)
            raise Exception(msg)

        try:
            result.click()
            print("[DEBUG select_country_two_steps] Clicked on the result element.")
        except Exception as e:
            msg = f"[ERROR select_country_two_steps] Failed to click the result element: {e}"
            print(msg)
            raise Exception(msg)
