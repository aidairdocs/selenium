# actions/date/enter_date_custom.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from steps_shared_utils.parse_ymd import parse_ymd
from steps_shared_utils.element_utils import find_element

def enter_date_custom_dialog_action(driver, selector_type, selector_value, step_value, step):
    """
    A specialized custom datepicker approach for the site that uses:
      - input#bdate (onclick="scwShow(this,event)")
      - table#scw as the pop-up
      - select#scwMonths for month
      - select#scwYears for year
      - td.scwCells with text content for day

    'step_value' should be "YYYY-MM-DD". We'll parse it into (yyyy, mm, dd).

    Example usage:
      step_value = "1991-01-24"  # parse_ymd => yyyy=1991, mm=1, dd=24
    """

    # 1) Parse the user-provided date "YYYY-MM-DD"
    yyyy, mm, dd = parse_ymd(step_value)
    print(f"[DEBUG] enter_date_custom_dialog_action: date to pick => {yyyy}-{mm:02d}-{dd:02d}")

    # 2) Click the main input/field to open the date window
    date_field = find_element(driver, selector_type, selector_value)
    date_field.click()
    print("[DEBUG] Clicked the date input (#bdate) to open the scw calendar window.")

    # 3) Wait for the table#scw (the overlay) to appear
    #    We'll wait up to 10 seconds. Adjust if site is slow.
    try:
        wait = WebDriverWait(driver, 10)
        calendar_table = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "table#scw"))
        )
        print("[DEBUG] Found the custom date table #scw, presumably displayed now.")
    except Exception as e:
        print(f"[ERROR] Could not find table#scw overlay within 10s: {e}")
        return  # or raise

    # 4) Pick the year (via select#scwYears)
    try:
        year_select = driver.find_element(By.CSS_SELECTOR, "select#scwYears")
        year_select.click()  # open the dropdown
        # We'll pick the correct option by text matching the integer year
        select_obj = Select(year_select)
        # Convert yyyy to string, e.g. "1991"
        select_obj.select_by_visible_text(str(yyyy))
        print(f"[DEBUG] Picked year {yyyy} from #scwYears.")
    except Exception as e:
        print(f"[ERROR] Failed picking year {yyyy} in scwYears: {e}")
        return

    # 5) Pick the month (via select#scwMonths)
    try:
        month_select = driver.find_element(By.CSS_SELECTOR, "select#scwMonths")
        month_select.click()
        # The select has text "JanuaryFebruaryMarch...", so we map mm to name:
        MONTH_NAMES = {
            1: "January", 2: "February", 3: "March", 4: "April",
            5: "May", 6: "June", 7: "July", 8: "August",
            9: "September", 10: "October", 11: "November", 12: "December"
        }
        month_name = MONTH_NAMES.get(mm, "")
        select_obj = Select(month_select)
        select_obj.select_by_visible_text(month_name)
        print(f"[DEBUG] Picked month '{month_name}' from #scwMonths.")
    except Exception as e:
        print(f"[ERROR] Failed picking month {mm} in scwMonths: {e}")
        return

    # 6) Pick the day (td.scwCells with text content=dd)
    try:
        # We'll do a simple text match. The day cells are <td class="scwCells"> with text = day number
        # e.g. 24 => "24"
        day_xpath = f"//td[( @class='scwCells' or @class='scwCellsWeekend' ) and text()='{dd}']"
        # day_xpath = f"//td[contains(@class,'scwCells') and text()='{dd}']"
        day_cell = driver.find_element(By.XPATH, day_xpath)
        day_cell.click()
        print(f"[DEBUG] Picked day {dd} by clicking the cell with text()='{dd}'.")
    except Exception as e:
        print(f"[ERROR] Failed picking day {dd}: {e}")
        return

    # 7) The calendar presumably closes automatically after picking a day
    #    If not, you might need to click a 'Close' button or do more steps
    print(f"[INFO] Successfully selected date {yyyy}-{mm:02d}-{dd:02d} in the custom scw calendar.")

