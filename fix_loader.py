# Run this file once: python fix_loader.py
# It will automatically replace document_loader.py with the fixed version

import os

NEW_CODE = '''"""
Document Loader - Fixed version with better PDF table extraction
"""

import os
import json
import re
import numpy as np
import fitz
import faiss
from sentence_transformers import SentenceTransformer
from werkzeug.utils import secure_filename


class DocumentLoader:

    def __init__(self, upload_folder: str, vectordb_folder: str):
        self.upload_folder   = upload_folder
        self.vectordb_folder = vectordb_folder
        self.index_path      = os.path.join(vectordb_folder, "faiss.index")
        self.metadata_path   = os.path.join(vectordb_folder, "metadata.json")

        print("[DocumentLoader] Loading sentence embedding model...")
        self.embedder      = SentenceTransformer("all-MiniLM-L6-v2")
        self.embedding_dim = 384
        self.chunk_size    = 400
        self.chunk_overlap = 80
        self.index         = None
        self.metadata      = []
        self._load_existing_index()
        print("[DocumentLoader] Ready.")

    def load_and_index(self, file) -> dict:
        filename = secure_filename(file.filename)
        filepath = os.path.join(self.upload_folder, filename)
        file.save(filepath)
        print(f"[DocumentLoader] Saved: {filename}")
        text = self._extract_text_from_pdf(filepath)
        if not text.strip():
            os.remove(filepath)
            raise ValueError("Could not extract any text from this PDF.")
        print(f"[DocumentLoader] Extracted {len(text)} characters from {filename}")
        chunks     = self._split_into_chunks(text, filename)
        texts      = [c["text"] for c in chunks]
        embeddings = self._embed_texts(texts)
        self._add_to_index(embeddings, chunks)
        self._save_index()
        return {
            "status":      "success",
            "filename":    filename,
            "chunk_count": len(chunks),
            "message":     f"Successfully indexed {filename} ({len(chunks)} text chunks)"
        }

    def list_documents(self) -> list:
        if not os.path.exists(self.upload_folder):
            return []
        return [f for f in os.listdir(self.upload_folder) if f.endswith(".pdf")]

    def delete_and_rebuild(self, filename: str) -> dict:
        filepath = os.path.join(self.upload_folder, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filename}")
        os.remove(filepath)
        result = self.rebuild_index()
        result["message"] = f"Deleted {filename} and rebuilt index. {result[\'message\']}"
        return result

    def rebuild_index(self) -> dict:
        self.index    = None
        self.metadata = []
        pdfs = self.list_documents()
        if not pdfs:
            self._save_index()
            return {"status": "success", "message": "No documents found. Index cleared."}
        total_chunks = 0
        for pdf_name in pdfs:
            filepath   = os.path.join(self.upload_folder, pdf_name)
            text       = self._extract_text_from_pdf(filepath)
            if not text.strip():
                continue
            chunks     = self._split_into_chunks(text, pdf_name)
            texts      = [c["text"] for c in chunks]
            embeddings = self._embed_texts(texts)
            self._add_to_index(embeddings, chunks)
            total_chunks += len(chunks)
        self._save_index()
        return {"status": "success", "message": f"Rebuilt index from {len(pdfs)} documents ({total_chunks} total chunks)"}

    def is_index_ready(self) -> bool:
        return self.index is not None and self.index.ntotal > 0

    def _extract_text_from_pdf(self, filepath: str) -> str:
        doc = fitz.open(filepath)
        all_pages_text = []
        for page_num, page in enumerate(doc):
            page_label = f"[Page {page_num + 1}]"
            page_text  = self._extract_page_by_words(page)
            if not page_text.strip():
                page_text = page.get_text("text")
            if page_text.strip():
                all_pages_text.append(f"{page_label}\\n{page_text}")
        doc.close()
        return "\\n\\n".join(all_pages_text)

    def _extract_page_by_words(self, page) -> str:
        words = page.get_text("words")
        if not words:
            return ""
        words_sorted = sorted(words, key=lambda w: (round(w[1] / 10) * 10, w[0]))
        lines      = []
        current_y  = None
        line_words = []
        for w in words_sorted:
            y    = round(w[1] / 10) * 10
            word = w[4].strip()
            if not word:
                continue
            if current_y is None:
                current_y = y
            if y == current_y:
                line_words.append(word)
            else:
                if line_words:
                    lines.append(" ".join(line_words))
                line_words = [word]
                current_y  = y
        if line_words:
            lines.append(" ".join(line_words))
        return "\\n".join(lines)

    def _split_into_chunks(self, text: str, source: str) -> list:
        chunks = []
        page_sections = re.split(r\'\\[Page \\d+\\]\', text)
        page_sections = [s.strip() for s in page_sections if s.strip()]
        if len(page_sections) > 1:
            for i, section in enumerate(page_sections):
                if section.strip():
                    chunks.append({"text": section.strip(), "source": source, "chunk_id": i})
            full = text.strip()
            if len(full) < 10000:
                chunks.append({"text": full, "source": source, "chunk_id": len(chunks)})
        else:
            start = 0
            chunk_id = 0
            while start < len(text):
                end   = start + self.chunk_size
                chunk = text[start:end]
                if chunk.strip():
                    chunks.append({"text": chunk.strip(), "source": source, "chunk_id": chunk_id})
                    chunk_id += 1
                start += self.chunk_size - self.chunk_overlap
        return chunks

    def _embed_texts(self, texts: list) -> np.ndarray:
        return self.embedder.encode(texts, convert_to_numpy=True, show_progress_bar=False, batch_size=32).astype(np.float32)

    def _add_to_index(self, embeddings: np.ndarray, chunks: list):
        if self.index is None:
            self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.index.add(embeddings)
        self.metadata.extend(chunks)

    def _save_index(self):
        if self.index is not None:
            faiss.write_index(self.index, self.index_path)
        elif os.path.exists(self.index_path):
            os.remove(self.index_path)
        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
        print(f"[DocumentLoader] Saved: {self.index.ntotal if self.index else 0} vectors")

    def _load_existing_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            try:
                self.index = faiss.read_index(self.index_path)
                with open(self.metadata_path, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
                print(f"[DocumentLoader] Loaded index: {self.index.ntotal} vectors")
            except Exception as e:
                print(f"[DocumentLoader] Failed to load: {e}")
                self.index    = None
                self.metadata = []
        else:
            print("[DocumentLoader] No existing index.")
'''

# Find the file path
target = os.path.join("backend", "modules", "document_loader.py")

if os.path.exists(target):
    with open(target, "w", encoding="utf-8") as f:
        f.write(NEW_CODE)
    print(f"SUCCESS: Replaced {target}")
else:
    print(f"ERROR: Could not find {target}")
    print("Make sure you run this script from D:\\college_chatbot\\")
    print("Current directory:", os.getcwd())

# Also delete old index files so they get rebuilt fresh
for stale in [
    os.path.join("backend","data","vectordb","faiss.index"),
    os.path.join("backend","data","vectordb","metadata.json"),
]:
    if os.path.exists(stale):
        os.remove(stale)
        print(f"Deleted stale: {stale}")

print("\nDone! Now run:  python run.py")
print("Then go to Admin Panel and click 'Rebuild Vector Index'")
