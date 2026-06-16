# 🎓 AI-Powered College Assistant Chatbot (RAG)
### Final Year B.E. IT Project — Complete Setup & Usage Guide

---

## 📋 TABLE OF CONTENTS
1. [Project Overview](#overview)
2. [System Architecture](#architecture)
3. [Folder Structure](#folder-structure)
4. [Setup Instructions](#setup)
5. [How to Configure Gemini API](#gemini-setup)
6. [How to Run](#how-to-run)
7. [How to Use Admin Panel](#admin-panel)
8. [How to Test the Chatbot](#testing)
9. [How the Local Model Works](#local-model)
10. [Troubleshooting](#troubleshooting)
11. [Project Explanation (for Viva)](#viva)

---

## 1. PROJECT OVERVIEW <a name="overview"></a>

This chatbot answers student queries about a specific college using **Retrieval-Augmented Generation (RAG)**. It:

- Answers questions **only from uploaded college PDFs** (no hallucination)
- Shows **source document citations** for every answer
- Uses **Gemini API** (cloud) with **automatic fallback** to a local LLM if internet fails
- Has an **Admin Panel** to upload/delete documents
- Stores **chat history** in SQLite
- Works on an **8GB RAM laptop** without a GPU

---

## 2. SYSTEM ARCHITECTURE <a name="architecture"></a>

```
User Types Question
        │
        ▼
   Flask Web Server (app.py)
        │
        ▼
QueryProcessor.retrieve_context()
   → Embed question using SentenceTransformer
   → Search FAISS vector database
   → Return top 4 most relevant text chunks
        │
        ▼
LLMHandler.generate_answer()
   → Try Gemini API (cloud)
   → If fails → Try Local LLM (TinyLlama)
   → If fails → Extract directly from context
        │
        ▼
Return Answer + Source Citations
        │
        ▼
Display in Chat UI with model badge
```

**When Admin uploads a PDF:**
```
PDF File
  → PyMuPDF extracts text
  → Split into 500-char overlapping chunks
  → SentenceTransformer generates embeddings
  → Store in FAISS index file
  → Save metadata (text + filename) as JSON
```

---

## 3. FOLDER STRUCTURE <a name="folder-structure"></a>

```
college_chatbot/
│
├── run.py                        ← START HERE — Main startup script
├── requirements.txt              ← Python dependencies
├── .env.example                  ← Copy this to .env and add API key
├── create_sample_pdf.py          ← Generates test PDF for demo
│
├── backend/
│   ├── app.py                    ← Flask routes and API endpoints
│   ├── data/
│   │   ├── uploads/              ← Uploaded PDFs stored here
│   │   ├── vectordb/             ← FAISS index files stored here
│   │   │   ├── faiss.index       ← Binary FAISS vector index
│   │   │   └── metadata.json     ← Text chunks and source filenames
│   │   └── chat_history/
│   │       └── history.db        ← SQLite chat history database
│   └── modules/
│       ├── __init__.py
│       ├── document_loader.py    ← PDF → chunks → FAISS
│       ├── query_processor.py    ← Question → embedding → search
│       ├── llm_handler.py        ← Gemini API + local LLM fallback
│       └── chat_history.py       ← SQLite read/write
│
└── frontend/
    ├── templates/
    │   ├── index.html            ← Main chatbot page
    │   └── admin.html            ← Admin document management panel
    └── static/
        ├── css/
        │   └── style.css         ← All styles for both pages
        └── js/
            ├── chat.js           ← Chat page logic
            └── admin.js          ← Admin panel logic
```

---

## 4. SETUP INSTRUCTIONS <a name="setup"></a>

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- 8GB RAM minimum
- Internet connection (for first-time model download and Gemini API)

### Step 1 — Download/Clone the Project
Place the `college_chatbot` folder anywhere on your computer.
```
cd college_chatbot
```

### Step 2 — Create Virtual Environment (Recommended)
A virtual environment keeps this project's packages separate from your system Python.
```bash
# Create virtual environment
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# You should see (venv) in your terminal prompt now
```

### Step 3 — Install PyTorch (CPU version — saves 2GB space)
Install PyTorch BEFORE requirements.txt to get the CPU-only version:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```
This installs PyTorch without CUDA (GPU support). For an 8GB laptop, this is correct.

### Step 4 — Install All Dependencies
```bash
pip install -r requirements.txt
```
This installs: Flask, PyMuPDF, FAISS, sentence-transformers, transformers, requests, numpy.

Wait for it to complete. This may take 5–10 minutes depending on your internet speed.

### Step 5 — Set Up Configuration
```bash
# Copy the example config
# On Windows:
copy .env.example .env
# On Mac/Linux:
cp .env.example .env
```
Then open `.env` in any text editor and add your Gemini API key (see next section).

---

## 5. HOW TO CONFIGURE GEMINI API <a name="gemini-setup"></a>

### Getting a Free Gemini API Key
1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (it looks like: `AIzaSy...`)

### Adding the Key to .env
Open `.env` in a text editor (Notepad, VS Code, etc.):
```
GEMINI_API_KEY=AIzaSyYour_actual_key_here
```
Replace `your_gemini_api_key_here` with your actual key.
Do NOT add quotes around the key.

### Testing the Key
The chatbot will automatically try Gemini when you send a message.
You'll see `✨ Gemini AI` badge on the answer if it worked.

---

## 6. HOW TO RUN <a name="how-to-run"></a>

### Start the Server
Make sure your virtual environment is activated, then:
```bash
python run.py
```

You should see:
```
✅ Gemini API Key: AIzaSy...xxxx
✅ Python 3.x
✅ flask
✅ fitz
✅ faiss
✅ sentence_transformers
✅ numpy

🚀 Server running at: http://localhost:5000
⚙️  Admin panel at:   http://localhost:5000/admin
```

### Open the App
- **Chatbot:** Open your browser → go to `http://localhost:5000`
- **Admin Panel:** Go to `http://localhost:5000/admin`

### Stop the Server
Press `Ctrl + C` in the terminal.

---

## 7. HOW TO USE ADMIN PANEL <a name="admin-panel"></a>

### Step 1 — Upload a PDF
1. Go to `http://localhost:5000/admin`
2. Click the upload area (or drag a PDF file onto it)
3. Wait for the success message: "Successfully indexed X text chunks"

The system will:
- Extract all text from the PDF
- Split it into 500-character chunks with 100-character overlap
- Generate embedding vectors using SentenceTransformer
- Store everything in FAISS vector database

### Step 2 — Upload Your College Documents
Upload all relevant PDFs:
- Admission brochure
- Fee structure document
- Hostel rules and information
- Course syllabus
- Anti-ragging policy
- Placement information
- etc.

### Step 3 — Create a Test PDF (Optional)
If you don't have college PDFs ready yet, generate a sample:
```bash
pip install reportlab
python create_sample_pdf.py
```
Then upload `sample_college_faq.pdf` through the admin panel.

### Managing Documents
- **View documents:** Listed under "Indexed Documents"
- **Delete a document:** Click the 🗑️ Delete button (automatically rebuilds index)
- **Rebuild index:** Click "Rebuild Vector Index" if index gets corrupted

---

## 8. HOW TO TEST THE CHATBOT <a name="testing"></a>

### Quick Test (After Uploading Sample PDF)
Open `http://localhost:5000` and ask these questions:

1. "What are the admission requirements?"
2. "What is the fee structure?"
3. "Are there any scholarships available?"
4. "What documents do I need for admission?"
5. "Tell me about hostel facilities"
6. "What are the important dates for 2024?"

### Expected Behavior
- ✅ Each answer should be based on content from the uploaded PDF
- ✅ Each answer should show the source file name
- ✅ You should see ✨ Gemini AI or 🖥️ Local LLM badge
- ✅ Chat history should save each conversation

### Testing Fallback Mode
To test offline/local mode:
1. Set `GEMINI_API_KEY=invalid_key_here` in `.env`
2. Restart the server
3. Ask a question — it should fall back to local LLM
4. You'll see 🖥️ Local LLM badge on the answer

### Testing Out-of-Scope Questions
Ask something not in any document:
"What is the weather today?"
Expected: "I don't have specific information about this in the college documents..."

---

## 9. HOW THE LOCAL MODEL WORKS <a name="local-model"></a>

### Default Model: TinyLlama-1.1B-Chat
- Size: ~600MB on disk (downloaded from HuggingFace Hub)
- RAM usage: ~2GB during inference
- Speed: ~10-30 seconds per answer on CPU (8GB RAM laptop)
- Quality: Good for factual Q&A from context

### First Run with Local Model
The model downloads automatically on first use.
It's saved to `~/.cache/huggingface/hub/` (your user home folder).
This only happens once — subsequent runs are fast.

### Using a Better Local Model (Optional)
Edit `.env` to change the model:
```
LOCAL_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
```
⚠️ Mistral-7B needs ~8GB RAM and ~14GB disk space.

---

## 10. TROUBLESHOOTING <a name="troubleshooting"></a>

### "ModuleNotFoundError: No module named 'fitz'"
```bash
pip install PyMuPDF
```

### "ModuleNotFoundError: No module named 'faiss'"
```bash
pip install faiss-cpu
```

### "Gemini API returned status 400"
Your API key is invalid. Go to https://makersuite.google.com/app/apikey and get a new key.

### "Gemini API returned status 429"
You've hit the rate limit. Wait 1 minute and try again. The free tier allows 60 requests/minute.

### Local model takes too long to respond (>2 minutes)
This is normal on CPU. Options:
1. Use Gemini API (much faster)
2. Use the context-extraction fallback (instant)

### "FAISS index is empty" error
Upload at least one PDF through the Admin Panel first.

### PDF shows 0 chunks
The PDF might be image-only (scanned). Try a different PDF with actual text.
OCR support can be added using pytesseract (not included by default).

### Port 5000 already in use
Change the port in `.env`:
```
FLASK_PORT=5001
```
Then access the app at `http://localhost:5001`

---

## 11. PROJECT EXPLANATION (FOR VIVA) <a name="viva"></a>

### What is RAG?
**Retrieval-Augmented Generation** is an AI architecture that combines:
1. **Retrieval:** Finding relevant text from a knowledge base (documents)
2. **Augmentation:** Adding that text as context to the LLM prompt
3. **Generation:** The LLM generates an answer using only that context

This prevents hallucination and grounds the AI in real documents.

### What is FAISS?
FAISS (Facebook AI Similarity Search) is a library for efficient nearest-neighbor search in high-dimensional vector spaces. We use it to find the most semantically similar text chunks to a user's question.

### What are Embeddings?
Embeddings are numerical representations (vectors) of text. Similar text has similar vectors. We use SentenceTransformers to convert both documents and questions into these vectors, then find which document vectors are closest to the question vector.

### Why Hybrid Model Architecture?
- Gemini (cloud): Fast, high quality, but requires internet + API quota
- Local LLM: Slow, decent quality, but works offline, no cost, no quota
- Hybrid: Best of both worlds — use cloud when available, fallback to local when not

### Module Responsibilities
| Module | Responsibility |
|--------|---------------|
| document_loader.py | PDF → text → chunks → embeddings → FAISS |
| query_processor.py | Question → embedding → FAISS search → relevant chunks |
| llm_handler.py | Gemini API call → fallback to local LLM → answer |
| chat_history.py | SQLite read/write for conversation persistence |
| app.py | Flask routes connecting all modules |

---

## 📝 PROJECT DETAILS

| Item | Details |
|------|---------|
| Project Title | AI-Powered College Assistant Chatbot using RAG |
| Tech Stack | Python, Flask, FAISS, SentenceTransformers, Gemini API |
| Architecture | RAG (Retrieval-Augmented Generation) |
| Database | SQLite (chat history) + FAISS (vector DB) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Primary LLM | Google Gemini 1.5 Flash |
| Fallback LLM | TinyLlama-1.1B-Chat (local, offline) |
| Embedding Model | all-MiniLM-L6-v2 (384 dimensions) |

---

*Built for Final Year B.E. IT Project Submission*
