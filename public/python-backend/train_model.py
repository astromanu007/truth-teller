"""
Fake News Detection - Model Training Script
============================================
This script trains a PassiveAggressiveClassifier on fake news data
and saves the trained model and TF-IDF vectorizer for inference.

Usage: python train_model.py
"""

import os
import re
import string
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import nltk

# Download required NLTK data
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

# Configuration
DATA_PATH = 'data/news.csv'
MODEL_PATH = 'model/fake_news_model.pkl'
VECTORIZER_PATH = 'model/tfidf_vectorizer.pkl'
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Get English stopwords
STOP_WORDS = set(stopwords.words('english'))


def clean_text(text):
    """
    Preprocess text for ML model:
    - Convert to lowercase
    - Remove punctuation
    - Remove numbers
    - Remove stopwords
    - Remove extra whitespace
    
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


def load_and_prepare_data(data_path):
    """
    Load and prepare the fake news dataset.
    Expected columns: 'text' and 'label'
    
    Args:
        data_path (str): Path to the CSV file
    
    Returns:
        tuple: (features, labels)
    """
    print(f"Loading data from {data_path}...")
    
    # Load dataset
    df = pd.read_csv(data_path)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nLabel distribution:\n{df['label'].value_counts()}")
    
    # Handle missing values
    df = df.dropna(subset=['text', 'label'])
    
    # Clean text data
    print("\nCleaning text data...")
    df['cleaned_text'] = df['text'].apply(clean_text)
    
    # Remove empty texts after cleaning
    df = df[df['cleaned_text'].str.len() > 0]
    
    print(f"Final dataset size: {len(df)} samples")
    
    return df['cleaned_text'].values, df['label'].values


def train_model(X, y):
    """
    Train the fake news detection model.
    
    Args:
        X (array): Text features
        y (array): Labels
    
    Returns:
        tuple: (trained_model, vectorizer, test_data)
    """
    print("\n" + "="*50)
    print("TRAINING MODEL")
    print("="*50)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=TEST_SIZE, 
        random_state=RANDOM_STATE,
        stratify=y
    )
    
    print(f"\nTraining samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    
    # Initialize TF-IDF Vectorizer
    print("\nFitting TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=10000,       # Maximum vocabulary size
        ngram_range=(1, 2),       # Use unigrams and bigrams
        min_df=2,                 # Minimum document frequency
        max_df=0.95,              # Maximum document frequency
        sublinear_tf=True         # Apply sublinear tf scaling
    )
    
    # Fit and transform training data
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"Vocabulary size: {len(vectorizer.vocabulary_)}")
    print(f"TF-IDF matrix shape: {X_train_tfidf.shape}")
    
    # Initialize and train classifier
    print("\nTraining PassiveAggressiveClassifier...")
    model = PassiveAggressiveClassifier(
        max_iter=1000,
        random_state=RANDOM_STATE,
        C=1.0,                    # Regularization parameter
        tol=1e-3                  # Tolerance for stopping criterion
    )
    
    model.fit(X_train_tfidf, y_train)
    
    # Evaluate model
    print("\n" + "="*50)
    print("MODEL EVALUATION")
    print("="*50)
    
    y_pred = model.predict(X_test_tfidf)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    return model, vectorizer, (X_test, y_test)


def save_model(model, vectorizer, model_path, vectorizer_path):
    """
    Save trained model and vectorizer to disk.
    
    Args:
        model: Trained classifier
        vectorizer: Fitted TF-IDF vectorizer
        model_path (str): Path to save model
        vectorizer_path (str): Path to save vectorizer
    """
    # Create model directory if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    # Save model
    print(f"\nSaving model to {model_path}...")
    joblib.dump(model, model_path)
    
    # Save vectorizer
    print(f"Saving vectorizer to {vectorizer_path}...")
    joblib.dump(vectorizer, vectorizer_path)
    
    # Verify saved files
    model_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
    vectorizer_size = os.path.getsize(vectorizer_path) / (1024 * 1024)  # MB
    
    print(f"\nModel size: {model_size:.2f} MB")
    print(f"Vectorizer size: {vectorizer_size:.2f} MB")
    print("\n✓ Model and vectorizer saved successfully!")


def main():
    """Main training pipeline."""
    print("\n" + "="*60)
    print(" FAKE NEWS DETECTION - MODEL TRAINING")
    print("="*60)
    
    # Check if data file exists
    if not os.path.exists(DATA_PATH):
        print(f"\n❌ Error: Data file not found at {DATA_PATH}")
        print("\nPlease ensure you have a news.csv file in the data/ folder")
        print("with columns: 'text' (article content) and 'label' (FAKE/REAL)")
        print("\nYou can download datasets from:")
        print("- https://www.kaggle.com/c/fake-news/data")
        print("- https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset")
        return
    
    # Load and prepare data
    X, y = load_and_prepare_data(DATA_PATH)
    
    # Train model
    model, vectorizer, test_data = train_model(X, y)
    
    # Save model and vectorizer
    save_model(model, vectorizer, MODEL_PATH, VECTORIZER_PATH)
    
    print("\n" + "="*60)
    print(" TRAINING COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Run the Flask app: python app.py")
    print("2. Open http://localhost:5000 in your browser")
    print("3. Test with news articles!")


if __name__ == "__main__":
    main()
