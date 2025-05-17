# E:\CRM\automation_project\steps_shared_actions\ocr_captcha_action.py

import os
import subprocess
import sys
import time
import io
import uuid
import base64
import tkinter as tk
from PIL import Image, ImageTk
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from steps_shared_utils.element_utils import find_element
from steps_shared_actions.alert_handler import handle_unexpected_alerts

EXECUTION_CONTEXT = {}

def ocr_captcha_action(driver, selector_type, selector_value, step_value, step):
    """
    ocr_captcha_action(driver, selector_type, selector_value, step_value, step)

    1) Finds the <img> element by (selector_type, selector_value).
    2) Scrolls it into view (if needed).
    3) Takes an element screenshot (Selenium 4+).
    4) Runs PaddleOCR externally.
    5) Shows a correction popup.
    6) Stores final text in EXECUTION_CONTEXT["last_ocr_result"].
    """

    print("[DEBUG] ocr_captcha_action started.")
    # 1) Handle leftover/unexpected alerts
    handle_unexpected_alerts(driver, action="dismiss")

    # 2) Locate the <img> element
    image_el = find_element(driver, selector_type, selector_value)

    # 3) Scroll the element into view, in case it's off-screen
    driver.execute_script("arguments[0].scrollIntoView(true);", image_el)
    time.sleep(0.5)  # small pause to let the page settle

    # 4) Directly screenshot this element (Selenium 4+ attribute)
    png_data = image_el.screenshot_as_png

    # Convert to a PIL image
    cropped_img = Image.open(io.BytesIO(png_data))

    # 5) Convert PIL -> base64 -> run external OCR
    b64_str = _pil_image_to_base64(cropped_img)
    recognized_text = _run_paddle_ocr_in_subprocess(b64_str)
    print(f"[DEBUG] Subprocess recognized => {recognized_text}")

    # 6) Show correction popup
    final_text = _show_ocr_correction_dialog(cropped_img, recognized_text)
    EXECUTION_CONTEXT["last_ocr_result"] = final_text
    print(f"[DEBUG] Stored OCR result => {final_text}")

    print("[DEBUG] ocr_captcha_action done.")


def _pil_image_to_base64(pil_image):
    """
    Convert a PIL image to base64-encoded PNG string for passing to PaddleOCR script.
    """
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def _run_paddle_ocr_in_subprocess(image_b64: str) -> str:
    """
    Calls paddle_ocr_api.py with --image_b64 argument.
    Returns recognized text from stdout or "" on error.
    """
    paddle_ocr_script = r"E:\CRM\passport_reader\ocr_validation_training\paddle_ocr_api.py"
    cmd = [sys.executable, paddle_ocr_script, "--image_b64", image_b64]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[ERROR] paddle_ocr_api.py failed: {result.stderr.strip()}")
            return ""
        return result.stdout.strip()
    except Exception as e:
        print(f"[ERROR] Subprocess call failed: {e}")
        return ""


def _show_ocr_correction_dialog(pil_image, recognized_text):
    """
    Shows a Tk popup with the cropped captcha image + recognized text + correction field.
    The user can confirm or correct the text, then it is stored.
    """
    root = tk.Tk()
    root.withdraw()

    dialog = tk.Toplevel(root)
    dialog.title("OCR Correction")
    dialog.attributes("-topmost", True)

    tk_image = ImageTk.PhotoImage(pil_image)
    img_label = tk.Label(dialog, image=tk_image)
    img_label.image = tk_image
    img_label.pack(pady=5)

    recognized_var = tk.StringVar(value=recognized_text)
    recognized_entry = tk.Entry(dialog, textvariable=recognized_var, state='readonly', width=40)
    recognized_entry.pack(pady=2)

    correction_var = tk.StringVar(value="")
    correction_entry = tk.Entry(dialog, textvariable=correction_var, width=40)
    correction_entry.pack(pady=2)

    final_text_dict = {"value": recognized_text}

    def on_valid_ocr():
        final_text_dict["value"] = recognized_text
        _save_paddleocr_training_data(pil_image, recognized_text)
        dialog.destroy()

    def on_use_correction():
        corr = correction_var.get().strip()
        if corr:
            final_text_dict["value"] = corr
            _save_paddleocr_training_data(pil_image, corr)
        else:
            final_text_dict["value"] = recognized_text
            _save_paddleocr_training_data(pil_image, recognized_text)
        dialog.destroy()

    btn_frame = tk.Frame(dialog)
    btn_frame.pack(pady=5)

    valid_btn = tk.Button(btn_frame, text="Valid OCR", command=on_valid_ocr, width=12)
    valid_btn.pack(side=tk.LEFT, padx=5)

    correction_btn = tk.Button(btn_frame, text="Use Correction", command=on_use_correction, width=12)
    correction_btn.pack(side=tk.LEFT, padx=5)

    def run_dialog():
        dialog.wait_window(dialog)

    run_dialog()
    root.destroy()

    return final_text_dict["value"]


def _save_paddleocr_training_data(pil_image, final_text):
    """
    Save the captcha image + final recognized/corrected text to DB for training.
    """
    import os
    import uuid
    save_folder = r"E:\CRM\training_data\paddleocr\datasets\en\images\train"
    os.makedirs(save_folder, exist_ok=True)

    image_uuid = str(uuid.uuid4())
    filename = f"{image_uuid}.png"
    full_path = os.path.join(save_folder, filename)

    pil_image.save(full_path, format="PNG")
    print(f"[DEBUG] Saved training image => {full_path}, text => {final_text}")

    try:
        from steps_shared_utils.paddleocr_db_manager import get_paddleocr_connection
        with get_paddleocr_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO paddleocr_training_data (image_path, corrected_text, language, image_name)
                    VALUES (%s, %s, %s, %s)
                """, (save_folder, final_text, "en", filename))
        print("[DEBUG] Inserted new row into paddleocr_training_data.")
    except Exception as e:
        print("[ERROR] Failed to insert into paddleocr_training_data:", e)
