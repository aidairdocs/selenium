# E:\CRM\automation_project\steps_shared_actions\capture_request_number_action.py

import time
from steps_shared_utils.element_utils import find_element
from steps_shared_actions.alert_handler import handle_unexpected_alerts

# We'll assume we store "request number" in a global dictionary, 
# just like we do with OCR or other ephemeral data.
# In practice, you might store it in EXECUTION_CONTEXT or some 
# named dictionary.

EXECUTION_CONTEXT = {}  # Or import a shared one if you prefer

def capture_request_number_action(driver, selector_type, selector_value, step_value, step):
    """
    capture_request_number_action(driver, selector_type, selector_value, step_value, step)

    1) Locate the element by (selector_type, selector_value).
    2) Extract the text or attribute from it.
    3) Store it in memory (EXECUTION_CONTEXT["REQUEST_NUMBER"]) or some dictionary.

    - If the same step is called twice, the new value overwrites the old one.
    """
    print("[DEBUG] capture_request_number_action started.")

    # (A) Dismiss any leftover alerts first
    handle_unexpected_alerts(driver, action="dismiss")

    # (B) Find the element (span, div, input, or whatever)
    element = find_element(driver, selector_type, selector_value)

    # (C) Decide if you want .text or get_attribute("value"). 
    #     This depends on the actual DOM node. 
    #     For a <span>, you'd do element.text. 
    #     For <input>, you might do element.get_attribute("value").
    request_number = element.text.strip()
    if not request_number:
        # Possibly check if it's an <input> type
        request_number = element.get_attribute("value") or ""

    print(f"[DEBUG] Extracted request_number='{request_number}' from the page.")

    # (D) Store/overwrite in some global dictionary or in step
    EXECUTION_CONTEXT["REQUEST_NUMBER"] = request_number
    print("[DEBUG] Stored in EXECUTION_CONTEXT['REQUEST_NUMBER'].")

    # (E) Dismiss any new alert if it popped up
    handle_unexpected_alerts(driver, action="dismiss")

    print("[DEBUG] capture_request_number_action done.")
