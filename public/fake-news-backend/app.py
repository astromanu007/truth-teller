"""
Truth Teller – Fake News Detection Backend
------------------------------------------
Flask API that classifies news text as FAKE or REAL
using a trained PassiveAggressiveClassifier and TF-IDF vectorizer.
"""

import os
import re
import string
import joblib
import numpy as np
import nltk
from flask import Flask, request, jsonify
from flask_cors import CORS

# -------------------------------------------------
# NLTK SETUP
# -------------------------------------------------
nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

STOP_WORDS = set(stopwords.words("english"))

# -------------------------------------------------
# PATH SETUP (IMPORTANT FOR RAILWAY)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "fake_news_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "model", "tfidf_vectorizer.pkl")

# -------------------------------------------------
# APP INIT
# -------------------------------------------------
app = Flask(__name__)
CORS(app)

# -------------------------------------------------
# LOAD MODEL & VECTORIZER (EAGER LOADING)
# -------------------------------------------------
print("🔥 app.py loaded from:", __file__)

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

print("✅ MODEL LOADED:", model is not None)
print("✅ VECTORIZER LOADED:", vectorizer is not None)

# -------------------------------------------------
# TEXT CLEANING
# -------------------------------------------------
def clean_text(text: str) -> str:
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

# -------------------------------------------------
# PREDICTION LOGIC
# -------------------------------------------------
def predict_news(text: str) -> dict:
    cleaned_text = clean_text(text)

    if not cleaned_text:
        return {"error": "Text is empty after preprocessing"}

    text_tfidf = vectorizer.transform([cleaned_text])

    prediction = model.predict(text_tfidf)[0]
    decision = model.decision_function(text_tfidf)[0]

    confidence = 1 / (1 + np.exp(-abs(decision)))
    confidence = round(confidence * 100, 2)

    return {
        "prediction": prediction,
        "confidence": confidence
    }

# -------------------------------------------------
# ROUTES
# -------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Truth Teller Backend API is running"
    })

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True)

        if not data or "text" not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'text' field in request body"
            }), 400

        text = data["text"]

        if not text or len(text.strip()) < 10:
            return jsonify({
                "success": False,
                "error": "Please enter at least 10 characters"
            }), 400

        result = predict_news(text)

        if "error" in result:
            return jsonify({
                "success": False,
                "error": result["error"]
            }), 400

        return jsonify({
            "success": True,
            "prediction": result["prediction"],
            "confidence": result["confidence"]
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "vectorizer_loaded": vectorizer is not None
    })

# -------------------------------------------------
# LOCAL ENTRY POINT (NOT USED BY RAILWAY)
# -------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
