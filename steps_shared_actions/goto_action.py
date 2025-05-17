
def goto_action(driver, selector_type, selector_value, step_value, step):
    """
    goto_action(...)

    Navigates to a URL specified in 'step_value'.
    'selector_value' is ignored here (since goto only needs a URL).
    """
    print(f"[DEBUG] goto_action() called. Navigating to {step_value}")
    driver.get(step_value)

