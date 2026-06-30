"""
======================================================
AI-Powered College Assistant Chatbot - Main Flask App
======================================================
Entry point for the Flask web server.
Run this file to start the chatbot server.

Author: Final Year B.E. IT Project
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import sys

# Add backend folder to path so we can import modules
sys.path.append(os.path.dirname(__file__))

from modules.document_loader import DocumentLoader
from modules.query_processor import QueryProcessor
from modules.llm_handler import LLMHandler
from modules.chat_history import ChatHistory

# ─────────────────────────────────────────────────────
# Initialize Flask App
# ─────────────────────────────────────────────────────
app = Flask(
    __name__,
    template_folder="../frontend/templates",  # HTML files location
    static_folder="../frontend/static"        # CSS/JS files location
)
CORS(app)  # Allow cross-origin requests (needed for frontend-backend communication)

# ─────────────────────────────────────────────────────
# Initialize Core Modules
# ─────────────────────────────────────────────────────
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "data", "uploads")
VECTORDB_FOLDER = os.path.join(os.path.dirname(__file__), "data", "vectordb")
HISTORY_DB = os.path.join(os.path.dirname(__file__), "data", "chat_history", "history.db")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(VECTORDB_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(HISTORY_DB), exist_ok=True)

# Create module instances
doc_loader   = DocumentLoader(UPLOAD_FOLDER, VECTORDB_FOLDER)
query_proc   = QueryProcessor(VECTORDB_FOLDER, doc_loader=doc_loader)
llm_handler  = LLMHandler()
chat_history = ChatHistory(HISTORY_DB)

# ─────────────────────────────────────────────────────
# PAGE ROUTES
# ─────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main chatbot page."""
    return render_template("index.html")

@app.route("/admin")
def admin():
    """Serve the admin document upload panel."""
    return render_template("admin.html")

# ─────────────────────────────────────────────────────
# API ROUTES - CHAT
# ─────────────────────────────────────────────────────

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Main chat endpoint.
    
    Receives a user question, retrieves relevant document chunks,
    sends them to LLM (Gemini or local), and returns the answer.
    
    Request JSON: { "question": "What are admission requirements?" }
    Response JSON: { "answer": "...", "sources": [...], "model_used": "..." }
    """
    data = request.get_json()
    
    # Validate input
    if not data or "question" not in data:
        return jsonify({"error": "No question provided"}), 400
    
    question = data["question"].strip()
    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400

    try:
        # Step 1: Convert question to embedding and retrieve top matching chunks
        context_chunks = query_proc.retrieve_context(question, top_k=4)
        
        # Step 2: If no relevant documents found
        if not context_chunks:
            answer = "I don't have enough information in my knowledge base to answer this. Please contact the college office directly."
            chat_history.save(question, answer, [], "no_context")
            return jsonify({
                "answer": answer,
                "sources": [],
                "model_used": "none"
            })

        # Step 3: Generate answer using LLM (Gemini first, fallback to local)
        answer, model_used = llm_handler.generate_answer(question, context_chunks)

        # Step 4: Extract source filenames for citation
        sources = list(set([chunk["source"] for chunk in context_chunks]))

        # Step 5: Save conversation to history
        chat_history.save(question, answer, sources, model_used)

        return jsonify({
            "answer": answer,
            "sources": sources,
            "model_used": model_used
        })

    except Exception as e:
        print(f"[ERROR in /api/chat]: {e}")
        return jsonify({"error": f"Something went wrong: {str(e)}"}), 500


@app.route("/api/history", methods=["GET"])
def get_history():
    """
    Fetch recent chat history.
    Returns last 20 conversations from SQLite database.
    """
    try:
        history = chat_history.get_recent(limit=20)
        return jsonify({"history": history})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────────────────
# API ROUTES - ADMIN (Document Management)
# ─────────────────────────────────────────────────────

@app.route("/api/upload", methods=["POST"])
def upload_document():
    """
    Admin endpoint to upload a PDF document.
    
    Accepts multipart/form-data with a file field named 'document'.
    Extracts text, chunks it, embeds it, and stores in FAISS.
    """
    if "document" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["document"]
    
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    try:
        result = doc_loader.load_and_index(file)
        return jsonify(result)
    except Exception as e:
        print(f"[ERROR in /api/upload]: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/documents", methods=["GET"])
def list_documents():
    """List all uploaded documents."""
    try:
        docs = doc_loader.list_documents()
        return jsonify({"documents": docs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/documents/<filename>", methods=["DELETE"])
def delete_document(filename):
    """
    Delete a specific document and rebuild the vector database.
    
    WARNING: Rebuilding takes time depending on document count.
    """
    try:
        result = doc_loader.delete_and_rebuild(filename)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/rebuild", methods=["POST"])
def rebuild_vectordb():
    """
    Force-rebuild the FAISS vector database from all uploaded PDFs.
    Use this if the index becomes corrupt or after manual file changes.
    """
    try:
        result = doc_loader.rebuild_index()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/status", methods=["GET"])
def status():
    """Health check endpoint. Returns system status."""
    return jsonify({
        "status": "running",
        "documents_count": len(doc_loader.list_documents()),
        "vector_db_ready": doc_loader.is_index_ready(),
        "gemini_configured": llm_handler.gemini_available
    })


# ─────────────────────────────────────────────────────
# Run the Server
# ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  AI College Chatbot Server Starting...")
    print("  Open browser: http://localhost:5000")
    print("  Admin Panel:  http://localhost:5000/admin")
    print("=" * 60)
    app.run(debug=True, host="0.0.0.0", port=5000)
