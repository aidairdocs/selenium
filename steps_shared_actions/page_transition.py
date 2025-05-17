# actions/page_transition.py

from steps_shared_utils.element_utils import find_element

def page_transition_action(driver, selector_type, selector_value, step_value, step):
    print("[DEBUG] page_transition_action() called.")
    element = find_element(driver, selector_type, selector_value)
    element.click()
    print("[DEBUG] Element clicked successfully (page_transition).")
