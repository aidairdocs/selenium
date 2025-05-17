# E:\CRM\automation_project\steps_shared_actions\click_action.py

from steps_shared_utils.element_utils import find_element

def click_action(driver, selector_type, selector_value, step_value, step):
    """
    click_action(...)

    Finds an element by (selector_type, selector_value) and clicks it.
    """
    print("[DEBUG] click_action() called.")
    element = find_element(driver, selector_type, selector_value)
    element.click()
    print("[DEBUG] Element clicked successfully.")

