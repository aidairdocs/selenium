import os
import time
from PIL import Image
from io import BytesIO
from steps_shared_actions.alert_handler import handle_unexpected_alerts

def full_page_screenshot_action(driver, selector_type, selector_value, step_value, step):
    """
    Takes a full-page screenshot by scrolling vertically and stitching slices.
    
    Improvements:
    1) Each iteration, we re-check the scrollHeight in case the page grows.
    2) For the final slice, we do a partial offset if needed.
    3) Ensures we don't miss the very bottom of the page.

    If step_value is empty, defaults to "E:\\CRM\\screenshots\\full_page_screenshot.png".
    Example usage in a step: "insert_value": "E:\\CRM\\screenshots\\my_page.png"
    """

    print("[DEBUG] full_page_screenshot_action started.")
    handle_unexpected_alerts(driver, action="dismiss")

    # 1) Decide output path
    default_path = r"E:\CRM\screenshots\full_page_screenshot.png"
    screenshot_path = step_value.strip() if step_value.strip() else default_path
    print(f"[DEBUG] Will save screenshot to '{screenshot_path}'")

    # 2) Store original window state
    original_size = driver.get_window_size()

    # 3) Measure the page size
    #   We'll do this in a loop if the page might dynamically load more content.
    original_width = driver.execute_script("return document.body.scrollWidth")
    total_height = driver.execute_script("return document.body.scrollHeight")

    # 4) Set window width to match the page width (so we capture horizontally)
    driver.set_window_size(original_width, 900)  # start with a moderate height
    time.sleep(1)

    # We'll re-check the final needed height in each slice
    slices = []
    current_scroll = 0
    slice_count = 0

    while True:
        slice_count += 1

        # 4a) Scroll to current position
        driver.execute_script(f"window.scrollTo(0, {current_scroll});")
        time.sleep(0.3)  # let the browser render

        # 4b) Possibly re-check total page height if site loads new content
        new_total_height = driver.execute_script("return document.body.scrollHeight")
        # we'll set total_height to the max so we always capture the expanded height
        if new_total_height > total_height:
            total_height = new_total_height
            print(f"[DEBUG] Page grew to new scrollHeight={total_height} at slice #{slice_count}")

        # 4c) Capture the screenshot of the current viewport
        png_data = driver.get_screenshot_as_png()
        screenshot_im = Image.open(BytesIO(png_data))
        slices.append((current_scroll, screenshot_im))

        # 4d) Move down by viewport height
        viewport_height = driver.execute_script("return window.innerHeight")
        next_scroll = current_scroll + viewport_height

        if next_scroll >= total_height:
            # This means the next slice would exceed the page bottom
            # We do one last partial slice if needed, then break
            # Actually let's do the partial approach:

            # If the page is bigger than the last scroll we took,
            # let's do one final scroll to (0, total_height - viewport_height) if that is bigger than current_scroll
            final_pos = max(total_height - viewport_height, current_scroll)
            if final_pos > current_scroll:
                driver.execute_script(f"window.scrollTo(0, {final_pos});")
                time.sleep(0.3)
                png_data = driver.get_screenshot_as_png()
                screenshot_im = Image.open(BytesIO(png_data))
                slices.append((final_pos, screenshot_im))
                print(f"[DEBUG] Captured final partial slice at scroll={final_pos}")

            break
        else:
            # Not at the bottom yet, keep going
            current_scroll = next_scroll

    # 5) Now we know the final total_height. Let's build the big image
    print(f"[DEBUG] Building final image with width={original_width}, height={total_height}")
    final_img = Image.new("RGB", (original_width, total_height), (255, 255, 255))

    # For each slice, paste it in at the correct offset
    for (scroll_y, im_slice) in slices:
        final_img.paste(im_slice, (0, scroll_y))

    # 6) Create folder if needed
    dir_part = os.path.dirname(screenshot_path)
    if dir_part:
        os.makedirs(dir_part, exist_ok=True)

    # 7) Save final stitched image
    final_img.save(screenshot_path)
    print(f"[DEBUG] Full-page screenshot saved to '{screenshot_path}'.")

    # 8) Return to a maximized window (or original)
    driver.maximize_window()
    # or to restore exactly:
    # driver.set_window_size(original_size["width"], original_size["height"])

    print("[DEBUG] full_page_screenshot_action done.")
