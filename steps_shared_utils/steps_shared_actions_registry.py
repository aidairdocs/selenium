# E:\CRM\automation_project\steps_shared_utils\steos_shared_actions_registry.py

from steps_shared_actions.capture_request_number_action import capture_request_number_action

from steps_shared_actions.ocr_captcha_action import ocr_captcha_action
from steps_shared_actions.enter_ocr_result_action import enter_ocr_result_action

from steps_shared_actions.goto_action import goto_action
from steps_shared_actions.goto_from_email import goto_from_email

from steps_shared_actions.select_option_action import select_option_action
from steps_shared_actions.force_chosen_value_injection_action import force_chosen_value_injection_action

from steps_shared_actions.manual_action import manual_action
from steps_shared_actions.safe_action import safe_action

from steps_shared_actions.enter_text_action import enter_text_action

from steps_shared_actions.click_safe_area_action import click_safe_area_action
from steps_shared_actions.dismiss_modal_action import dismiss_modal_action

from steps_shared_actions.click_action import click_action

from steps_shared_actions.page_transition import page_transition_action

from steps_shared_actions.enter_date_custom import enter_date_custom_dialog_action
from steps_shared_actions.datepicker_dialog import enter_date_datepicker_action
from steps_shared_actions.enter_year_action import enter_year_action
from steps_shared_actions.enter_month_action import enter_month_action
from steps_shared_actions.enter_day_action import enter_day_action
from steps_shared_actions.split_fields_text_month import enter_date_split_text_month_action
from steps_shared_actions.standard_dd_mm_yyyy import enter_date_dd_mm_yyyy_action
from steps_shared_actions.force_date_injection_action import force_date_injection_action
from steps_shared_actions.force_date_injection_5days_action import force_date_injection_5days_action

from steps_shared_actions.select_country_prefix_action import select_country_prefix_action
from steps_shared_actions.select_country_two_steps import select_country_two_steps
from steps_shared_actions.select_mat_option_action import select_mat_option_action


from steps_shared_actions.full_page_screenshot_action import full_page_screenshot_action


ACTION_HANDLERS = {
    "goto": goto_action,
    "goto_from_email": goto_from_email,
    "click": click_action,
    "enter_text": enter_text_action,
    "select_option": select_option_action,
    "select_mat_option_action": select_mat_option_action,
    "manual": manual_action,
    "click_safe_area": click_safe_area_action,
    "page_transition": page_transition_action,
    "enter_date_dd_mm_yyyy_action": enter_date_dd_mm_yyyy_action,
    "enter_date_datepicker": enter_date_datepicker_action,
    "enter_year_action": enter_year_action,
    "enter_month_action": enter_month_action,
    "enter_day_action": enter_day_action,
    "enter_date_split_textmonth": enter_date_split_text_month_action,
    "enter_date_custom_dialog_action": enter_date_custom_dialog_action,
    "ocr_captcha": ocr_captcha_action,
    "enter_ocr_result": enter_ocr_result_action,
    "capture_request_number": capture_request_number_action,
    "full_page_screenshot": full_page_screenshot_action,
    "force_date_injection": force_date_injection_action,
    "select_country_prefix": select_country_prefix_action,
    "force_date_injection_5days_action": force_date_injection_5days_action,
    "force_chosen_value_injection_action": force_chosen_value_injection_action,
    "dismiss_modal": dismiss_modal_action,
    "safe_action": safe_action,
    "select_country_two_steps": select_country_two_steps,

}