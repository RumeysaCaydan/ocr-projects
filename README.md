# OCR Projects Portfolio 🚀

This repository documents my journey in mastering **Optical Character Recognition (OCR)** technologies using Python. It includes practical implementations ranging from basic image-to-text conversion to automated document parsing using Computer Vision techniques.

## 🛠 Tech Stack
* **Language:** Python 3.x
* **OCR Engine:** Tesseract-OCR v5.0
* **Libraries:** * `pytesseract` (OCR Wrapper)
    * `opencv-python` (Image Preprocessing)
    * `re` (Regular Expressions for Information Extraction)

##  Project Modules

### 1. ID Card Reader (`id_card_reader`)
Automated extraction of personal information from Turkish Identity Cards.
* **Features:** Extracts **TC Identity Number** and **Surname**.
* **Techniques:** Grayscale conversion for noise reduction & Regex pattern matching.

### 2. Invoice & Receipt Scanner (`02_Invoice_Scanner`)
A tool to parse shopping receipts or invoices to extract financial data.
* **Features:** Automatically identifies the **Date** and **Total Amount**.
* **Techniques:** cv2.threshold (Binary Thresholding) to handle low-quality/faded receipt images.

### 3. Basic OCR
Foundational scripts to test Tesseract engine configuration and basic image-to-text conversion.

##  Installation & Usage

1.  **Install Tesseract-OCR:**
    Download and install the Tesseract executable for your OS.

2.  **Install Python Dependencies:**
    ```bash
    pip install opencv-python pytesseract
    ```

3.  **Run the Scripts:**
    Navigate to the project folder and run the python scripts:
    ```bash
    python id_reader.py
    ```

---
*Developed by Rumeysa Caydan*
