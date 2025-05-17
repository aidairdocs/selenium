# E:\CRM\automation_project\steps_shared_actions\enter_ocr_result_action.py

from steps_shared_utils.element_utils import find_element
from steps_shared_actions.alert_handler import handle_unexpected_alerts

# Import the global dictionary from ocr_captcha_action
from .ocr_captcha_action import EXECUTION_CONTEXT

def enter_ocr_result_action(driver, selector_type, selector_value, step_value, step):
    """
    1) Retrieve the last OCR text from EXECUTION_CONTEXT
    2) Find the input field
    3) Type that text
    """
    print("[DEBUG] enter_ocr_result_action started.")
    handle_unexpected_alerts(driver, action="accept")

    final_text = EXECUTION_CONTEXT.get("last_ocr_result", "")
    print(f"[DEBUG] Using last OCR text => {final_text}")

    input_el = find_element(driver, selector_type, selector_value)
    input_el.clear()
    input_el.send_keys(final_text)

    handle_unexpected_alerts(driver, action="accept")
    print("[DEBUG] enter_ocr_result_action done.")
