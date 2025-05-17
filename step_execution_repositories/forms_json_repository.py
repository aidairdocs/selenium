# E:\CRM\automation_project\step_execution_repositories\forms_json_repository.py
import json

def load_forms_and_steps_from_json(json_path):
    """
    Reads the JSON file containing form info + steps.
    Returns a dict like:
    {
      "form": { "id_uuid": "...", "form_name": "...", "url": "...", ... },
      "steps": [
        { "id_uuid": "...", "step_order": 1, "action_type": "goto", ... },
        ...
      ]
    }
    """
    print(f"[DEBUG] Loading forms + steps from JSON: {json_path}")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # data["form"] -> form dictionary
        # data["steps"] -> list of step dictionaries
        return data
    except Exception as e:
        print(f"[ERROR] Failed to load JSON from '{json_path}': {e}")
        raise
