<div align="center">

  <br />
  <h1>📰 Truth Teller</h1>
  <h3>ML-Powered Fake News Detection System</h3>

  <p>
    An end-to-end machine learning platform that classifies news articles as <b>REAL</b> or <b>FAKE</b> with 99% accuracy. Built with React, Python/Flask, and Scikit-Learn.
  </p>

  <p>
    <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/react-18.0+-61DAFB.svg" alt="React Version">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome">
    <a href="https://news-truth-checker.lovable.app/">
      <img src="https://img.shields.io/badge/Live_Demo-Online-success?style=for-the-badge&logo=vercel" alt="Live Demo" />
    </a>
  </p>

  <h4>
    <a href="https://news-truth-checker.lovable.app/">View Demo</a>
    <span> · </span>
    <a href="https://truth-teller-backend-production.up.railway.app/docs">API Docs</a>
    <span> · </span>
    <a href="#-getting-started">Run Locally</a>
  </h4>
</div>

<br />

<details>
  <summary><b>Table of Contents</b></summary>
  <ol>
    <li><a href="#-about-the-project">About The Project</a></li>
    <li><a href="#-system-architecture">System Architecture</a></li>
    <li><a href="#-tech-stack">Tech Stack</a></li>
    <li><a href="#-model-performance">Model Performance</a></li>
    <li><a href="#-getting-started">Getting Started</a></li>
    <li><a href="#-api-reference">API Reference</a></li>
    <li><a href="#-roadmap">Roadmap</a></li>
  </ol>
</details>

---

## 📖 About The Project

![App Screenshot](https://via.placeholder.com/800x400.png?text=Place+Your+App+Screenshot+Here)
*(Replace the link above with a screenshot or GIF of your UI)*

Fake news spreads rapidly across digital platforms, leading to public misinformation and social polarization. Manual fact-checking is unscalable against the velocity of modern media.

**Truth Teller** solves this by providing a real-time, AI-driven veracity check. It ingests news text, processes it through a refined NLP pipeline, and utilizes a **Passive Aggressive Classifier** to determine credibility with high precision.

### Key Features
* **🔎 Real-time Analysis:** Instant classification (<100ms latency).
* **📊 Confidence Scoring:** Transparency on how certain the model is.
* **🌐 Full-Stack Deployment:** Production-ready React frontend and Flask backend.
* **📉 Lightweight:** Optimized for low-memory environments using sparse matrices.

---

## 🧠 System Architecture

The system follows a decoupled client-server architecture. The Machine Learning pipeline is wrapped in a Flask API, serving predictions to a modern React client.

```mermaid
graph TD
    User[👤 User] -->|Input Text| UI[⚛️ React Frontend]
    UI -->|POST /predict| API[🐍 Flask API]
    
    subgraph "Backend Engine"
        API -->|Raw Text| Pre[🧹 Preprocessing]
        Pre -->|Cleaned Text| Vect[🧮 TF-IDF Vectorizer]
        Vect -->|Sparse Matrix| Model[🤖 Passive Aggressive Classifier]
        Model -->|Result| Logic[⚙️ Probability Logic]
    end
    
    Logic -->|JSON Response| UI
    UI -->|Visual Feedback| User
