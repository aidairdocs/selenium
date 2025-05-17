# E:\CRM\automation_project\step_builder_selenium_flow\step_builder_element_selection_manager.py

import json
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException

def enable_element_selection(driver):
    """
    Injects JavaScript into the browser that highlights elements on hover
    and captures their info upon right-click. This version closes selection
    mode right after the user right-clicks an element (or presses Escape).

    NOTE: This function does not write anything to the database directly.
    Instead, it sets 'window.selectedElementInfo' in the browser, which
    can then be retrieved with 'get_selected_element_info(driver)'.
    """
    print("[DEBUG] enable_element_selection() called: resetting window.selectedElementInfo to null.")
    driver.execute_script("window.selectedElementInfo = null;")
    driver.execute_script("""
    (function() {
        if (!window.elementSelectionEnabled) {
            window.elementSelectionEnabled = true;
            var prevElement = null;

            function mouseMoveHandler(event) {
                var element = event.target;
                if (prevElement && prevElement !== element) {
                    prevElement.style.outline = '';
                }
                if (element) {
                    element.style.outline = '2px solid red';
                    prevElement = element;
                }
            }

            function contextMenuHandler(event) {
                // Prevent the default context menu
                event.preventDefault();
                event.stopPropagation();
                var element = event.target;
                if (element) {
                    var rect = element.getBoundingClientRect();
                    var elementInfo = {
                        tag_name: element.tagName.toLowerCase(),
                        text_content: element.textContent.trim(),
                        xpath: getElementXPath(element),
                        css_selector: getCssSelector(element),
                        position: {
                            x: rect.left + window.scrollX,
                            y: rect.top + window.scrollY,
                            width: rect.width,
                            height: rect.height
                        },
                        attributes: getElementAttributes(element),
                        dataset: element.dataset,              // NEW: Captures all data-* attributes
                        parent_info: getParentInfo(element),     // Parent element info
                        computed_styles: {                       // Computed styles
                            display: window.getComputedStyle(element).display,
                            visibility: window.getComputedStyle(element).visibility,
                            position: window.getComputedStyle(element).position
                        },
                        outer_html: element.outerHTML,           // Outer HTML of the element
                        inner_html: element.innerHTML            // NEW: Inner HTML of the element
                    };                    
                    window.selectedElementInfo = elementInfo;
                    exitSelectionMode();
                }
            }

            function keyDownHandler(event) {
                if (event.key === 'Escape') {
                    exitSelectionMode();
                }
            }

            function exitSelectionMode() {
                if (prevElement) {
                    prevElement.style.outline = '';
                }
                document.removeEventListener('mousemove', mouseMoveHandler, true);
                document.removeEventListener('contextmenu', contextMenuHandler, true);
                document.removeEventListener('keydown', keyDownHandler, true);
                window.elementSelectionEnabled = false;
            }

            // Attach our event listeners
            document.addEventListener('mousemove', mouseMoveHandler, true);
            document.addEventListener('contextmenu', contextMenuHandler, true);
            document.addEventListener('keydown', keyDownHandler, true);

            // Utility function to compute an XPath
            function getElementXPath(element) {
                if (element.id) {
                    return '//*[@id="' + element.id + '"]';
                }
                var paths = [];
                while (element && element.nodeType === Node.ELEMENT_NODE) {
                    var index = 0;
                    var hasSameTagSiblings = false;
                    var sibling = element.previousSibling;
                    while (sibling) {
                        if (
                            sibling.nodeType !== Node.DOCUMENT_TYPE_NODE &&
                            sibling.nodeName === element.nodeName
                        ) {
                            hasSameTagSiblings = true;
                            index++;
                        }
                        sibling = sibling.previousSibling;
                    }
                    var tagName = element.nodeName.toLowerCase();
                    var pathIndex = hasSameTagSiblings ? '[' + (index + 1) + ']' : '';
                    paths.unshift(tagName + pathIndex);

                    if (element.assignedSlot) {
                        element = element.assignedSlot;
                    } else if (element.parentNode) {
                        element = element.parentNode;
                    } else if (element.host) {
                        element = element.host;
                    } else {
                        break;
                    }
                }
                return paths.length ? '//' + paths.join('/') : null;
            }

            // Compute a CSS selector for an element
            function getCssSelector(element) {
                var paths = [];
                while (element && element.nodeType === Node.ELEMENT_NODE) {
                    var selector = element.nodeName.toLowerCase();
                    if (element.id) {
                        selector += '#' + element.id;
                        paths.unshift(selector);
                        break;
                    } else {
                        var sib = element, nth = 1;
                        while (sib = sib.previousElementSibling) {
                            if (sib.nodeName.toLowerCase() == selector)
                                nth++;
                        }
                        if (nth != 1)
                            selector += ":nth-of-type(" + nth + ")";
                    }
                    paths.unshift(selector);
                    if (element.assignedSlot) {
                        element = element.assignedSlot;
                    } else if (element.parentNode) {
                        element = element.parentNode;
                    } else if (element.host) {
                        element = element.host;
                    } else {
                        break;
                    }
                }
                return paths.join(" > ");
            }

            function getElementAttributes(element) {
                var attrs = {};
                for (var i = 0; i < element.attributes.length; i++) {
                    var attr = element.attributes[i];
                    attrs[attr.name] = attr.value;
                }
                return attrs;
            }
            
            // New: Function to get parent element information
            function getParentInfo(element) {
                if (element.parentElement) {
                    return {
                        tag_name: element.parentElement.tagName.toLowerCase(),
                        id: element.parentElement.id,
                        class: element.parentElement.className,
                        xpath: getElementXPath(element.parentElement),
                        css_selector: getCssSelector(element.parentElement)
                    };
                }
                return null;
            }
        }
    })();
    """)

def get_selected_element_info(driver):
    """
    Reads 'window.selectedElementInfo' from the browser's window object.
    Then, if an element was actually selected, we locate the real DOM node
    (using the XPATH from 'selectedElementInfo') and gather all HTML attributes
    to store in element_info["attributes"].

    Returns None if no element was selected, or a dict like:
    {
      'tag_name': 'input',
      'text_content': '...',
      'xpath': '//input[2]',
      'css_selector': 'input:nth-of-type(2)',
      'position': {...},
      'attributes': {
         'id': 'title',
         'name': 'title',
         'class': 'inner_text_box_man',
         ... plus any other DOM attributes ...
      },
      'parent_info': { ... },          // New: Parent element information
      'computed_styles': { ... },      // New: Computed styles like display, visibility, position
      'outer_html': '<input ...>'      // New: Outer HTML of the element
    }
    """
    print("[DEBUG element_selection_manager.get_selected_element_info] called. Checking if user selected an element in the browser.")
    
    # 1) Retrieve the partial info from window.selectedElementInfo
    element_info = driver.execute_script("return window.selectedElementInfo;")
    if element_info:
        print("[DEBUG] Retrieved element info from browser:", element_info)
    else:
        print("[DEBUG] No element info found (user may not have right-clicked or selection mode ended).")
        return None

    # 2) Attempt to gather extended attributes from the actual DOM node if we have an XPATH
    xpath = element_info.get("xpath", "")
    if xpath:
        try:
            # Locate the real DOM element by XPATH
            web_element = driver.find_element(By.XPATH, xpath)
            
            # Use a JS snippet to enumerate *all* of its attributes
            script = r"""
            function getAllAttributes(el) {
                var attrs = {};
                for (var i = 0; i < el.attributes.length; i++) {
                    var attr = el.attributes[i];
                    attrs[attr.name] = attr.value;
                }
                return attrs;
            }
            return getAllAttributes(arguments[0]);
            """
            extended_attrs = driver.execute_script(script, web_element)
            print("[DEBUG] Gathered extended attributes from real DOM node:", extended_attrs)

            # Merge the extended attributes with what we already have
            if "attributes" not in element_info:
                element_info["attributes"] = {}
            for key, val in extended_attrs.items():
                element_info["attributes"][key] = val

        except NoSuchElementException:
            print("[WARNING] Could not locate the DOM node by the XPATH. Possibly the page changed or ephemeral element.")
        except WebDriverException as e:
            print("[WARNING] Error retrieving extended attributes:", e)
        except Exception as e:
            print("[WARNING] Unexpected error while gathering extended attributes:", e)
    else:
        print("[DEBUG] No XPATH found in element_info, cannot gather extended attributes from DOM node.")

    # 3) Return the augmented element_info with additional attributes
    return element_info
