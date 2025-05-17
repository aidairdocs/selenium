import json
from step_builder_db_manager import get_connection

def load_form_steps(form_id):
    """
    Returns a dict like:
    {
      "steps": [
        {
          "step_number": 1,
          "action": "click",
          "selector_type": "xpath",
          "selector_value": "//div/button[1]",
          "value": "",
          "element_type": "button",
          "text_content": "Submit",
          "description": "Click the Submit button",
          "condition": "",  # or "IS_MINOR == True" etc.
          "id_uuid": id_uuid
        },
        ...
      ]
    }
    """
    print("[DEBUG] form_steps_repository.load_form_steps() called with form_id=", form_id)

    steps_data = {"steps": []}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Updated SQL query to include id_uuid from form_steps table.
                cur.execute("""
                    SELECT
                        id_uuid,
                        step_order,
                        action_type,
                        selector_value,
                        selector_type,
                        element_type,
                        selector_title,
                        insert_value,
                        description,
                        condition
                    FROM form_steps
                    WHERE forms_id = %s
                    ORDER BY step_order
                """, (form_id,))

                rows = cur.fetchall()
                print(f"[DEBUG] Found {len(rows)} step(s) for form_id={form_id}.")

                for (
                    id_uuid,
                    step_order,
                    action_type,
                    selector_value,
                    selector_type,
                    element_type,
                    selector_title,
                    insert_value,
                    description,
                    condition_str
                ) in rows:
                    # Build each step dict, including the unique step id.
                    steps_data["steps"].append({
                        "step_number": step_order,
                        "action": action_type,
                        "selector_type": selector_type or "xpath",
                        "selector_value": selector_value or "",
                        "value": insert_value or "",
                        "element_type": element_type or "",
                        "text_content": selector_title or "",
                        "description": description or "",
                        "condition": condition_str or "",  # store as a string
                        # Optionally include a pseudo element ID (if desired)
                        "element_id": f"element_{step_order}",
                        # Include the actual unique step identifier from the DB.
                        "id_uuid": id_uuid
                    })
        return steps_data

    except Exception as e:
        print(f"[ERROR] Failed to load steps for form_id={form_id}: {e}")
        raise


def save_new_step(
    form_id,
    step_order,
    action_type,
    selector_value,
    selector_type,
    insert_value,
    description,
    selector_title="",
    element_type="",
    element_attributes=None,
    condition=""
):
    """
    save_new_step(...)

    Inserts a new row into form_steps for the given form (form_id).
    - form_id: The UUID of the forms table
    - step_order: The integer order for this step (1-based or otherwise)
    - action_type: e.g. 'click', 'goto', 'enter_text', etc.
    - selector_value: Usually XPATH or CSS
    - selector_type: 'xpath' or 'css'
    - insert_value: The text/URL for 'goto' or 'enter_text', etc.
    - description: A user-provided note for this step
    - selector_title: Optional text near the element
    - element_type: e.g. 'select', 'input', 'button'
    - element_attributes: JSON-friendly dict of attributes
    - condition: A string representing any condition or expression

    The new column "condition" in form_steps must exist in the DB.
    """
    if element_attributes is None:
        element_attributes = {}

    from step_builder_db_manager import get_connection

    print("[DEBUG form_steps_repository.save_new_step] Called.")
    print(f"[DEBUG] Inserting step_order={step_order}, action_type={action_type} for form_id={form_id}.")
    print(f"[DEBUG] element_attributes being saved: {element_attributes}")
    print(f"[DEBUG] condition => {condition!r}")

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Insert the new step into the database.
                cur.execute("""
                    INSERT INTO form_steps (
                        forms_id,
                        step_order,
                        action_type,
                        selector_value,
                        selector_type,
                        insert_value,
                        description,
                        selector_title,
                        element_type,
                        element_attributes,
                        condition,
                        created_at
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()
                    )
                """, (
                    form_id,
                    step_order,
                    action_type,
                    selector_value,
                    selector_type,
                    insert_value,
                    description,
                    selector_title,
                    element_type,
                    json.dumps(element_attributes),
                    condition  # Insert the condition string
                ))

        print(f"[DEBUG] Successfully inserted step_order={step_order} for form_id={form_id}.")
        return step_order
    except Exception as e:
        print(f"[ERROR] Failed to insert new step: {e}")
        raise
