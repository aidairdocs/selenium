"""Action rules for <select> tags."""

def actions_for_select(attributes):
    """Return possible actions for a <select> element."""
    actions = ["select_option", "click"]

    def in_id_or_name(substr):
        elem_id = attributes.get("id", "").lower()
        elem_name = attributes.get("name", "").lower()
        return (substr.lower() in elem_id) or (substr.lower() in elem_name)

    if in_id_or_name("day"):
        actions.append("enter_day_action")
    if in_id_or_name("month"):
        actions.append("enter_month_action")
    if in_id_or_name("year"):
        actions.append("enter_year_action")

    return actions
