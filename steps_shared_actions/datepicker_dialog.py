# actions/date/datepicker_dialog.py
from steps_shared_utils.parse_ymd import parse_ymd


def enter_date_datepicker_action(driver, selector_type, selector_value, step_value, step):
    """
    For a datepicker that user cannot type into. Must click an icon, pick year, month, day in a pop-up.
    """
    yyyy, mm, dd = parse_ymd(step_value)
    # 1) click the icon or the field
    # 2) wait for the pop-up
    # 3) choose the year, month, day
    ...
