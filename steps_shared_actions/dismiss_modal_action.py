# E:\CRM\automation_project\steps_shared_actions/dismiss_modal_action.py

from selenium.webdriver.common.by import By

def dismiss_modal_action(driver, selector_type, selector_value, step_value, step):
    """
    Attempts to dismiss a modal popup by first clicking on its close button.
    If that fails, it tries to remove the modal from the DOM via JavaScript.
    
    Parameters:
      driver        : Selenium WebDriver instance.
      selector_type : Not used here but kept for consistency.
      selector_value: Not used here but kept for consistency.
      step_value    : Not used here.
      step          : The step dictionary (can be used for logging).
    """
    try:
        # Option 1: Try clicking the close button inside the modal.
        # Adjust the CSS selector if needed.
        close_button = driver.find_element(By.CSS_SELECTOR, "div.modal-content button.close")
        close_button.click()
        print("[DEBUG dismiss_modal_action] Modal dismissed by clicking close button.")
    except Exception as e:
        print(f"[WARNING dismiss_modal_action] Failed to click close button: {e}. Trying JavaScript removal.")
        try:
            # Option 2: Remove the modal from the DOM via JavaScript.
            driver.execute_script("var modal = document.querySelector('div.modal-content'); if(modal){ modal.remove(); }")
            print("[DEBUG dismiss_modal_action] Modal removed via JavaScript.")
        except Exception as e_js:
            print(f"[ERROR dismiss_modal_action] Could not remove modal via JavaScript: {e_js}.")
