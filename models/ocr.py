import cv2
import os
import easyocr
import re
import string

# =========================
# ✅ Text Cleaning Function
# =========================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# =========================
# ✅ Load Saved Model
# =========================
from .predictor import check_news

# =========================
# 🚀 OCR + Fake News Integration
# =========================
def ocr_and_check(img_path):
    reader = easyocr.Reader(['en'], gpu=False)

    results = reader.readtext(img_path)

    print("\n📷 OCR Extracted Text:")

    extracted_lines = []

    for _, text, _ in results:
        print(text)
        extracted_lines.append(text)

    full_text = " ".join(extracted_lines)

    print("\n📰 Fake News Prediction:")
    prediction = check_news(full_text)

    print(prediction)

    return {
        "text": full_text,
        "prediction": prediction
    }