"""Action rules for <input> tags."""

def actions_for_input(attributes):
    """Return possible actions for an <input> element."""
    actions = []
    input_type = attributes.get("type", "").lower()
    input_class = attributes.get("class", "").lower()

    if attributes.get("autocomplete", "").lower() == "country-name" or \
       attributes.get("id", "").lower() == "autocomplete-applicant-address-country":
        actions.append("select_country_two_steps")
    else:
        if input_type in ("text", "email", "password", "tel", ""):
            if "scwShow" in attributes.get("onfocus", "") or "scwShow" in attributes.get("onclick", ""):
                actions.append("enter_date_custom_dialog_action")
            else:
                actions.extend(["enter_text", "click"])
            if "datepicker" in input_class:
                if "readonly" in attributes and "journey" in attributes.get("name", "").lower():
                    actions.append("force_date_injection_5days_action")
                else:
                    actions.append("force_date_injection")
            if "search countries" in attributes.get("placeholder", "").lower():
                actions.append("search_and_select_country_action")
            if attributes.get("role", "").lower() == "combobox" or \
               "mat-mdc-autocomplete-trigger" in input_class or \
               attributes.get("aria-autocomplete", "").lower() == "list":
                actions.append("select_country_two_steps")
            actions.append("enter_ocr_result")
            if "hasDatepicker" in attributes.get("class", ""):
                actions.append("enter_date_dd_mm_yyyy_action")
        elif input_type in ("radio", "checkbox"):
            actions.append("click")
        else:
            actions.append("click")

    return actions
