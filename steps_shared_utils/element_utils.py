# E:\CRM\automation_project\steps_shared_utils\element_utils.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_element(driver, primary_selector_type, primary_selector_value, fallback_selectors=None, wait_time=5, extracted_info=None):
    """
    Attempts to locate an element using a primary selector, manual fallback selectors,
    and additional automatically generated selectors from the extracted_info.
    
    Parameters:
      driver: The Selenium WebDriver instance.
      primary_selector_type: A string indicating the type of the primary selector ("xpath" or "css").
      primary_selector_value: The primary selector string.
      fallback_selectors: (Optional) A list of tuples [(selector_type, selector_value), ...]
                          that will be attempted in order if the primary selector fails.
      wait_time: Maximum time in seconds to wait for each selector (default is 5 seconds).
      extracted_info: (Optional) A dictionary with extra information about the element as extracted
                      during selection. Expected keys include:
                        - "xpath"
                        - "css_selector"
                        - "tag_name"
                        - "attributes" (may include "id", "name", "placeholder", etc.)
                        - "dataset" (the element.dataset object)
                        - "parent_info": A dictionary that may contain "css_selector"
                        - "text_content"
    
    Returns:
      The first WebElement found using one of the provided or derived selectors.
    
    Raises:
      Exception if no element is found using any of the provided or derived selectors.
    
    Example:
      extracted = {
          "xpath": "//*[@id='email']",
          "css_selector": "input#email",
          "tag_name": "input",
          "attributes": {
              "id": "email",
              "name": "email",
              "placeholder": "Email"
          },
          "dataset": {},
          "parent_info": { "css_selector": "div#emailContainer" },
          "text_content": ""
      }
      
      element = find_element(
          driver,
          "xpath", "//*[@id='email']",
          fallback_selectors=[
              ("css", "input[placeholder='Email']"),
              ("css", "div#email > app-text-input input[placeholder='Email']")
          ],
          wait_time=5,
          extracted_info=extracted
      )
    """
    # Start with the primary selector.
    selectors = [(primary_selector_type, primary_selector_value)]
    if fallback_selectors:
        selectors.extend(fallback_selectors)
    
    # If extra info is provided, generate additional selectors.
    if extracted_info:
        tag = extracted_info.get("tag_name", "").lower()
        attributes = extracted_info.get("attributes", {})
        dataset = extracted_info.get("dataset", {})
        parent_info = extracted_info.get("parent_info", {})
        text_content = extracted_info.get("text_content", "").strip()
        
        # 1. Use extracted XPath.
        if "xpath" in extracted_info and extracted_info["xpath"]:
            candidate = ("xpath", extracted_info["xpath"])
            if not any(sel[0].lower() == "xpath" and sel[1] == candidate[1] for sel in selectors):
                selectors.append(candidate)
        
        # 2. Use extracted CSS selector.
        if "css_selector" in extracted_info and extracted_info["css_selector"]:
            candidate = ("css", extracted_info["css_selector"])
            if not any(sel[0].lower() == "css" and sel[1] == candidate[1] for sel in selectors):
                selectors.append(candidate)
        
        # 3. If the element has an ID attribute, build a CSS selector from it.
        if attributes.get("id"):
            candidate = ("css", f"{tag}#{attributes['id']}")
            if not any(sel[0].lower() == "css" and sel[1] == candidate[1] for sel in selectors):
                selectors.append(candidate)
        
        # 4. If the element has a name attribute, build a CSS selector from it.
        if attributes.get("name"):
            candidate = ("css", f"{tag}[name='{attributes['name']}']")
            if not any(sel[0].lower() == "css" and sel[1] == candidate[1] for sel in selectors):
                selectors.append(candidate)
        
        # 5. If the element has a placeholder attribute, build a CSS selector from it.
        if attributes.get("placeholder"):
            candidate = ("css", f"{tag}[placeholder='{attributes['placeholder']}']")
            if not any(sel[0].lower() == "css" and sel[1] == candidate[1] for sel in selectors):
                selectors.append(candidate)
        
        # 6. (Optional) Build a composite selector from dataset attributes.
        # Here, we build a selector that includes all data-* attributes.
        if dataset:
            data_selectors = []
            for key, value in dataset.items():
                data_selectors.append(f"[data-{key}='{value}']")
            if data_selectors:
                candidate = ("css", f"{tag}{''.join(data_selectors)}")
                if not any(sel[0].lower() == "css" and sel[1] == candidate[1] for sel in selectors):
                    selectors.append(candidate)
        
        # 7. Use parent's CSS selector if available to build a composite selector.
        if parent_info and parent_info.get("css_selector") and tag:
            candidate = ("css", f"{parent_info['css_selector']} {tag}")
            if not any(sel[0].lower() == "css" and sel[1] == candidate[1] for sel in selectors):
                selectors.append(candidate)
        
        # 8. If text_content is provided and the element is not an input or textarea, add an XPath based on text.
        if text_content and tag not in ["input", "textarea"]:
            candidate = ("xpath", f"//*[contains(normalize-space(text()), '{text_content}')]")
            if not any(sel[0].lower() == "xpath" and sel[1] == candidate[1] for sel in selectors):
                selectors.append(candidate)
    
    # print(f"[DEBUG] find_element: Trying the following selectors in order: {selectors}")
    
    # Iterate through the list of selectors.
    for sel_type, sel_value in selectors:
        try:
            wait = WebDriverWait(driver, wait_time)
            if sel_type.lower() == 'xpath':
                element = wait.until(EC.presence_of_element_located((By.XPATH, sel_value)))
            elif sel_type.lower() == 'css':
                element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel_value)))
            else:
                raise ValueError(f"Unsupported selector_type: {sel_type}")
            # print(f"[DEBUG] find_element: Found element using {sel_type} '{sel_value}'.")
            return element
        except Exception as e:
            print(f"[DEBUG] find_element: No element found using {sel_type} '{sel_value}': {e}")
    
    raise Exception("find_element: No element found using the provided selectors.")
