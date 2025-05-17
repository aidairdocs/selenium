# Action to select an option from an Angular Material dropdown

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def select_mat_option_action(driver, selector_type, selector_value, step_value, step):
    """Select a mat-option element matching the given text."""
    # Locate and click the dropdown trigger (<div> with mat-mdc-select-value)
    if selector_type.lower() == "xpath":
        trigger = driver.find_element(By.XPATH, selector_value)
    else:
        trigger = driver.find_element(By.CSS_SELECTOR, selector_value)

    trigger.click()
    print(f"[DEBUG select_mat_option_action] Clicked dropdown trigger using {selector_type}='{selector_value}'.")

    # Wait for mat-option with matching text to appear and click it
    try:
        option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//mat-option[normalize-space(.)='{step_value}']")
            )
        )
        option.click()
        print(f"[DEBUG select_mat_option_action] Selected mat-option with text '{step_value}'.")
    except Exception as e:
        msg = f"[ERROR select_mat_option_action] Could not select option '{step_value}': {e}"
        print(msg)
        raise
