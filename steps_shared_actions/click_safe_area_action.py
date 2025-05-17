from selenium.webdriver.common.by import By

def click_safe_area_action(driver, selector_type, selector_value, step_value, step):
    """
    click_safe_area_action(...)

    A run-time action that clicks a "safe" location on the page to dismiss
    any pop-up or overlay (e.g. a datepicker) blocking future steps.

    We do this by either:
      - Clicking on <body>, or
      - Using JavaScript to click at a specific coordinate (like (1,1)) if <body> not clickable.

    'selector_type' / 'selector_value' might be ignored if the step doesn't need them.
    'step_value' might also be unused, unless you want to store some logic about where to click.
    """
    print("[DEBUG] click_safe_area_action() called. Attempting to click a safe area on the page.")
    try:
        # Approach A: Find <body> and click it
        # Sometimes <body>.click() might not be recognized if <body> is not truly clickable,
        # but often it triggers a close of popups, datepickers, etc.

        body_element = driver.find_element(By.CSS_SELECTOR, "body")
        body_element.click()
        print("[DEBUG] Clicked <body> to dismiss potential pop-ups.")
    except Exception as e:
        print(f"[WARNING] Could not click <body>: {e}. Trying an alternate JS approach.")

        # Approach B: Use JavaScript to click at a small offset from top-left corner
        # This usually is safe if the top-left corner isn't covering any UI overlays.
        script = """
        var evt = document.createEvent('MouseEvents');
        evt.initMouseEvent('click', true, true, window, 1,
            1, 1, 1, 1, false, false, false, false, 0, null);
        var el = document.elementFromPoint(1, 1);
        if (el) {
            el.dispatchEvent(evt);
            return true;
        }
        return false;
        """
        result = driver.execute_script(script)
        print(f"[DEBUG] JS click at (1,1) result = {result}. Possibly dismissed pop-up.")

    print("[DEBUG] click_safe_area_action completed. Any overlay/popup should now be closed.")

