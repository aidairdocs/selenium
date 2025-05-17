import time
from selenium.common.exceptions import TimeoutException

# Import the update and get functions from the configuration module.
from steps_shared_utils.step_wait_config import update_step_config, get_step_config

def adaptive_wait_for_action(driver, action_test_fn, max_wait=7.0, poll_interval=0.5, step_id=None, action_type=None, form_id=None, form_name=None):
    """
    Wait adaptively for an action to become performable.
    
    This function repeatedly calls the provided action_test_fn (a non-destructive test
    of the output action) at intervals of poll_interval seconds, up to a maximum of max_wait seconds.
    
    Before starting, it checks the configuration JSON for an existing optimal wait time for this
    specific form/step/action. If found, that value is used as the max_wait. Otherwise, it defaults
    to 7 seconds.
    
    Parameters:
      driver         : Selenium WebDriver instance.
      action_test_fn : A callable that accepts the driver and returns True if the action can be performed.
      max_wait       : Default maximum time (in seconds) to wait (used if no config is available).
      poll_interval  : Time (in seconds) between test attempts.
      step_id        : The unique identifier for the step (from form_steps::id_uuid).
      action_type    : The type of action (e.g., "click", "enter_text", "select_date").
      form_id        : The unique identifier for the form (if available).
      form_name      : The name of the form (if available).
      
    Returns:
      measured_wait : The time (in seconds) that it took for the action to become performable.
                     If the action never becomes ready, returns max_wait.
    """
    # Use the existing optimal wait time from the JSON config if available.
    if form_id and step_id and action_type:
        existing_config = get_step_config(form_id, step_id, action_type, default_wait=max_wait)
        if existing_config.get("optimal_wait", 0) > 0:
            max_wait = existing_config["optimal_wait"]
        else:
            max_wait = max_wait  # Use the default passed in (7.0s in this case)
    
    print(f"[DEBUG adaptive_wait] Called for step_id '{step_id}', action '{action_type}', form_id '{form_id}', form_name '{form_name}' with max_wait={max_wait}s.")
    print(f"[DEBUG adaptive_wait] Starting adaptive wait for step_id '{step_id}', action '{action_type}'. Poll interval: {poll_interval}s.")
    
    start_time = time.time()
    elapsed = 0
    attempts = 0
    success = False
    
    while elapsed < max_wait:
        attempts += 1
        try:
            if action_test_fn(driver):
                success = True
                break
        except Exception as e:
            print(f"[DEBUG adaptive_wait] Attempt {attempts} raised exception: {e}")
        time.sleep(poll_interval)
        elapsed = time.time() - start_time
        print(f"[DEBUG adaptive_wait] Attempt {attempts}: elapsed time = {elapsed:.2f}s")
    
    measured_wait = elapsed if success else max_wait
    if success:
        print(f"[DEBUG adaptive_wait] Action became performable after {measured_wait:.2f}s in {attempts} attempts.")
    else:
        print(f"[WARNING adaptive_wait] Action did not become performable after {max_wait}s (attempts: {attempts}). Using max_wait as measured time.")
    
    # Update configuration for this step and action.
    if step_id and action_type:
        update_step_config(step_id, action_type, measured_wait, form_id=form_id, form_name=form_name)
        print(f"[DEBUG adaptive_wait] Updated wait configuration for step_id '{step_id}', action '{action_type}'.")
    else:
        print("[DEBUG adaptive_wait] step_id or action_type not provided; configuration not updated.")
    
    return measured_wait
