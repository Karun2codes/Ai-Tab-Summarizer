# AI Multi-Tab Summarizer 

A beginner-friendly Chrome extension project that extracts text from multiple open tabs and generates AI summaries using a custom-trained BART model.

## 🚀 Project Overview
This project demonstrates a full-stack AI application:
- **ML Pipeline**: Data loading (CNN/DailyMail), Preprocessing, Training (BART), and Evaluation (ROUGE).
- **Backend**: FastAPI server to serve the model for real-time inference.
- **Frontend**: Chrome Extension (Manifest V3) that interacts with the browser tabs.

## 📂 File Structure
- `data_loader.py`: Fetches the CNN/DailyMail dataset.
- `preprocess.py`: Cleans and tokenizes text.
- `model.py`: BART model wrapper class.
- `train.py`: Fine-tuning script using HuggingFace Trainer API.
- `evaluate.py`: ROUGE metric calculation.
- `inference.py`: Standalone class for generating summaries.
- `app.py`: FastAPI server script.
- `extension/`: Chrome extension source code.
- `requirements.txt`: List of dependencies.

## 🛠️ Setup Instructions

### 1. Backend Setup
1. Install Python 3.8+.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Train the model:
   ```bash
   python train.py
   ```
   *Note: If you don't train, the system will fallback to the base `facebook/bart-base` model.*
4. Start the FastAPI server:
   ```bash
   python app.py
   ```

### 2. Chrome Extension Setup
1. Open Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode** (toggle in the top right).
3. Click **Load unpacked**.
4. Select the `extension/` folder from this project directory.

## 📖 How to Use
1. Open several news articles or blog posts in different tabs.
2. Click the **AI Multi-Tab Summarizer** icon in your extension bar.
3. Click **Summarize All Tabs** to see individual summaries.
4. Click **Combined Summary** to see a single summary covering all tab content.

## 📊 Evaluation
Run `python evaluate.py` to see the ROUGE scores for the model on the test set.

## 🎓 Design Decisions
- **Model**: Used BART (Bidirectional and Auto-Regressive Transformers) because it is state-of-the-art for abstractive summarization.
- **FastAPI**: Chosen for its speed and automatic documentation.
- **Manifest V3**: Used the latest Chrome extension standards for security and longevity.

---
*Created for Final Year Evaluation.*
