# Action to select a <mat-option> item in Angular Material dropdowns.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from steps_shared_utils.element_utils import find_element


def select_mat_option_action(driver, selector_type, selector_value, step_value, step):
    """Select an item from an Angular Material <mat-select> dropdown."""
    print("[DEBUG] select_mat_option_action started.")

    dropdown = find_element(driver, selector_type, selector_value)
    dropdown.click()

    normalized_text = step_value.strip().lower()
    option_xpath = (
        "//mat-option[translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz')='" + normalized_text + "']"
    )

    option = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, option_xpath))
    )
    option.click()
    print(f"[DEBUG] Selected mat-option '{step_value}'.")
