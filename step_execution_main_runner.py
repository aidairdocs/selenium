# E:\CRM\automation_project\step_execution_main_runner.py

import os
import sys
import json

# # 1) Figure out the parent directory of "step_execution"
# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# # That means: E:\CRM\automation_project\step_execution\
# PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
# # That means: E:\CRM\automation_project\

# # 2) Insert that into sys.path
# if PROJECT_ROOT not in sys.path:
#     sys.path.insert(0, PROJECT_ROOT)

# 3) Now we can import from steps_shared
from step_execution_selenium_flow.step_execution_step_executor import run_steps_crm_format

# LOAD A CUSTOM FUNCTION TO READ JSON FROM A FILE
from step_execution_repositories.forms_json_repository import load_forms_and_steps_from_json

# SELENIUM-SPECIFIC FUNCTIONS TO START/CLOSE THE BROWSER
from steps_shared_utils.steps_shares_browser_manager import init_browser, close_browser

import os
import json

print("[DEBUG] Python executable:", sys.executable)
print("[DEBUG] PATH:", os.environ.get('PATH'))

def write_execution_input_debug(data):
    """
    Writes the full received JSON (data) to a debug text file and opens it automatically.
    """
    debug_file = os.path.join(os.path.dirname(__file__), "execution_input_debug.txt")
    try:
        with open(debug_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=2))
        # Automatically open the file (this works on Windows)
        os.startfile(debug_file)
    except Exception as e:
        print(f"[ERROR] Could not write or open debug file: {e}")

def main():
    """
    Usage Examples:
    ---------------
    1) Old style: python main_runner.py <form_id>
       -> loads from "exec_data_<form_id>.json"

    2) New style: python main_runner.py --stdin
       -> reads the JSON from sys.stdin, ignoring the old <form_id> approach
    """

    # -----------------------------------------------------
    # PRINT INITIAL DEBUG MESSAGE
    # -----------------------------------------------------
    print("[DEBUG] main_runner.py started.")

    # -----------------------------------------------------
    # CHECK COMMAND-LINE ARGUMENTS FOR --stdin
    # IF PRESENT, WE'LL READ JSON FROM STANDARD INPUT
    # -----------------------------------------------------
    if "--stdin" in sys.argv:
        # A) Read JSON from stdin
        print("[DEBUG] Reading JSON from stdin.")

        # sys.stdin.read() blocks until EOF, so if running from
        # another script, make sure that script sends JSON data properly.
        raw_data = sys.stdin.read()
        print(f"[DEBUG] Raw JSON from stdin => {raw_data[:200]}...")  # Show only first 200 chars

        # ATTEMPT TO PARSE THE RAW JSON
        try:
            data = json.loads(raw_data)
        except Exception as e:
            print(f"[ERROR] Failed to parse JSON from stdin: {e}")
            sys.exit(1)

        # WE EXPECT THE DATA TO CONTAIN A "steps" KEY
        write_execution_input_debug(data)
        steps_data = {"steps": data.get("steps", [])}
        print(f"[DEBUG] Loaded {len(steps_data['steps'])} steps from stdin data.")

    else:
        # B) Fallback: old style reading from a file using <form_id>
        if len(sys.argv) < 2:
            print("[ERROR] Please provide a forms:id_uuid or use --stdin.")
            sys.exit(1)

        # GRAB THE ARGUMENT AFTER python main_runner.py
        chosen_form_id = sys.argv[1]
        print(f"[DEBUG] Received form_id={chosen_form_id} from argument.")

        # BUILD THE JSON FILE NAME BASED ON THE ID
        json_path = f"exec_data_{chosen_form_id}.json"
        print(f"[DEBUG] Loading steps from file: {json_path}")

        # ATTEMPT TO LOAD THE FILE USING OUR CUSTOM REPOSITORY FUNCTION
        try:
            data = load_forms_and_steps_from_json(json_path)
            write_execution_input_debug(data)
            steps_data = {"steps": data.get("steps", [])}
            print(f"[DEBUG] Loaded {len(steps_data['steps'])} steps from {json_path}.")
        except Exception as e:
            print(f"[ERROR] Failed to load steps from '{json_path}': {e}")
            sys.exit(1)

    # IF NO STEPS WERE FOUND, EXIT GRACEFULLY
    if not steps_data["steps"]:
        print("[INFO] No steps found. Exiting.")
        sys.exit(0)

    # -----------------------------------------------------
    # 3) INITIALIZE THE SELENIUM BROWSER
    # -----------------------------------------------------
    print("[DEBUG] Initializing Selenium browser...")
    driver = init_browser(headless=False)

    try:
        # -----------------------------------------------------
        # 4) EXECUTE THE STEPS
        # -----------------------------------------------------
        print("[DEBUG] Running steps now...")
        # run_steps_crm_format() presumably iterates over steps_data["steps"] and uses
        # the driver to interact with a webpage.
        run_steps_crm_format(steps_data, driver=driver, condition_context=data.get("condition_context", {}))

        print("[INFO] Steps execution completed successfully.")
    finally:
        # -----------------------------------------------------
        # 5) CLOSE THE BROWSER (ALWAYS EXECUTES VIA `finally`)
        # -----------------------------------------------------
        print("[DEBUG] Closing the browser.")
        close_browser(driver)

    # FINAL DEBUG STATEMENT
    print("[DEBUG] main_runner.py finished.")

if __name__ == "__main__":
    main()
