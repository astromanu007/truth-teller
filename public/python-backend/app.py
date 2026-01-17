"""
Fake News Detection - Flask API
===============================
RESTful API for classifying news articles as FAKE or REAL
using a trained PassiveAggressiveClassifier model.

Usage: python app.py
API Endpoints:
    GET  /        - Serve the web interface
    POST /predict - Classify news text
"""

import os
import re
import string
import joblib
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import nltk

# Download required NLTK data
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Configuration
MODEL_PATH = 'model/fake_news_model.pkl'
VECTORIZER_PATH = 'model/tfidf_vectorizer.pkl'
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True

# Get English stopwords
STOP_WORDS = set(stopwords.words('english'))

# Global variables for model and vectorizer
model = None
vectorizer = None


def load_model():
    """
    Load the trained model and TF-IDF vectorizer from disk.
    This function is called once at startup.
    """
    global model, vectorizer
    
    print("Loading model and vectorizer...")
    
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found at {MODEL_PATH}. "
            "Please run train_model.py first."
        )
    
    if not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError(
            f"Vectorizer file not found at {VECTORIZER_PATH}. "
            "Please run train_model.py first."
        )
    
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    
    print("✓ Model and vectorizer loaded successfully!")


def clean_text(text):
    """
    Preprocess text using the SAME pipeline as training.
    This ensures consistent feature extraction.
    
    Args:
        text (str): Raw text input
    
    Returns:
        str: Cleaned text
    """
    if not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Tokenize and remove stopwords
    words = text.split()
    words = [word for word in words if word not in STOP_WORDS]
    
    # Rejoin words
    text = ' '.join(words)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def predict_news(text):
    """
    Predict whether news text is FAKE or REAL.
    
    Args:
        text (str): News article or headline
    
    Returns:
        dict: Prediction result with label and confidence
    """
    # Preprocess the text
    cleaned_text = clean_text(text)
    
    if not cleaned_text:
        return {
            'error': 'Text is empty after preprocessing',
            'prediction': None,
            'confidence': None
        }
    
    # Vectorize the text
    text_tfidf = vectorizer.transform([cleaned_text])
    
    # Get prediction
    prediction = model.predict(text_tfidf)[0]
    
    # Get confidence score using decision function
    # PassiveAggressiveClassifier uses decision_function
    decision = model.decision_function(text_tfidf)[0]
    
    # Convert decision to probability-like score (0-100%)
    # Using sigmoid-like transformation
    import numpy as np
    confidence = 1 / (1 + np.exp(-abs(decision)))
    confidence = round(confidence * 100, 1)
    
    return {
        'prediction': prediction,
        'confidence': confidence,
        'cleaned_text': cleaned_text[:200] + '...' if len(cleaned_text) > 200 else cleaned_text
    }


# ============================================
# API ROUTES
# ============================================

@app.route('/')
def home():
    """Serve the main web interface."""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    API endpoint for news classification.
    
    Request Body (JSON):
        {
            "text": "News article or headline to classify"
        }
    
    Response (JSON):
        {
            "success": true,
            "prediction": "FAKE" or "REAL",
            "confidence": 85.5,
            "message": "Analysis complete"
        }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing "text" field in request body'
            }), 400
        
        text = data['text'].strip()
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Text cannot be empty'
            }), 400
        
        if len(text) < 10:
            return jsonify({
                'success': False,
                'error': 'Text is too short for accurate analysis'
            }), 400
        
        # Perform prediction
        result = predict_news(text)
        
        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
        
        return jsonify({
            'success': True,
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'message': 'Analysis complete'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'vectorizer_loaded': vectorizer is not None
    })


@app.route('/api/info')
def api_info():
    """API information endpoint."""
    return jsonify({
        'name': 'Fake News Detection API',
        'version': '1.0.0',
        'model': 'PassiveAggressiveClassifier',
        'vectorizer': 'TF-IDF',
        'endpoints': {
            '/': 'Web interface',
            '/predict': 'POST - Classify news text',
            '/health': 'GET - Health check',
            '/api/info': 'GET - API information'
        }
    })


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print(" FAKE NEWS DETECTION API")
    print("="*60)
    
    # Load model at startup
    try:
        load_model()
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        print("\nPlease run: python train_model.py")
        exit(1)
    
    print(f"\n🚀 Starting Flask server...")
    print(f"   URL: http://localhost:{PORT}")
    print(f"   API: http://localhost:{PORT}/predict")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(host=HOST, port=PORT, debug=DEBUG)
