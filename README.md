# Project Folder Structure

└── .
    ├── __pycache__
    │   ├── __init__.cpython-311.pyc
    │   ├── app.cpython-311.pyc
    │   ├── db_helper.cpython-311.pyc
    │   ├── db_manager.cpython-311.pyc
    │   ├── forms_window.cpython-311.pyc
    │   ├── step_builder_db_manager.cpython-311.pyc
    │   └── steps_shared_step_executor.cpython-311.pyc
    ├── old
    │   ├── actions
    │   │   ├── __init__.py
    │   │   ├── click_action.py
    │   │   ├── enter_text_action.py
    │   │   ├── enter_text_action_w_escape.py
    │   │   ├── enter_text_date_with_auto_slashes.py
    │   │   ├── manual_action.py
    │   │   └── select_option.py
    │   ├── agent_passport_reader
    │   │   ├── __pycache__
    │   │   │   ├── face_extraction.cpython-311.pyc
    │   │   │   ├── image_preprocessing.cpython-311.pyc
    │   │   │   ├── image_processing.cpython-311.pyc
    │   │   │   ├── mrz_extraction.cpython-311.pyc
    │   │   │   ├── ocr_extraction.cpython-311.pyc
    │   │   │   ├── roi_extraction.cpython-311.pyc
    │   │   │   └── roi_selection.cpython-311.pyc
    │   │   ├── images
    │   │   │   ├── LIO SHALOM Passport Israel 34982091.jpg
    │   │   │   ├── passport_sample.jpg
    │   │   │   ├── RINA PINHASOV Passport Israel 32923661.jpg
    │   │   │   ├── SARA DALIA IRAM Passport Israel 41323290.jpg
    │   │   │   └── YARIV KELER BARUCH Passport Israel 23265685.jpg
    │   │   ├── models
    │   │   │   └── haarcascade_frontalface_default.xml
    │   │   ├── passport_detection
    │   │   │   ├── extracted_face_photo.jpg
    │   │   │   ├── face_detected.jpg
    │   │   │   └── identifying fields in an Israeli passport.jpg
    │   │   ├── face_extraction.py
    │   │   ├── israel.json
    │   │   ├── main.py
    │   │   ├── README.md
    │   │   ├── relative_position.json
    │   │   ├── requirements.txt
    │   │   ├── roi_selection.py
    │   │   └── visualize_fields.py
    │   ├── Agent_Selenium
    │   │   ├── __pycache__
    │   │   │   ├── __init__.cpython-311.pyc
    │   │   │   ├── action_performance.cpython-311.pyc
    │   │   │   ├── agent_selenium_long.cpython-311.pyc
    │   │   │   ├── browser_manager.cpython-311.pyc
    │   │   │   ├── config_loader.cpython-311.pyc
    │   │   │   ├── constants.cpython-311.pyc
    │   │   │   ├── element_selection.cpython-311.pyc
    │   │   │   ├── functions_action_performing.cpython-311.pyc
    │   │   │   ├── functions_element_selection.cpython-311.pyc
    │   │   │   ├── functions_GUI.cpython-311.pyc
    │   │   │   ├── functions_utility.cpython-311.pyc
    │   │   │   ├── gui_manager.cpython-311.pyc
    │   │   │   ├── match_between_JSON_steps_to_JSON_current_step.cpython-311.pyc
    │   │   │   ├── new_step_creator.cpython-311.pyc
    │   │   │   ├── selenium_extraction_elements_current_page.cpython-311.pyc
    │   │   │   ├── selenium_step_executor.cpython-311.pyc
    │   │   │   ├── selenium_steps.cpython-311.pyc
    │   │   │   ├── selenium_steps_long.cpython-311.pyc
    │   │   │   ├── selenum_execute_steps.cpython-311.pyc
    │   │   │   ├── steps_handler.cpython-311.pyc
    │   │   │   ├── user_interface.cpython-311.pyc
    │   │   │   ├── utils.cpython-311.pyc
    │   │   │   └── utils_json.cpython-311.pyc
    │   │   ├── actions
    │   │   │   ├── __pycache__
    │   │   │   │   ├── __init__.cpython-311.pyc
    │   │   │   │   ├── click_action.cpython-311.pyc
    │   │   │   │   ├── enter_text_action.cpython-311.pyc
    │   │   │   │   ├── enter_text_action_w_escape.cpython-311.pyc
    │   │   │   │   ├── enter_text_date_with_auto_slashes.cpython-311.pyc
    │   │   │   │   ├── manual_action.cpython-311.pyc
    │   │   │   │   └── select_option.cpython-311.pyc
    │   │   │   ├── __init__.py
    │   │   │   ├── click_action.py
    │   │   │   ├── enter_text_action.py
    │   │   │   ├── enter_text_action_w_escape.py
    │   │   │   ├── enter_text_date_with_auto_slashes.py
    │   │   │   ├── manual_action.py
    │   │   │   └── select_option.py
    │   │   ├── test
    │   │   │   ├── match_between_JSON_steps_to_JSON_current_step.py
    │   │   │   └── selenium_extraction_elements_current_page.py
    │   │   ├── __init__.py
    │   │   ├── action_performance.py
    │   │   ├── agent_selenium_long.py
    │   │   ├── browser_manager.py
    │   │   ├── client_data.json
    │   │   ├── config_loader.py
    │   │   ├── constants.py
    │   │   ├── element_selection.py
    │   │   ├── selenium_steps_long.py
    │   │   ├── user_interface.py
    │   │   └── utils.py
    │   └── agent_selenium_folder
    │       ├── __pycache__
    │       │   └── config_loader.cpython-311.pyc
    │       ├── agents
    │       │   ├── __pycache__
    │       │   │   └── __init__.cpython-311.pyc
    │       │   ├── element_highlighter
    │       │   │   └── agent_element_highlighter.py
    │       │   ├── html_source
    │       │   │   ├── __pycache__
    │       │   │   │   ├── __init__.cpython-311.pyc
    │       │   │   │   ├── config_loader.cpython-311.pyc
    │       │   │   │   └── html_extractor.cpython-311.pyc
    │       │   │   ├── __init__.py
    │       │   │   ├── agent_html_source.py
    │       │   │   ├── html_config_loader.py
    │       │   │   └── html_extractor.py
    │       │   ├── screen_recognition
    │       │   │   ├── __pycache__
    │       │   │   │   ├── __init__.cpython-311.pyc
    │       │   │   │   ├── config_loader.cpython-311.pyc
    │       │   │   │   └── screenshot_capturer.cpython-311.pyc
    │       │   │   ├── __init__.py
    │       │   │   ├── agent_windows_snip.py
    │       │   │   ├── config_loader.py
    │       │   │   └── screenshot_capturer.py
    │       │   └── __init__.py
    │       ├── config
    │       │   ├── agents.json
    │       │   ├── paths.json
    │       │   └── sites.json
    │       ├── data
    │       │   ├── clients
    │       │   │   └── client_variables.json
    │       │   ├── html_outputs
    │       │   │   ├── india
    │       │   │   │   └── 1730143000
    │       │   │   │       ├── elements.json
    │       │   │   │       ├── screenshot.png
    │       │   │   │       └── source_html.html
    │       │   │   └── usa_esta
    │       │   │       └── 1730147494
    │       │   │           ├── annotated_screenshot.png
    │       │   │           ├── elements.json
    │       │   │           ├── screenshot.png
    │       │   │           └── source_html.html
    │       │   └── steps
    │       │       ├── cambidia
    │       │       │   └── steps_cambidia.json
    │       │       ├── india_30_days
    │       │       │   ├── stage_1
    │       │       │   │   └── stage_1.json
    │       │       │   ├── stage_10
    │       │       │   ├── stage_11
    │       │       │   ├── stage_12
    │       │       │   ├── stage_13
    │       │       │   ├── stage_14
    │       │       │   ├── stage_15
    │       │       │   ├── stage_16
    │       │       │   ├── stage_17
    │       │       │   ├── stage_18
    │       │       │   ├── stage_2
    │       │       │   │   └── stage_2.json
    │       │       │   ├── stage_3
    │       │       │   ├── stage_4
    │       │       │   ├── stage_5
    │       │       │   ├── stage_6
    │       │       │   ├── stage_7
    │       │       │   ├── stage_8
    │       │       │   ├── stage_9
    │       │       │   └── steps_india_30_days.json
    │       │       ├── kenya_eta
    │       │       │   ├── stage_1
    │       │       │   ├── stage_2
    │       │       │   ├── stage_3
    │       │       │   ├── stage_4
    │       │       │   ├── stage_5
    │       │       │   ├── stage_6
    │       │       │   ├── stage_7
    │       │       │   ├── stage_8
    │       │       │   └── steps_kenya_eta.json
    │       │       ├── laos
    │       │       │   ├── stage_1
    │       │       │   ├── stage_10
    │       │       │   ├── stage_11
    │       │       │   ├── stage_12
    │       │       │   ├── stage_13
    │       │       │   ├── stage_14
    │       │       │   ├── stage_15
    │       │       │   ├── stage_16
    │       │       │   ├── stage_2
    │       │       │   ├── stage_3
    │       │       │   ├── stage_4
    │       │       │   ├── stage_5
    │       │       │   ├── stage_6
    │       │       │   ├── stage_7
    │       │       │   ├── stage_8
    │       │       │   ├── stage_9
    │       │       │   └── steps_laos.json
    │       │       ├── singapore_plf
    │       │       │   ├── stage_1
    │       │       │   ├── stage_2
    │       │       │   ├── stage_3
    │       │       │   ├── stage_4
    │       │       │   └── steps_singapore_plf.json
    │       │       └── usa_esta
    │       │           ├── stage_1
    │       │           │   └── stage_1.json
    │       │           ├── stage_2
    │       │           │   └── stage_2.json
    │       │           ├── stage_3
    │       │           ├── stage_4
    │       │           ├── stage_5
    │       │           ├── stage_6
    │       │           ├── stage_7
    │       │           ├── stage_8
    │       │           └── steps_usa_esta.json
    │       ├── __init__.py
    │       ├── combined_agent.py
    │       ├── config_loader.py
    │       ├── geckodriver.log
    │       ├── main.py
    │       ├── Project_Structure.txt
    │       └── test_imports.py
    ├── step_builder_lib
    │   ├── __pycache__
    │   │   ├── __init__.cpython-311.pyc
    │   │   └── db_manager.cpython-311.pyc
    │   ├── __init__.py
    │   └── table_specs.py
    ├── step_builder_repositories
    │   ├── __pycache__
    │   │   ├── __init__.cpython-311.pyc
    │   │   ├── form_steps_repository.cpython-311.pyc
    │   │   ├── forms_repository.cpython-311.pyc
    │   │   ├── step_builder_form_steps_repository.cpython-311.pyc
    │   │   └── step_builder_forms_repository.cpython-311.pyc
    │   ├── __init__.py
    │   ├── step_builder_form_steps_repository.py
    │   └── step_builder_forms_repository.py
    ├── step_builder_selenium_flow
    │   ├── __pycache__
    │   │   ├── __init__.cpython-311.pyc
    │   │   ├── browser_manager.cpython-311.pyc
    │   │   ├── create_new_step_flow.cpython-311.pyc
    │   │   ├── create_step_helpers.cpython-311.pyc
    │   │   ├── element_selection_manager.cpython-311.pyc
    │   │   ├── step_builder_browser_manager.cpython-311.pyc
    │   │   ├── step_builder_create_new_step_flow.cpython-311.pyc
    │   │   ├── step_builder_create_step_helpers.cpython-311.pyc
    │   │   ├── step_builder_element_selection_manager.cpython-311.pyc
    │   │   ├── step_builder_step_executor.cpython-311.pyc
    │   │   └── step_executor.cpython-311.pyc
    │   ├── __init__.py
    │   ├── step_builder_create_new_step_flow.py
    │   ├── step_builder_create_step_helpers.py
    │   ├── step_builder_element_selection_manager.py
    │   └── step_builder_step_executor.py
    ├── step_builder_ui
    │   ├── __pycache__
    │   │   ├── __init__.cpython-311.pyc
    │   │   ├── step_builder_user_interface.cpython-311.pyc
    │   │   └── user_interface.cpython-311.pyc
    │   ├── __init__.py
    │   └── step_builder_user_interface.py
    ├── step_execution_repositories
    │   ├── __pycache__
    │   │   ├── __init__.cpython-311.pyc
    │   │   └── forms_json_repository.cpython-311.pyc
    │   ├── __init__.py
    │   └── forms_json_repository.py
    ├── step_execution_selenium_flow
    │   ├── __pycache__
    │   │   ├── __init__.cpython-311.pyc
    │   │   ├── browser_manager.cpython-311.pyc
    │   │   └── step_execution_step_executor.cpython-311.pyc
    │   ├── __init__.py
    │   ├── evaluate_condition_debug.txt
    │   ├── run_steps_crm_format_debug.txt
    │   ├── step_execution_step_executor.py
    │   └── step_execution_step_executor_evaluate_condition.txt
    ├── steps_shared_actions
    │   ├── __pycache__
    │   │   ├── __init__.cpython-311.pyc
    │   │   ├── alert_handler.cpython-311.pyc
    │   │   ├── capture_request_number_action.cpython-311.pyc
    │   │   ├── click_action.cpython-311.pyc
    │   │   ├── click_safe_area_action.cpython-311.pyc
    │   │   ├── datepicker_dialog.cpython-311.pyc
    │   │   ├── dismiss_modal_action.cpython-311.pyc
    │   │   ├── enter_date_custom.cpython-311.pyc
    │   │   ├── enter_day_action.cpython-311.pyc
    │   │   ├── enter_month_action.cpython-311.pyc
    │   │   ├── enter_ocr_result_action.cpython-311.pyc
    │   │   ├── enter_text_action.cpython-311.pyc
    │   │   ├── enter_year_action.cpython-311.pyc
    │   │   ├── force_chosen_value_injection_action.cpython-311.pyc
    │   │   ├── force_date_injection_5days_action.cpython-311.pyc
    │   │   ├── force_date_injection_action.cpython-311.pyc
    │   │   ├── full_page_screenshot_action.cpython-311.pyc
    │   │   ├── goto_action.cpython-311.pyc
    │   │   ├── goto_from_email.cpython-311.pyc
    │   │   ├── goto_from_email_action.cpython-311.pyc
    │   │   ├── handle_unknown_action.cpython-311.pyc
    │   │   ├── manual_action.cpython-311.pyc
    │   │   ├── ocr_captcha_action.cpython-311.pyc
    │   │   ├── page_transition.cpython-311.pyc
    │   │   ├── safe_action.cpython-311.pyc
    │   │   ├── search_and_select_country_action.cpython-311.pyc
    │   │   ├── select_country_in_app_list_action.cpython-311.pyc
    │   │   ├── select_country_prefix_action.cpython-311.pyc
    │   │   ├── select_country_two_steps.cpython-311.pyc
    │   │   ├── select_option_action.cpython-311.pyc
    │   │   ├── split_fields_numbers.cpython-311.pyc
    │   │   ├── split_fields_text_month.cpython-311.pyc
    │   │   └── standard_dd_mm_yyyy.cpython-311.pyc
    │   ├── __init__.py
    │   ├── ACTIONBYSITE.txt
    │   ├── alert_handler.py
    │   ├── capture_request_number_action.py
    │   ├── click_action.py
    │   ├── click_safe_area_action.py
    │   ├── datepicker_dialog.py
    │   ├── dismiss_modal_action.py
    │   ├── enter_date_custom.py
    │   ├── enter_day_action.py
    │   ├── enter_month_action.py
    │   ├── enter_ocr_result_action.py
    │   ├── enter_text_action.py
    │   ├── enter_year_action.py
    │   ├── force_chosen_value_injection_action.py
    │   ├── force_date_injection_5days_action.py
    │   ├── force_date_injection_action.py
    │   ├── full_page_screenshot_action.py
    │   ├── goto_action.py
    │   ├── goto_from_email.py
    │   ├── handle_unknown_action.py
    │   ├── manual_action.py
    │   ├── ocr_captcha_action.py
    │   ├── page_transition.py
    │   ├── safe_action.py
    │   ├── select_country_prefix_action.py
    │   ├── select_country_two_steps.py
    │   ├── select_option_action.py
    │   ├── split_fields_text_month.py
    │   └── standard_dd_mm_yyyy.py
    ├── steps_shared_utils
    │   ├── __pycache__
    │   │   ├── __init__.cpython-311.pyc
    │   │   ├── adaptive_wait.cpython-311.pyc
    │   │   ├── date_utils.cpython-311.pyc
    │   │   ├── element_utils.cpython-311.pyc
    │   │   ├── paddleocr_db_manager.cpython-311.pyc
    │   │   ├── parse_ymd.cpython-311.pyc
    │   │   ├── pick_conditions_gui.cpython-311.pyc
    │   │   ├── step_wait_config.cpython-311.pyc
    │   │   ├── steps_shared_actions_registry.cpython-311.pyc
    │   │   ├── steps_shared_conditions_registry.cpython-311.pyc
    │   │   ├── steps_shares_browser_manager.cpython-311.pyc
    │   │   └── wait_helpers.cpython-311.pyc
    │   ├── __init__.py
    │   ├── adaptive_wait.py
    │   ├── element_utils.py
    │   ├── paddleocr_db_manager.py
    │   ├── parse_ymd.py
    │   ├── pick_conditions_gui.py
    │   ├── step_wait_config.json
    │   ├── step_wait_config.py
    │   ├── steps_shared_actions_registry.py
    │   ├── steps_shared_conditions_registry.py
    │   ├── steps_shares_browser_manager.py
    │   └── wait_helpers.py
    ├── vscode
    │   └── settings.json
    ├── __init__.py
    ├── execution_input_debug.txt
    ├── generate_sitemap.py
    ├── README.md
    ├── step_builder_db_manager.py
    ├── step_builder_main_controller.py
    └── step_execution_main_runner.py
