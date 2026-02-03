import cv2
import pytesseract
import re

# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_id_info(image_path):
    # 1. Load Image
    img = cv2.imread(image_path)

    if img is None:
        print(f"Error: Image not found at {image_path}")
        return

    # 2. Preprocessing (Grayscale)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. OCR Process (Turkish language support)
    print("Processing image...")
    extracted_text = pytesseract.image_to_string(gray, lang='tur')

    print("\n--- RAW OCR OUTPUT ---")
    print(extracted_text)
    print("----------------------\n")

    # 4. Extract Specific Data using Regex

    # Pattern for Turkish ID Number (11 digits)
    tc_match = re.search(r'\d{11}', extracted_text)

    # Pattern for Surname (Assumes uppercase word after 'Soyadı')
    surname_match = re.search(r'Soyadı\s*[:]*\s*([A-ZÇĞİÖŞÜ]+)', extracted_text, re.IGNORECASE)

    # 5. Display Results
    print("--- EXTRACTED DATA ---")

    if tc_match:
        print(f"TC Identity No: {tc_match.group()}")
    else:
        print(" TC Identity No not found.")

    if surname_match:
        print(f" Surname: {surname_match.group(1)}")
    else:
        print(" Surname not found.")


if __name__ == "__main__":
    # Ensure 'id_sample.png' exists in the same directory
    extract_id_info("id_sample.png")