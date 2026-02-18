# ⚙️ Setup Guide for VeriSense

Follow these steps to get your Fake News Detector running locally.

## Prerequisites
- Python 3.10 or higher
- A MongoDB Atlas account (free tier is fine)

## Step 1: Environment Setup

1. **Create a Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

2. **Install Libraries**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLP Models**
   The app will attempt to download models on the first run, but you need the spaCy core model installed manually:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Step 2: Database Configuration (MongoDB)

1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas/database).
2. Create a generic free cluster.
3. In "Security" > "Network Access", allow IP `0.0.0.0/0` (for testing) or your current IP.
4. In "Database Access", create a user (e.g., `admin`) and password.
5. Go to "Database" > "Connect" > "Drivers" and copy the connection string.
   - It looks like: `mongodb+srv://admin:<password>@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority`
6. Open `.env` file in the project root (create it if missing) and paste:
   ```env
   MONGODB_URI=your_connection_string_here
   ```

## Step 3: Google Fact Check API (Optional)

To enable external fact-checking against Google's database:
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable "Fact Check Tools API".
3. Generate an API Key.
4. Add it to your `.env`:
   ```env
   GOOGLE_FACTCHECK_API_KEY=your_api_key
   ```

## Step 4: Running the App

```bash
streamlit run app.py
```

**Note on First Run:**
The application will download the `DeBERTa-v3`, `Sentence-BERT`, and `DistilBART` models. This allows for high accuracy but requires about **2-3 GB of disk space** and a stable internet connection.

## Troubleshooting

- **Memory Errors**: If the app crashes on limited hardware, edit `config.py` and switch to lighter models (e.g., `distilbert` instead of `deberta`).
- **Connection Errors**: Ensure your IP is whitelisted in MongoDB Atlas.
