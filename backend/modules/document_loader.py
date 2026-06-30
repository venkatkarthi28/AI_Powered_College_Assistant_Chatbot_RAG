"""
Document Loader - PyMuPDF text extraction (no OCR)
"""

import os
import json
import re
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from werkzeug.utils import secure_filename


class DocumentLoader:

    def __init__(self, upload_folder: str, vectordb_folder: str):
        self.upload_folder   = upload_folder
        self.vectordb_folder = vectordb_folder
        self.index_path      = os.path.join(vectordb_folder, "faiss.index")
        self.metadata_path   = os.path.join(vectordb_folder, "metadata.json")

        # Lazy-load the embedding model: don't load it here, so that Flask
        # can bind to its port immediately on startup (important for hosts
        # like Render, which kill the deploy if no port is detected within
        # a few minutes). The model loads on first actual use instead.
        self._embedder      = None
        self.embedding_dim = 384
        self.chunk_size    = 400
        self.chunk_overlap = 80
        self.index         = None
        self.metadata      = []
        self._load_existing_index()
        print("[DocumentLoader] Ready (embedding model will load on first use).")

    @property
    def embedder(self):
        """Lazily load the sentence embedding model on first access."""
        if self._embedder is None:
            print("[DocumentLoader] Loading sentence embedding model (first use)...")
            self._embedder = SentenceTransformer("all-MiniLM-L6-v2")
            print("[DocumentLoader] Embedding model loaded.")
        return self._embedder

    def load_and_index(self, file) -> dict:
        filename = secure_filename(file.filename)
        filepath = os.path.join(self.upload_folder, filename)
        file.save(filepath)
        print(f"[DocumentLoader] Saved: {filename}")

        text = self._extract_text_from_pdf(filepath)
        if not text.strip():
            os.remove(filepath)
            raise ValueError("Could not extract any text from this PDF. Scanned/image-only PDFs are not supported.")

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
        result["message"] = f"Deleted {filename} and rebuilt index. {result['message']}"
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
        """
        Extract text from PDF using direct text extraction only.
        Scanned/image-only PDFs (no embedded text layer) are not supported.
        """
        import fitz
        doc  = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text("text")
        doc.close()

        if len(text.strip()) > 50:
            print(f"[DocumentLoader] Direct text extraction succeeded.")
        else:
            print(f"[DocumentLoader] WARNING: Little or no text found. This PDF may be a scanned image, which is not supported.")

        return text

    def _split_into_chunks(self, text: str, source: str) -> list:
        chunks = []
        page_sections = re.split(r'\[Page \d+\]', text)
        page_sections = [s.strip() for s in page_sections if s.strip()]

        if len(page_sections) > 1:
            for i, section in enumerate(page_sections):
                if section.strip():
                    chunks.append({"text": section.strip(), "source": source, "chunk_id": i})
            full = text.strip()
            if len(full) < 10000:
                chunks.append({"text": full, "source": source, "chunk_id": len(chunks)})
        else:
            start = 0; chunk_id = 0
            while start < len(text):
                end   = start + self.chunk_size
                chunk = text[start:end]
                if chunk.strip():
                    chunks.append({"text": chunk.strip(), "source": source, "chunk_id":chunk_id})
                    chunk_id += 1
                start += self.chunk_size - self.chunk_overlap

        return chunks

    def _embed_texts(self, texts: list) -> np.ndarray:
        return self.embedder.encode(
            texts, convert_to_numpy=True,
            show_progress_bar=False, batch_size=32
        ).astype(np.float32)

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
                self.index = None; self.metadata = []
        else:
            print("[DocumentLoader] No existing index.")