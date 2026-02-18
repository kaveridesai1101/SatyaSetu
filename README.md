# 🛡️ VeriSense – Smart Fake News Detector

> **Check credibility. Understand truth. Think critically.**

VeriSense is an AI-powered verification platform designed to help students and researchers identify fake news, assess article credibility, and detect bias using state-of-the-art Machine Learning models.

## 🚀 Key Features

- **Multi-Model Analysis**: Combines **DeBERTa-v3** (Classification), **Sentence-BERT** (Claim Verification), and **DistilBART** (Summarization).
- **Credibility Scoring**: Generates a 0-100 trust score based on multiple signals.
- **Explainable AI (XAI)**: Uses **SHAP** to highlight exactly *why* an article is flagged as fake or real.
- **Bias & Sentiment Detection**: Identifies sensationalism, political bias, and emotional manipulation.
- **Fact Check Integration**: Cross-references claims with Google Fact Check Tools (optional).
- **Student-Friendly UI**: Modern, clean interface with history tracking and educational insights.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Core ML**: PyTorch, Hugging Face Transformers
- **NLP**: spaCy, Sentence-Transformers
- **Database**: MongoDB Atlas
- **Auth**: Bcrypt, Streamlit Session State
- **Visualization**: Plotly, Matplotlib (SHAP)

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd verisense
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Convert environment keys**
   Rename `.env.example` to `.env` and add your MongoDB connection string (and optional Google API key).
   ```env
   MONGODB_URI=mongodb+srv://...
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🏗️ Architecture

The system follows a modular architecture:
- `src/models`: Wrappers for DeBERTa, S-BERT, etc.
- `src/auth`: User authentication and session management.
- `src/integrations`: Connectors for MongoDB and Google API.
- `src/ui`: Reusable Streamlit components.

## 🧩 How It Works

1. **Input**: User pastes text or URL.
2. **Preprocessing**: Text is cleaned and claims are extracted using spaCy.
3. **Classification**: DeBERTa model predicts "Real" vs "Fake".
4. **Verification**: Extracted claims are compared against a trusted knowledge base using Semantic Search.
5. **Synthesis**: Scores are combined, and SHAP values explain the decision.
6. **Output**: User sees a dashboard with the final determination and verified facts.

## 📄 License
MIT License
