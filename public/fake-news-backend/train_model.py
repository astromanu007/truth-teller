"""
Fake News Detection - Model Training Script
=========================================
Trains a PassiveAggressiveClassifier using True.csv and Fake.csv
and saves the trained model and TF-IDF vectorizer.
"""

import os
import re
import string
import pandas as pd
import joblib
import nltk

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Download stopwords
nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

# ---------------- CONFIG ----------------
TRUE_DATA_PATH = "data/True.csv"
FAKE_DATA_PATH = "data/Fake.csv"

MODEL_PATH = "model/fake_news_model.pkl"
VECTORIZER_PATH = "model/tfidf_vectorizer.pkl"

TEST_SIZE = 0.2
RANDOM_STATE = 42
STOP_WORDS = set(stopwords.words("english"))


# ---------------- CLEAN TEXT ----------------
def clean_text(text):
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", "", text)

    words = text.split()
    words = [w for w in words if w not in STOP_WORDS]

    text = " ".join(words)
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ---------------- LOAD DATA ----------------
def load_and_prepare_data():
    print("Loading datasets...")

    if not os.path.exists(TRUE_DATA_PATH) or not os.path.exists(FAKE_DATA_PATH):
        raise FileNotFoundError("True.csv or Fake.csv not found in data/ folder")

    true_df = pd.read_csv(TRUE_DATA_PATH)
    fake_df = pd.read_csv(FAKE_DATA_PATH)

    # Assign labels
    true_df["label"] = 1   # REAL
    fake_df["label"] = 0   # FAKE

    # Combine title + text
    true_df["content"] = true_df["title"] + " " + true_df["text"]
    fake_df["content"] = fake_df["title"] + " " + fake_df["text"]

    # Merge datasets
    df = pd.concat([true_df, fake_df], axis=0)
    df = df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

    print(f"Total samples: {len(df)}")
    print("Label distribution:")
    print(df["label"].value_counts())

    # Clean text
    print("Cleaning text...")
    df["content"] = df["content"].apply(clean_text)

    df = df[df["content"].str.len() > 0]

    X = df["content"]
    y = df["label"]

    return X, y


# ---------------- TRAIN MODEL ----------------
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    vectorizer = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,
        sublinear_tf=True
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    model = PassiveAggressiveClassifier(
        max_iter=1000,
        random_state=RANDOM_STATE,
        tol=1e-3
    )

    model.fit(X_train_tfidf, y_train)

    y_pred = model.predict(X_test_tfidf)

    print("\nAccuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    return model, vectorizer


# ---------------- SAVE MODEL ----------------
def save_model(model, vectorizer):
    os.makedirs("model", exist_ok=True)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print("\nModel saved to:", MODEL_PATH)
    print("Vectorizer saved to:", VECTORIZER_PATH)


# ---------------- MAIN ----------------
def main():
    print("\nFAKE NEWS DETECTION - TRAINING STARTED\n")

    X, y = load_and_prepare_data()
    model, vectorizer = train_model(X, y)
    save_model(model, vectorizer)

    print("\nTRAINING COMPLETE")
    print("Next: run → python app.py")


if __name__ == "__main__":
    main()
