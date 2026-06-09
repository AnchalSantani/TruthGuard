import os
import re
import string
import pickle
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRUE_PATH = os.path.join(BASE_DIR, "static", "data", "True.csv")
FAKE_PATH = os.path.join(BASE_DIR, "static", "data", "Fake.csv")


print("Loading datasets...")

true_df = pd.read_csv(TRUE_PATH)
fake_df = pd.read_csv(FAKE_PATH)

true_df["label"] = 1
fake_df["label"] = 0

true_df["text"] = (
    true_df["title"].fillna("") + " " +
    true_df["text"].fillna("")
)

fake_df["text"] = (
    fake_df["title"].fillna("") + " " +
    fake_df["text"].fillna("")
)

data = pd.concat([true_df, fake_df], ignore_index=True)

data["text"] = data["text"].apply(clean_text)

X = data["text"]
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training TF-IDF...")

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("Training Logistic Regression...")

model = LogisticRegression(
    max_iter=200,
    solver="lbfgs"
)

model.fit(X_train_tfidf, y_train)

predictions = model.predict(X_test_tfidf)

print("Accuracy:", accuracy_score(y_test, predictions))

MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "vectorizer.pkl")

with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

with open(VECTORIZER_PATH, "wb") as f:
    pickle.dump(vectorizer, f)

print("Model saved:", MODEL_PATH)
print("Vectorizer saved:", VECTORIZER_PATH)