
<div align="center">

# 📰 Truth Teller
### The AI-Powered Disinformation Defense System

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Flask](https://img.shields.io/badge/Flask-API-000000?style=for-the-badge&logo=flask&logoColor=white)
![ML](https://img.shields.io/badge/AI-Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production-success?style=for-the-badge)

<br />

<img src="https://github.com/astromanu007/truth-teller/blob/main/UI.png?raw=true" alt="Truth Teller Dashboard" width="100%" style="border-radius: 12px; box-shadow: 0px 5px 15px rgba(0,0,0,0.15);">

<br />
<br />

[**🚀 Launch Live Demo**](https://news-truth-checker.lovable.app/)
·
[**⚙️ Backend API Docs**](https://truth-teller-backend-production.up.railway.app)
·
[**🐛 Report a Bug**](https://github.com/astromanu007/truth-teller/issues)

</div>

---

## 🔍 Problem Statement
In the digital age, misinformation spreads 6x faster than factual news. Manual fact-checking cannot keep pace with the volume of content generated daily. **Truth Teller** solves this by automating the verification process using advanced Natural Language Processing (NLP).

## ✨ Key Features
**Truth Teller** is not just a model; it is a full-stack engineering solution.

### 🧠 **Intelligent Analysis**
* **Hybrid NLP Engine:** Uses TF-IDF Vectorization combined with a Passive Aggressive Classifier for high-dimensional text analysis.
* **Real-Time Inference:** Delivers prediction results in **< 200ms**.
* **Confidence Quantification:** Returns a precise probability score (e.g., *98.5% confidence*), not just a binary output.

### 🖥️ **Production-Grade UI/UX**
* **Responsive Architecture:** Fully optimized for Desktop, Tablet, and Mobile via Tailwind CSS.
* **Visual Feedback:** Dynamic color grading (Green for Real, Red for Fake) for immediate cognitive recognition.
* **Clean Input Stream:** Large-context text area capable of processing full-length articles or short headlines.

### ⚙️ **Robust Backend Engineering**
* **RESTful API Standard:** Stateless architecture ensuring easy scaling.
* **CORS Enabled:** Secure cross-origin resource sharing for third-party integrations.
* **Health Monitoring:** Dedicated `/health` endpoint for uptime checks.

---

## 🛠️ Technology Stack
Built with industry-standard tools for reliability and scale.

| Category | Technologies |
| :--- | :--- |
| **Frontend** | ![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB) ![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white) ![Tailwind](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white) ![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white) |
| **Backend** | ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=flat&logo=gunicorn&logoColor=white) |
| **Machine Learning** | ![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white) ![NLTK](https://img.shields.io/badge/NLTK-NLP-blue?style=flat) |
| **DevOps & Cloud** | ![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=flat&logo=railway&logoColor=white) ![Lovable](https://img.shields.io/badge/Lovable-Platform-ff0000?style=flat) ![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white) |

---

## 📐 System Architecture

The application follows a **Decoupled Microservices Pattern**. The React frontend communicates with the Python ML backend via JSON over HTTPS.

```mermaid
graph TD
    User["👤 End User"] -->|1. Input News| UI["⚛️ React UI"]
    UI -->|2. POST /predict| API["🐍 Flask API"]
    
    subgraph Backend ["Backend Processing"]
        API -->|3. Clean Text| NLP["🧹 Preprocessing"]
        NLP -->|4. Vectorize| TFIDF["🧮 TF-IDF"]
        TFIDF -->|5. Predict| MODEL["🧠 PassiveAggressive"]
    end
    
    MODEL -->|6. JSON Response| UI
    UI -->|7. Render Result| User
    
    %% Styles
    classDef react fill:#61DAFB,stroke:#333,stroke-width:2px,color:black;
    classDef flask fill:#000,stroke:#fff,stroke-width:2px,color:white;
    classDef ml fill:#F7931E,stroke:#333,stroke-width:2px,color:white;
    
    class UI react;
    class API flask;
    class MODEL ml;

```

---

## 📊 Performance Analytics

The model was trained and tested on a dataset of **~20,000 news articles** (ISOT Fake News Dataset).

### 🏆 Test Set Results (8,978 Samples)

| Metric | Score | Definition |
| --- | --- | --- |
| **Accuracy** | **99.89%** | Overall correctness of the model. |
| **Precision** | **1.00** | Accuracy of positive predictions. |
| **Recall** | **1.00** | Ability to find all positive instances. |
| **F1-Score** | **1.00** | Harmonic mean of Precision and Recall. |

### 📉 Confusion Matrix

*A visual representation of the model's reliability.*

|  | **Predicted REAL** | **Predicted FAKE** |
| --- | --- | --- |
| **Actual REAL** | **4,687** ✅ | 8 ❌ |
| **Actual FAKE** | 2 ❌ | **4,281** ✅ |

> **Analysis:** The model only misclassified 10 articles out of nearly 9,000, demonstrating exceptional capability in distinguishing linguistic patterns between legitimate journalism and fabricated stories.

---

## 🔌 API Reference

Integrate Truth Teller into your own applications.

#### Base URL: `https://truth-teller-backend-production.up.railway.app`

### `POST /predict`

Classifies a text string.

**Request Body:**

```json
{
  "text": "Breaking: Aliens have landed in Times Square and are demanding pizza."
}

```

**Response:**

```json
{
  "success": true,
  "prediction": "FAKE",
  "confidence": 99.2,
  "processed_timestamp": "2023-10-27T10:00:00Z"
}

```

---

## 🏎️ Local Installation

Want to run this locally? Follow these steps.

1. **Clone the Repo**
```bash
git clone [https://github.com/astromanu007/truth-teller.git](https://github.com/astromanu007/truth-teller.git)
cd truth-teller

```


2. **Start Backend**
```bash
cd truth-teller\public\fake-news-backend
pip install -r requirements.txt
python app.py

```

---

## 👤 Author

**Mr. Manish Dhatrak** *National Innovator | AI & ML Researcher*

I am passionate about leveraging Artificial Intelligence to solve complex societal problems.

---

<div align="center">
<sub>Built with precision. Deployed with passion. © 2025 Truth Teller.</sub>
</div>

```

```
