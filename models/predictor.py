import os
import re
import string
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "vectorizer.pkl")


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


print("Loading saved model...")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

print("Model loaded successfully!")


def check_news(news_text):
    cleaned = clean_text(news_text)

    tfidf_text = vectorizer.transform([cleaned])

    prediction = model.predict(tfidf_text)[0]
    probability = model.predict_proba(tfidf_text)[0][prediction]

    label = "✅ Real News" if prediction == 1 else "❌ Fake News"

    return f"{label} (Confidence: {probability*100:.2f}%)"