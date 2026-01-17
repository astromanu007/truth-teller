# Fake News Detection System

ML-powered fake news detection using PassiveAggressiveClassifier and TF-IDF vectorization.

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Prepare Dataset

Create the `data/` folder and add your `news.csv` file:

```bash
mkdir data model
```

Your `news.csv` should have these columns:
- `text`: The news article or headline content
- `label`: Either "FAKE" or "REAL"

**Recommended datasets:**
- [Kaggle Fake News Dataset](https://www.kaggle.com/c/fake-news/data)
- [Fake and Real News Dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)

### 3. Train the Model

```bash
python train_model.py
```

This will:
- Load and preprocess the data
- Train the PassiveAggressiveClassifier
- Evaluate accuracy
- Save model files to `model/`

### 4. Run the Web App

```bash
python app.py
```

Open http://localhost:5000 in your browser.

## 📁 Project Structure

```
fake-news-detection/
│
├── model/
│   ├── fake_news_model.pkl      # Trained classifier
│   └── tfidf_vectorizer.pkl     # Fitted vectorizer
│
├── data/
│   └── news.csv                 # Training dataset
│
├── templates/
│   └── index.html               # Web interface
│
├── static/
│   └── style.css                # Custom styles
│
├── train_model.py               # Model training script
├── app.py                       # Flask API server
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/predict` | POST | Classify news text |
| `/health` | GET | Health check |
| `/api/info` | GET | API information |

### POST /predict

**Request:**
```json
{
    "text": "Your news article or headline here"
}
```

**Response:**
```json
{
    "success": true,
    "prediction": "FAKE",
    "confidence": 87.5,
    "message": "Analysis complete"
}
```

## 🧠 Model Details

- **Algorithm:** PassiveAggressiveClassifier
- **Vectorization:** TF-IDF (max 10,000 features, unigrams + bigrams)
- **Preprocessing:** Lowercase, remove punctuation/stopwords/URLs/numbers
- **Train/Test Split:** 80/20

## 🔧 Configuration

Edit these constants in the scripts:

**train_model.py:**
```python
DATA_PATH = 'data/news.csv'
MODEL_PATH = 'model/fake_news_model.pkl'
TEST_SIZE = 0.2
```

**app.py:**
```python
HOST = '0.0.0.0'
PORT = 5000
DEBUG = True
```

## 📊 Expected Accuracy

With a good quality dataset (10,000+ samples), expect:
- **Accuracy:** 92-96%
- **Precision:** 91-95%
- **Recall:** 92-96%

## 🚢 Deployment

For production:

1. Set `DEBUG = False` in app.py
2. Use gunicorn:
   ```bash
   gunicorn app:app -w 4 -b 0.0.0.0:5000
   ```
3. Deploy to Heroku, Railway, or any Python hosting platform

## 📝 License

MIT License - Free for personal and commercial use.
