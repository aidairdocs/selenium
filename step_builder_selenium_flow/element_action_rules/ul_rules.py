"""Action rules for <ul> tags."""

def actions_for_ul(attributes):
    """Return possible actions for a <ul> element."""
    cls = attributes.get("class", "").lower()
    if "chosen-choices" in cls:
        return [
            "force_chosen_value_injection_action",
            "click",
            "select_country_two_steps",
        ]
    return ["click"]
