"""Action rules for <span>, <div>, and <button> tags."""

def actions_for_span_div_button(attributes, text_content=""):
    """Return possible actions for a <span>, <div>, or <button> element."""
    actions = []
    cls = attributes.get("class", "").lower()

 codex/locate-function-get-possible-actions-for-element-hgoy6o
    if "mat-mdc-select-value" in cls:
        actions.append("select_mat_option_action")
    elif "ant-select-selector" in cls:
        actions.append("select_country_two_steps")
=======
    if "ant-select-selector" in cls:
        actions.append("select_country_two_steps")
 codex/locate-function-get-possible-actions-for-element-yt2weh
    elif "mat-mdc-select-value" in cls or "mat-select-value" in cls:
        actions.append("select_mat_option")
=======
 main
 main
    elif "modal-content" in cls:
        actions.append("dismiss_modal")
    else:
        actions.append("click")
        if "selected-flag" in cls:
            actions.append("select_country_prefix")
        actions.append("capture_request_number")
        actions.append("click")
        txt = text_content.lower() if text_content else ""
        if "all countries" in txt or "frequently selected" in txt or "search" in txt:
            actions.append("search_and_select_country_action")

    return actions
