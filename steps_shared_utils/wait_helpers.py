import time
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def click_with_retry(driver, element, max_retries=5, delay=1.0):
    """
    Attempts to click the given element up to max_retries times.
    Between attempts, waits for 'delay' seconds.
    """
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            element.click()
            return  # success
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
            last_exc = e
            print(f"[WARNING] Attempt #{attempt} to click element failed: {e}")
            time.sleep(delay)
    raise last_exc

def wait_for_overlay_disappear(driver, overlay_id="overlay-background", timeout=2):
    """
    Waits up to 'timeout' seconds for an overlay (by ID) to disappear.
    """
    print(f"[DEBUG] Waiting up to {timeout}s for overlay '{overlay_id}' to disappear.")
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.ID, overlay_id))
        )
        print("[DEBUG] Overlay disappeared or was not present.")
    except TimeoutException:
        print(f"[WARNING] Overlay '{overlay_id}' still visible after {timeout}s. Continuing anyway.")

def wait_until_clickable(driver, by, locator, timeout=2):
    """
    Waits up to 'timeout' seconds for an element (located by the given by/locator) to become clickable.
    """
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.element_to_be_clickable((by, locator)))

def wait_for_page_ready(driver, timeout=3, spinner_css=None, check_jquery=False, check_angular=False):
    """
    Combined wait function that checks for page readiness in one step.
    It verifies:
      - The document's readyState is "complete"
      - (Optionally) That a spinner (if provided via spinner_css) is no longer visible
      - (Optionally) That jQuery has no active AJAX calls
      - (Optionally) That Angular (if present) is stable
    All conditions are checked together, so that the total wait is no longer the sum of individual waits.
    
    Parameters:
      driver          : Selenium WebDriver instance.
      timeout         : Maximum seconds to wait for all conditions.
      spinner_css     : (Optional) CSS selector for a loading spinner/overlay.
      check_jquery    : (Optional) If True, waits until jQuery.active is 0.
      check_angular   : (Optional) If True, waits until Angular is stable.
    """
    start_time = time.time()

    def combined_condition(d):
        # Check document.readyState
        if d.execute_script("return document.readyState") != "complete":
            return False
        # Check spinner invisibility if spinner_css is provided
        if spinner_css:
            try:
                spinner = d.find_element(By.CSS_SELECTOR, spinner_css)
                if spinner.is_displayed():
                    return False
            except Exception:
                # If the spinner isn't found, assume it's gone
                pass
        # Optionally check jQuery status
        if check_jquery:
            try:
                jquery_active = d.execute_script("return (typeof jQuery !== 'undefined' ? jQuery.active : 0)")
                if jquery_active != 0:
                    return False
            except Exception:
                pass
        # Optionally check Angular stability
        if check_angular:
            try:
                angular_stable = d.execute_script("""
                    if (window.getAllAngularTestabilities) {
                        return getAllAngularTestabilities()[0].isStable();
                    }
                    return true;
                """)
                if not angular_stable:
                    return False
            except Exception:
                pass
        return True

    try:
        WebDriverWait(driver, timeout).until(combined_condition)
        total_wait = time.time() - start_time
        print(f"[DEBUG wait_helpers] Combined wait_for_page_ready finished in {total_wait:.2f}s")
    except TimeoutException as e:
        total_wait = time.time() - start_time
        print(f"[WARNING wait_helpers] wait_for_page_ready timed out after {timeout}s: {e}. Total wait: {total_wait:.2f}s")
