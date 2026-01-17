"""
Fake News Detection - Flask API
===============================
Classifies news articles as FAKE or REAL using a trained
PassiveAggressiveClassifier and TF-IDF vectorizer.

Run:
    python app.py
"""
print("🔥 app.py LOADED FROM:", __file__)

import os
import re
import string
import joblib
import numpy as np
import nltk
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Download stopwords
nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

# ---------------- APP SETUP ----------------
app = Flask(__name__)
CORS(app)

MODEL_PATH = "model/fake_news_model.pkl"
VECTORIZER_PATH = "model/tfidf_vectorizer.pkl"

STOP_WORDS = set(stopwords.words("english"))

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

print("✅ MODEL LOADED:", model is not None)
print("✅ VECTORIZER LOADED:", vectorizer is not None)


# ---------------- LOAD MODEL ----------------
def load_model():
    global model, vectorizer

    if model is None:
        model = joblib.load(MODEL_PATH)

    if vectorizer is None:
        vectorizer = joblib.load(VECTORIZER_PATH)


# ---------------- TEXT CLEANING ----------------
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


# ---------------- PREDICTION LOGIC ----------------
def predict_news(text):
    cleaned_text = clean_text(text)

    if not cleaned_text:
        return {"error": "Empty text after preprocessing"}

    text_tfidf = vectorizer.transform([cleaned_text])
    prediction = model.predict(text_tfidf)[0]

    decision = model.decision_function(text_tfidf)[0]
    confidence = 1 / (1 + np.exp(-abs(decision)))
    confidence = round(confidence * 100, 2)

    return {
        "prediction": prediction,
        "confidence": confidence
    }


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Accept JSON or HTML form
        data = request.get_json(silent=True)

        if data and "text" in data:
            text = data["text"]
        else:
            text = request.form.get("text")

        if not text or len(text.strip()) < 10:
            return jsonify({
                "success": False,
                "error": "Please enter a valid news article (min 10 characters)."
            }), 400

        prediction, confidence = predict_news(text)

        if prediction is None:
            return jsonify({
                "success": False,
                "error": "Unable to process text."
            }), 400

        return jsonify({
            "success": True,
            "prediction": prediction,
            "confidence": confidence
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "vectorizer_loaded": vectorizer is not None
    })


# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" FAKE NEWS DETECTION API")
    print("=" * 60)

    try:
        load_model()
    except Exception as e:
        print(f"❌ {e}")
        exit(1)

    print("\n🚀 Server running at: http://localhost:5000")
    print("📡 Prediction API: POST /predict\n")

    app.run(host="0.0.0.0", port=5000, debug=True)
