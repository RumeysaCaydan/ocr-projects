#libraries
from pathlib import Path
import cv2
import pytesseract
import re
import json

# Set Tesseract executable path (Windows users)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define input and output directories
INPUT_DIR = Path("input_image")
OUTPUT_JSON_DIR = Path("json_output")

OUTPUT_JSON_DIR.mkdir(exist_ok=True)

# Regex patterns
DATE_REGEX = r"\b(\d{2}[./-]\d{2}[./-]\d{2,4})\b"
MONEY_REGEX = r"(\d{1,4}(?:[.\s]\d{3})*,\d{2})"


def enhance_image(gray_image):
    """
    Improve image contrast and resolution to increase OCR accuracy.
    Applies CLAHE and resizing.
    """
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray_image)
    enhanced = cv2.resize(enhanced, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    return enhanced


def perform_ocr(image):
    """
    Perform OCR using Tesseract with Turkish language support.
    """
    config = "--oem 3 --psm 6"
    return pytesseract.image_to_string(image, lang="tur", config=config)


def extract_date(text):
    """
    Extract date from OCR text using regex.
    """
    match = re.search(DATE_REGEX, text)
    return match.group(1) if match else None


def convert_to_float(value):
    """
    Convert various number formats to float.
    Handles:
    - 1.234,56
    - 21 421.90
    - 21421,90
    """
    value = value.replace(" ", "")

    if "," in value:
        value = value.replace(".", "").replace(",", ".")
    else:
        value = value.replace(",", "")

    try:
        return float(value)
    except:
        return 0


def extract_total(text):
    """
    Extract total amount from OCR text.
    Priority:
    1. Line containing 'TOPLAM'
    2. Fallback: largest monetary value above threshold
    Includes correction for OCR digit merging errors.
    """
    lines = text.splitlines()

    # 1️⃣ Search for 'TOPLAM' line first
    for i, line in enumerate(lines):
        if "TOPLAM" in line.upper():
            match = re.search(MONEY_REGEX, line)
            if match:
                return match.group(1)

            if i + 1 < len(lines):
                match_next = re.search(MONEY_REGEX, lines[i + 1])
                if match_next:
                    return match_next.group(1)

    # 2️⃣ Fallback: take largest monetary value
    values = re.findall(MONEY_REGEX, text)
    if not values:
        return None

    numeric_values = [convert_to_float(v) for v in values]

    # Ignore very small values (VAT etc.)
    filtered = [v for v in numeric_values if v > 10]

    if not filtered:
        return None

    largest = max(filtered)

    # 🔥 Fix common OCR digit-merging issue (e.g., 21421,90 instead of 214,21)
    if largest > 5000:
        largest = largest / 100

    return f"{largest:.2f}".replace(".", ",")


# Main processing loop
for image_path in sorted(INPUT_DIR.glob("*")):

    if image_path.suffix.lower() not in [".png", ".jpg", ".jpeg"]:
        continue

    image = cv2.imread(str(image_path))
    if image is None:
        continue

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    enhanced = enhance_image(gray)

    ocr_text = perform_ocr(enhanced)

    date_value = extract_date(ocr_text)
    total_value = extract_total(ocr_text)

    result = {
        "file": image_path.name,
        "date": date_value,
        "total": total_value
    }

    with open(OUTPUT_JSON_DIR / f"{image_path.stem}.json",
              "w", encoding="utf-8") as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)

    print(f"{image_path.name} -> date: {date_value} | total: {total_value}")