# E:\CRM\automation_project\steps_shared_actions\alert_handler.py

from selenium.common.exceptions import NoAlertPresentException

def handle_unexpected_alerts(driver, action="accept"):
    """
    Always attempts to switch to any open alert/confirm/prompt and clicks the "OK" (accept) button.
    Returns True if an alert was found, or False if no alert was present.

    We also print the alert's text for debugging. 
    If you discover a new alert that needs special logic, you can add it here.
    """
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"[DEBUG alert_handler] Found unexpected alert: '{alert_text}'")

        # Always accept/click "OK"
        alert.accept()
        print("[DEBUG alert_handler] Alert accepted (always confirm).")

        return True

    except NoAlertPresentException:
        # No alert, do nothing
        return False
    except Exception as e:
        print(f"[WARNING alert_handler] Error handling alert: {e}")
        return False
