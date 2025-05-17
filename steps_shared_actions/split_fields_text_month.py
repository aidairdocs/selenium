# actions/date/split_fields_text_month.py
from steps_shared_utils.parse_ymd import parse_ymd


def enter_date_split_text_month_action(driver, selector_type, selector_value, step_value, step):
    """
    3 separate fields: day (numbers), month (text?), year (numbers).
    Month field might be a <select> with "January", "FEBRUARY", "March", etc.
    """
    yyyy, mm, dd = parse_ymd(step_value)
    # day -> day field
    # month -> pick a text from <select> that matches the month name
    # year -> year field
    ...
