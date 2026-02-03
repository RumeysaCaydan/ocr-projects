import cv2
import pytesseract
import re

# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_invoice_data(image_path):
    # 1. Load Image
    img = cv2.imread(image_path)

    if img is None:
        print(f"Error: Image not found at {image_path}")
        return

    # 2. Preprocessing
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Thresholding (Critical for receipts to remove noise/shadows)
    # Pixels darker than 150 become black, others white
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # 3. OCR Process
    print("Processing invoice...")
    # 'tur' for Turkish characters, 'eng' for general keywords
    raw_text = pytesseract.image_to_string(thresh, lang='tur+eng')

    print("\n--- RAW OCR OUTPUT ---")
    print(raw_text)
    print("----------------------\n")

    # 4. Extract Data using Regex

    # A) Extract Date (Format: DD.MM.YYYY or DD/MM/YYYY)
    date_pattern = r'\d{2}[./]\d{2}[./]\d{4}'
    date_match = re.search(date_pattern, raw_text)

    # B) Extract Total Amount
    # Looks for 'TOPLAM' or 'TOTAL' followed by a number (e.g., 120,50 or 120.50)
    amount_pattern = r'(TOPLAM|GENEL TOPLAM|TOTAL)\s*[:]*\s*(\d+[.,]\d{2})'
    amount_match = re.search(amount_pattern, raw_text, re.IGNORECASE)

    # 5. Display Results
    print("--- EXTRACTED INVOICE DATA ---")

    if date_match:
        print(f" Date: {date_match.group()}")
    else:
        print(" Date not found.")

    if amount_match:
        # group(2) contains only the number part
        print(f"Total Amount: {amount_match.group(2)}")
    else:
        print(" Total amount not found.")


if __name__ == "__main__":
    # Ensure 'invoice_sample.png' exists in the directory
    extract_invoice_data("invoice_sample.png")