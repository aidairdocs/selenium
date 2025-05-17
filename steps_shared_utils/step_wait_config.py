import json
import os

# Define the path for the configuration file (stored in the same directory as this module)
CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "step_wait_config.json")

def load_config():
    """
    Load the wait configuration from the JSON file.
    Returns a dictionary. If the file does not exist, returns an empty dict.
    """
    if not os.path.exists(CONFIG_FILE_PATH):
        print(f"[DEBUG step_wait_config] Config file not found at {CONFIG_FILE_PATH}. Returning empty config.")
        return {}
    try:
        with open(CONFIG_FILE_PATH, "r") as f:
            config = json.load(f)
            # print(f"[DEBUG step_wait_config] Loaded config: {config}")
            return config
    except Exception as e:
        print(f"[ERROR step_wait_config] Failed to load config: {e}")
        return {}

def save_config(config):
    """
    Save the wait configuration dictionary to the JSON file.
    """
    # print(f"[DEBUG step_wait_config] CONFIG_FILE_PATH is set to: {CONFIG_FILE_PATH}")
    try:
        with open(CONFIG_FILE_PATH, "w") as f:
            json.dump(config, f, indent=4)
        # print(f"[DEBUG step_wait_config] Config saved successfully to {CONFIG_FILE_PATH}.")
    except Exception as e:
        print(f"[ERROR step_wait_config] Failed to save config: {e}")

def update_step_config(step_id, action_type, measured_wait, form_id=None, form_name=None, alpha=0.2):
    """
    Update the configuration for a given step and action with a new measured wait time.
    
    If form_id (and optionally form_name) is provided, then store the config under that form.
    Instead of storing a growing list of samples, we use an exponential moving average (EMA)
    to update the optimal_wait.
    
    Parameters:
      step_id      : Unique identifier for the step (from the database).
      action_type  : Type of action (e.g., "click", "enter_text").
      measured_wait: The wait time measured in this run (in seconds).
      form_id      : (Optional) The unique identifier for the form.
      form_name    : (Optional) The form's name.
      alpha        : Smoothing factor for EMA (default 0.2).
    """
    config = load_config()
    
    if form_id:
        if form_id not in config:
            config[form_id] = {"form_name": form_name or "", "steps": {}}
        if step_id not in config[form_id]["steps"]:
            config[form_id]["steps"][step_id] = {}
        if action_type not in config[form_id]["steps"][step_id]:
            # Initialize with the first measurement
            config[form_id]["steps"][step_id][action_type] = {"ema": measured_wait, "count": 1}
        else:
            current_data = config[form_id]["steps"][step_id][action_type]
            current_ema = current_data.get("ema", measured_wait)
            count = current_data.get("count", 1)
            # Update EMA: new_ema = alpha * measured_wait + (1 - alpha) * old_ema
            new_ema = alpha * measured_wait + (1 - alpha) * current_ema
            config[form_id]["steps"][step_id][action_type]["ema"] = new_ema
            config[form_id]["steps"][step_id][action_type]["count"] = count + 1
        # print(f"[DEBUG step_wait_config] Updating config for form_id '{form_id}', step_id '{step_id}', action '{action_type}': {config[form_id]['steps'][step_id][action_type]}")
    else:
        # Fallback if form_id not provided: use top-level keyed by step_id.
        if step_id not in config:
            config[step_id] = {}
        if action_type not in config[step_id]:
            config[step_id][action_type] = {"ema": measured_wait, "count": 1}
        else:
            current_data = config[step_id][action_type]
            current_ema = current_data.get("ema", measured_wait)
            count = current_data.get("count", 1)
            new_ema = alpha * measured_wait + (1 - alpha) * current_ema
            config[step_id][action_type]["ema"] = new_ema
            config[step_id][action_type]["count"] = count + 1
        # print(f"[DEBUG step_wait_config] Updating config for step_id '{step_id}', action '{action_type}': {config[step_id][action_type]}")
    
    save_config(config)


def get_step_config(form_id, step_id, action_type, default_wait=0):
    """
    Retrieve the wait configuration for a given form, step, and action.
    Returns a dictionary with keys "ema" (the current estimated optimal wait)
    and "count" (the number of measurements that have been taken).
    
    If no configuration exists, returns a default structure with "ema" set to default_wait and "count" 0.
    
    Parameters:
      form_id     : The unique identifier for the form.
      step_id     : The unique identifier for the step (from the DB, e.g. id_uuid).
      action_type : The type of action (e.g., "click", "enter_text").
      default_wait: The default wait time to use if no config is present (default is 0).
    
    Returns:
      A dictionary such as: {"ema": <optimal_wait>, "count": <number_of_measurements>}
    """
    config = load_config()
    form_config = config.get(form_id, {})
    steps_config = form_config.get("steps", {})
    action_config = steps_config.get(step_id, {}).get(action_type, {"ema": default_wait, "count": 0})
    print(f"[DEBUG step_wait_config] get_step_config for form_id '{form_id}', step_id '{step_id}', action '{action_type}': {action_config}")
    return action_config

