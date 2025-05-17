# E:\CRM\automation_project\step_builder_selenium_flow\step_builder_create_step_helpers.py
"""
Holds helper functions for creating a new step: 
 - prompt_for_action_type
 - prompt_for_value
 - prompt_for_description
 - element_selection_gui
 - element_selection_title_gui (for label/ title)
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
from step_builder_selenium_flow.step_builder_element_selection_manager import enable_element_selection, get_selected_element_info
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoAlertPresentException

# Import action rules for different HTML tags
from step_builder_selenium_flow.element_action_rules import (
    input_rules,
    select_rules,
    textarea_rules,
    anchor_rules,
    image_rules,
    span_div_button_rules,
    ul_rules,
    default_rules,
)



def element_selection_gui(driver):
    """
    Activates real-time element selection in the open browser,
    then shows a small window instructing the user to Ctrl+right-click 
    (or just right-click) an element in the browser.

    Once the user clicks 'OK' here, we retrieve the selected info from the page.
    Then we display a confirmation pop-up with the tag_name, attributes, etc.
    If user confirms, we return (True, element_info).
    If user cancels, we return (False, None).
    """
    print("[DEBUG] element_selection_gui() with real-time highlighting.")
    
    # 1) Enable selection for the user to pick an element
    enable_element_selection(driver)

    # Show instructions
    root = tk.Tk()
    root.title("Select Element in Browser")
    root.geometry("900x900")

    label_text = (
        "Hover elements in the browser to see them highlighted.\n"
        "CTRL + Right-click on the desired element to select.\n\n"
        "When finished, click 'OK' below."
    )
    label = tk.Label(root, text=label_text, justify=tk.LEFT)
    label.pack(pady=10)

    def on_ok():
        root.destroy()

    tk.Button(root, text="OK", command=on_ok).pack(pady=10)
    root.mainloop()

    # 2) After user closes the window, read the selectedElementInfo
    element_info = get_selected_element_info(driver)
    if element_info:
        print("[DEBUG] element_selection_gui: user selected an element with info:", element_info)

        # 2.1) Show a confirmation pop-up with more details
        confirmed = confirm_element_selection(element_info)
        if confirmed:
            print("[DEBUG] User confirmed selected element.")
            return True, element_info
        else:
            print("[DEBUG] User cancelled after seeing element details.")
            return False, None
    else:
        print("[DEBUG] No element selected (user might not have right-clicked).")
        return False, None


def confirm_element_selection(element_info):
    """
    Shows a scrollable pop-up summarizing the chosen element
    (tag_name, attributes, etc.), so that huge text won't
    push the GUI buttons out of view.
    Returns True if user confirms, False otherwise.
    """
    root = tk.Tk()
    root.title("Confirm Element Selection")
    root.geometry("900x600")  # set a fixed size (optional)
    root.resizable(True, True)  # let them resize if they wish

    # Build a textual summary
    tag_name = element_info.get("tag_name", "")
    text_content = element_info.get("text_content", "")
    xpath = element_info.get("xpath", "")
    css_selector = element_info.get("css_selector", "")
    attributes = element_info.get("attributes", {})
    options = element_info.get("options", [])  # if you already extracted them

    attr_str = "\n".join([f"{k}={v}" for k,v in attributes.items()])

    # Possibly also format the options if you extracted them:
    options_str = ""
    if options:
        # For example: "AFGHANISTAN\nALBANIA\nANDORRA"
        options_str = "\n".join([f" - {opt['text']}" for opt in options])

    info_text = (
        f"You selected an element with these details:\n\n"
        f"Tag Name: {tag_name}\n"
        f"Text Content: {text_content}\n\n"
        f"XPath: {xpath}\n"
        f"CSS: {css_selector}\n\n"
        f"Attributes:\n{attr_str}\n\n"
    )
    if options_str:
        info_text += f"Discovered OPTIONS:\n{options_str}\n\n"

    # Use a ScrolledText for the big text
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=25)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    text_area.insert(tk.END, info_text)
    text_area.config(state=tk.DISABLED)  # make read-only

    def on_confirm():
        root.user_response = True
        root.destroy()

    def on_cancel():
        root.user_response = False
        root.destroy()

    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    confirm_btn = tk.Button(button_frame, text="Confirm", command=on_confirm, width=12)
    confirm_btn.pack(side=tk.LEFT, padx=5)

    cancel_btn = tk.Button(button_frame, text="Cancel", command=on_cancel, width=12)
    cancel_btn.pack(side=tk.LEFT, padx=5)

    root.user_response = False
    root.mainloop()

    return root.user_response


def prompt_for_value(action_type):
    """
    If action_type is 'goto', we ask for a URL.
    If action_type is 'enter_text', we ask for text input.
    If action_type is 'select_option', etc. 
    Returns the string the user entered or "" if cancelled.
    """
    print("[DEBUG] prompt_for_value() called for action_type=", action_type)

    root = tk.Tk()
    root.title("Enter Value")
    root.geometry("900x900")

    value_var = tk.StringVar()
    label_text = f"Enter the value for action '{action_type}':"
    label = tk.Label(root, text=label_text)
    label.pack(pady=10)

    entry = tk.Entry(root, textvariable=value_var, width=40)
    entry.pack()

    def on_ok():
        root.destroy()

    ok_btn = tk.Button(root, text="OK", command=on_ok)
    ok_btn.pack(pady=5)

    root.mainloop()
    result = value_var.get()
    print(f"[DEBUG] User entered value='{result}' for action='{action_type}'.")
    return result


def prompt_for_description():
    """
    Simple prompt for a textual description of the new step.
    """
    print("[DEBUG] prompt_for_description() called.")
    root = tk.Tk()
    root.title("Step Description")
    root.geometry("900x900")

    desc_var = tk.StringVar()
    label = tk.Label(root, text="Enter a description for this step:")
    label.pack(pady=10)

    entry = tk.Entry(root, textvariable=desc_var, width=50)
    entry.pack()

    def on_ok():
        root.destroy()

    ok_btn = tk.Button(root, text="OK", command=on_ok)
    ok_btn.pack(pady=5)

    root.mainloop()
    result = desc_var.get()
    print(f"[DEBUG] Step description: {result}")
    return result


def element_selection_title_gui(driver):
    """
    Similar to element_selection_gui, but instructs user to select the 'title' or 
    label near the main element. We'll store that text in 'selector_title'.
    """
    print("[DEBUG] element_selection_title_gui() for selecting label/title.")
    
    # 1) Enable selection
    enable_element_selection(driver)

    root = tk.Tk()
    root.title("Select Title/Label in Browser")
    root.geometry("900x900")

    label_text = (
        "Please hover over the text or label near your chosen element.\n"
        "CTRL + Right-click to select it.\n\n"
        "When finished, click 'OK'."
    )
    label = tk.Label(root, text=label_text, justify=tk.LEFT)
    label.pack(pady=10)

    def on_ok():
        root.destroy()

    tk.Button(root, text="OK", command=on_ok).pack(pady=10)
    root.mainloop()

    title_info = get_selected_element_info(driver)
    if title_info:
        print("[DEBUG] element_selection_title_gui: user selected title with info:", title_info)
        # We might also confirm the selection just like confirm_element_selection(title_info) if needed
        return True, title_info
    else:
        print("[DEBUG] No title selected (user might not have right-clicked).")
        return False, None


def ask_if_skip_element_selection():
    """
    Asks the user if they want to skip element selection 
    (i.e. create a 'goto' or 'manual' step) or pick an element.
    Returns 'goto', 'manual', 'click_safe_area', 'full_screenshot', or 'element'. (the last meaning they want to pick an element).
    """
    root = tk.Tk()
    root.title("Step Type")
    root.geometry("900x900")
    root.resizable(False, False)

    choice_var = tk.StringVar(value="element")  # default

    label_text = (
        "Which type of step do you want?\n\n"
        " - Select an Element (requires picking an element)\n"
        " - Goto (no element)\n"
        " - Manual Action (no element)\n"
        " - Click Safe Area (no element; used to dismiss pop-ups)\n"
        " - Full Page Screenshot (no element)\n"
        " - Goto from Email (no element)\n"
        " - Dismiss Modal (no element)\n"
        " - Safe Action (manual with checklist; for sensitive operations)\n"
    )
    label = tk.Label(root, text=label_text, wraplength=350, justify=tk.LEFT)
    label.pack(pady=10)

    # Radiobuttons:
    tk.Radiobutton(root, text="Select an Element", variable=choice_var, value="element").pack(anchor=tk.W)
    tk.Radiobutton(root, text="Goto (no element)", variable=choice_var, value="goto").pack(anchor=tk.W)
    tk.Radiobutton(root, text="Manual Action (no element)", variable=choice_var, value="manual").pack(anchor=tk.W)
    tk.Radiobutton(root, text="Click Safe Area (no element)", variable=choice_var, value="click_safe_area").pack(anchor=tk.W)
    tk.Radiobutton(root, text="Full Page Screenshot (no element)", variable=choice_var, value="full_screenshot").pack(anchor=tk.W)
    tk.Radiobutton(root, text="Goto from Email (no element)", variable=choice_var, value="goto_from_email").pack(anchor=tk.W)
    tk.Radiobutton(root, text="Dismiss Modal (no element)", variable=choice_var, value="dismiss_modal").pack(anchor=tk.W)
    tk.Radiobutton(root, text="Safe Action (manual with checklist)", variable=choice_var, value="safe_action").pack(anchor=tk.W)

    def on_ok():
        root.destroy()

    ok_btn = tk.Button(root, text="OK", command=on_ok)
    ok_btn.pack(pady=5)

    root.mainloop()
    result = choice_var.get()
    print(f"[DEBUG] ask_if_skip_element_selection => '{result}'")
    return result

# // ----------------------------------------------------------------
# // Here you add the options Selection by selected element
# // ----------------------------------------------------------------


# Mapping from tag name to handler function
TAG_HANDLERS = {
    "input": input_rules.actions_for_input,
    "select": select_rules.actions_for_select,
    "textarea": textarea_rules.actions_for_textarea,
    "a": anchor_rules.actions_for_anchor,
    "img": image_rules.actions_for_image,
    "span": span_div_button_rules.actions_for_span_div_button,
    "div": span_div_button_rules.actions_for_span_div_button,
    "button": span_div_button_rules.actions_for_span_div_button,
    "ul": ul_rules.actions_for_ul,
}


def get_possible_actions_for_element(element_info):
    """Return a list of possible action names for the given element."""
    print("[DEBUG] get_possible_actions_for_element(...) called.")

    tag_name = element_info.get("tag_name", "").lower()
    attributes = element_info.get("attributes", {})
    text_content = element_info.get("text_content", "")

    handler = TAG_HANDLERS.get(tag_name, default_rules.actions_for_default)

    if tag_name in ("span", "div", "button"):
        actions = handler(attributes, text_content)
    else:
        actions = handler(attributes)

    return actions



def prompt_for_element_action(possible_actions):
    """
    Shows a GUI with the possible actions that the user can choose from,
    based on the element's tag/attributes.

    Returns the chosen action, or None if cancelled.
    """
    print("[DEBUG] prompt_for_element_action(...) called.")

    root = tk.Tk()
    root.title("Select Action for Element")
    root.geometry("900x900")
    root.resizable(False, False)

    chosen_action = tk.StringVar(value="")

    label = tk.Label(root, text="Choose an action for this element:", font=("Arial", 12))
    label.pack(pady=10)

    for action in possible_actions:
        tk.Radiobutton(root, text=action, variable=chosen_action, value=action).pack(anchor=tk.W)

    def on_ok():
        if not chosen_action.get():
            messagebox.showwarning("No Selection", "Please select an action.")
            return
        root.destroy()

    ok_btn = tk.Button(root, text="OK", command=on_ok)
    ok_btn.pack(pady=5)

    cancel_btn = tk.Button(root, text="Cancel", command=lambda: [chosen_action.set(""), root.destroy()])
    cancel_btn.pack(pady=5)

    root.mainloop()

    result = chosen_action.get()
    if not result:
        print("[INFO] No action selected for element (user cancelled).")
        return None
    print(f"[DEBUG] User chose action_type={result} for the selected element.")
    return result

def handle_unexpected_alerts(driver, action="dismiss"):
    """
    Attempts to switch to any open alert. If found, either 'dismiss' or 'accept' it.
    This function can be called at the start of each step to clear stray alerts.
    """
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"[DEBUG] Found unexpected alert: {alert_text}")
        if action == "dismiss":
            alert.dismiss()
            print("[DEBUG] Alert dismissed.")
        else:
            alert.accept()
            print("[DEBUG] Alert accepted.")
        return True  # indicates an alert was found and handled
    except NoAlertPresentException:
        # No alert is present, do nothing
        return False
    except Exception as e:
        print(f"[WARNING] Error handling unexpected alert: {e}")
        return False

# ------------------------------------------------------
# SELECT ACTION
# ------------------------------------------------------

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def extract_select_options(driver, element_info):
    """
    extract_select_options(driver, element_info)

    One Uniform Workflow:
    ---------------------
    1) The user *always* opens the drop-down on the page FIRST (physically clicks it),
       so all child items are visible in the DOM.
    2) Then the user uses the highlight tool to select the parent element.

    With this approach, it doesn't matter if the drop-down is a standard <select>
    or a custom/JS-based drop-down that loads <li> or <div> items dynamically.
    Because the user has opened it, the child nodes (options) are already in the DOM,
    and we can extract them via BFS or Selenium's Select class.

    Steps in Code:
    -------------
    - If the tag is 'select', we use Selenium's Select(...) to gather <option> items.
    - Otherwise, we do a BFS to find <li> or <option> child elements, capturing their text.
    - All discovered items are stored in element_info["options"] as a list of dicts:
         [ { "text": "...", "value": "..." }, ... ].

    Important:
    ----------
    - If the user does NOT open the drop-down, this code might find zero items,
      because the site hasn't populated them in the DOM.
    - No forced clicks are performed here. 
    """

    print("[DEBUG extract_select_options] Called with element_info:", element_info)

    # Ensure we have a place to store discovered options
    element_info["options"] = []

    # (A) Handle a standard <select> if tag_name == "select"
    tag_name = element_info.get("tag_name", "").lower()
    if tag_name == "select":
        print("[DEBUG extract_select_options] Detected a <select> tag.")
        xpath = element_info.get("xpath", "")
        if not xpath:
            print("[WARNING extract_select_options] No xpath for <select>. Cannot locate element.")
            return

        try:
            print(f"[DEBUG extract_select_options] Locating <select> via XPATH: {xpath}")
            select_webel = driver.find_element(By.XPATH, xpath)
            sel = Select(select_webel)

            opt_list = []
            for opt in sel.options:
                opt_text = opt.text.strip()
                opt_value = opt.get_attribute("value") or ""
                opt_list.append({"text": opt_text, "value": opt_value})

            element_info["options"] = opt_list
            print("[DEBUG extract_select_options] Found <option> items in standard <select>:", opt_list)
            return  # Done for <select>
        except (NoSuchElementException, TimeoutException) as e:
            print(f"[WARNING extract_select_options] Failed to locate <select> element: {e}")
            return
        except Exception as e:
            print(f"[WARNING extract_select_options] Error retrieving <select> options: {e}")
            return

    # (B) Not a <select>: BFS approach for a custom or JS-based drop-down
    print("[DEBUG extract_select_options] Not a <select>. Attempting BFS for a custom drop-down.")
    xpath = element_info.get("xpath", "")
    if not xpath:
        print("[WARNING extract_select_options] No xpath found for custom drop-down. BFS might fail.")
        return

    try:
        parent_el = driver.find_element(By.XPATH, xpath)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"[WARNING extract_select_options] BFS: Could not locate parent element: {e}")
        return
    except Exception as e:
        print(f"[WARNING extract_select_options] BFS: Unexpected error locating parent: {e}")
        return

    print("[DEBUG extract_select_options] Starting BFS to find <li> or <option> child items...")
    from collections import deque
    queue = deque([parent_el])
    found_options = []

    while queue:
        current_node = queue.popleft()
        try:
            # Gather direct children
            children = current_node.find_elements(By.XPATH, "./*")
        except Exception as e:
            print(f"[DEBUG extract_select_options] BFS: Could not find children: {e}")
            continue

        for child in children:
            try:
                tag = child.tag_name.lower()
                text_content = child.text.strip()

                # We treat <li> or <option> as potential "options" (example logic)
                if tag in ("li", "option"):
                    val_attr = child.get_attribute("value") or ""
                    found_options.append({"text": text_content, "value": val_attr})

                # If there's a chance <div class="dropdown-item" is used, you can add:
                # if 'dropdown-item' in child.get_attribute('class'): ...
                # found_options.append(...)

                # Enqueue for deeper BFS
                queue.append(child)
            except Exception as sub_e:
                print(f"[DEBUG extract_select_options] BFS: error reading child node: {sub_e}")
                continue

    element_info["options"] = found_options
    print("[DEBUG extract_select_options] BFS discovered custom drop-down items:", found_options)

    # If found_options is empty, it may mean the user did not open the drop-down
    # or the site uses a more complex shadow DOM approach requiring special logic.
