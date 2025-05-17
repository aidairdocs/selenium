# E:\CRM\automation_project\step_builder_repositories\step_builder_forms_repository.py
"""
Handles database operations related to the 'forms' table.
This code is execution-agnostic; it simply loads forms from DB.
No step-building logic is present here.
"""

from step_builder_db_manager import get_connection

def load_forms():
    """
    load_forms()

    Fetches a list of forms from the database, returning them as a list of dicts:
    [
      {
        "id_uuid": "...",
        "form_name": "...",
        "status": "..."
      },
      ...
    ]

    Adjust the WHERE clause or remove it entirely if you want to load forms
    with different statuses.
    """
    print("[DEBUG forms_repository.load_forms] Called.")

    forms_list = []
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Example SELECT - adapt as needed
                cur.execute("""
                    SELECT id_uuid, form_name, status
                    FROM forms
                    WHERE status = 'development'
                    ORDER BY created_at
                """)
                rows = cur.fetchall()

                for row in rows:
                    form_id, form_name, status = row
                    forms_list.append({
                        "id_uuid": str(form_id),
                        "form_name": form_name,
                        "status": status
                    })

        print(f"[DEBUG forms_repository.load_forms] Loaded {len(forms_list)} forms from DB.")
        return forms_list

    except Exception as e:
        print(f"[ERROR] forms_repository.load_forms: Failed to load forms: {e}")
        # Re-raise so the caller can handle it
        raise
