import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img=cv2.imread("deneme.png")

text = pytesseract.image_to_string(img, lang="tur")
print(text)
