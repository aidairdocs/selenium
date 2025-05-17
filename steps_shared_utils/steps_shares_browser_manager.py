# E:\CRM\automation_project\steps_shared_utils\steps_shares_browser_manager.py

import os
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def init_browser(headless=False):
    """
    init_browser(headless=False)

    Initializes a Firefox WebDriver, optionally in headless mode.
    Returns a Selenium WebDriver instance.
    """
    print("[DEBUG browser_manager.init_browser] Called with headless=", headless)
    try:
        options = Options()
        options.headless = headless

        # Set the capability to automatically accept unexpected alerts.
        options.set_capability("unhandledPromptBehavior", "accept")
        
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        print("[DEBUG browser_manager.init_browser] Successfully initialized Firefox WebDriver.")
        return driver
    except Exception as e:
        print(f"[ERROR browser_manager.init_browser] Failed to initialize Firefox WebDriver: {e}")
        sys.exit(1)  # or raise

def close_browser(driver):
    """
    close_browser(driver)

    Closes the given WebDriver instance, logging debug output.
    """
    print("[DEBUG browser_manager.close_browser] Called.")
    try:
        driver.quit()
        print("[DEBUG browser_manager.close_browser] Firefox WebDriver closed.")
    except Exception as e:
        print(f"[ERROR browser_manager.close_browser] Failed to close Firefox WebDriver: {e}")
