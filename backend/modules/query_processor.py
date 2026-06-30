"""
======================================================
Module: Query Processor
======================================================
Handles question-to-context retrieval:
  1. Convert user question to embedding vector
  2. Search FAISS for most similar document chunks
  3. Return top-k chunks as context for LLM

This is the "R" (Retrieval) in RAG.
"""

import os
import json
import numpy as np
import faiss


class QueryProcessor:
    """
    Converts user questions into embeddings and retrieves
    the most relevant document chunks from FAISS.
    """

    def __init__(self, vectordb_folder: str, doc_loader=None):
        """
        Initialize the QueryProcessor.

        Args:
            vectordb_folder: Directory containing FAISS index and metadata
            doc_loader: The shared DocumentLoader instance. Its `.embedder`
                        property is reused here (lazily) so the embedding
                        model is loaded only once in memory, and only when
                        actually first needed -- not at startup. This keeps
                        Flask's port binding fast and avoids duplicating the
                        ~300-400MB model in RAM (important on hosts like
                        Render's free tier, which caps at 512MB).
        """
        self.vectordb_folder = vectordb_folder
        self.index_path      = os.path.join(vectordb_folder, "faiss.index")
        self.metadata_path   = os.path.join(vectordb_folder, "metadata.json")
        self._doc_loader     = doc_loader
        self._own_embedder   = None

        print("[QueryProcessor] Ready (embedding model will load on first use).")

    @property
    def embedder(self):
        """Reuse the shared DocumentLoader's embedder if available, else load our own."""
        if self._doc_loader is not None:
            return self._doc_loader.embedder
        if self._own_embedder is None:
            print("[QueryProcessor] No shared loader provided, loading own model...")
            from sentence_transformers import SentenceTransformer
            self._own_embedder = SentenceTransformer("all-MiniLM-L6-v2")
        return self._own_embedder

    # ──────────────────────────────────────────────────
    # PUBLIC METHODS
    # ──────────────────────────────────────────────────

    def retrieve_context(self, question: str, top_k: int = 4) -> list:
        """
        Main retrieval pipeline:
        Question -> Embedding -> FAISS Search -> Top-K Chunks

        Args:
            question: User's natural language question
            top_k: Number of most relevant chunks to retrieve

        Returns:
            List of dicts: [{text, source, score}, ...] sorted by relevance
            Returns empty list if index doesn't exist or question is irrelevant.
        """
        # Step 1: Load index (reload each time to pick up changes)
        index, metadata = self._load_index()
        if index is None or index.ntotal == 0:
            print("[QueryProcessor] No FAISS index found or index is empty.")
            return []

        # Step 2: Convert question to embedding vector
        question_embedding = self._embed_question(question)

        # Step 3: Clamp top_k to available vectors
        actual_top_k = min(top_k, index.ntotal)

        # Step 4: Search FAISS for nearest neighbors
        # distances: array of L2 distances (lower = more similar)
        # indices:   array of metadata indices
        distances, indices = index.search(question_embedding, actual_top_k)

        # Step 5: Build results list
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:  # FAISS returns -1 for invalid results
                continue

            chunk    = metadata[idx]
            # Convert L2 distance to a similarity score (0 to 1, higher = better)
            similarity = self._distance_to_similarity(dist)

            # Filter out chunks with very low similarity (not relevant)
            if similarity < 0.2:
                continue

            results.append({
                "text":   chunk["text"],
                "source": chunk["source"],
                "score":  round(similarity, 3)
            })

        print(f"[QueryProcessor] Retrieved {len(results)} relevant chunks for: '{question[:50]}...'")
        return results

    # ──────────────────────────────────────────────────
    # PRIVATE METHODS
    # ──────────────────────────────────────────────────

    def _embed_question(self, question: str) -> np.ndarray:
        """
        Convert question string to a 2D float32 numpy array for FAISS.

        Args:
            question: The user's question text

        Returns:
            numpy array of shape (1, embedding_dim) -- FAISS requires 2D input
        """
        embedding = self.embedder.encode(
            [question],                # Must be a list even for single input
            convert_to_numpy=True,
            show_progress_bar=False
        )
        return embedding.astype(np.float32)  # FAISS requires float32

    def _load_index(self):
        """
        Load FAISS index and metadata from disk.

        Returns:
            Tuple of (faiss.Index, list of metadata dicts)
            Returns (None, []) if index doesn't exist
        """
        if not os.path.exists(self.index_path) or not os.path.exists(self.metadata_path):
            return None, []

        try:
            index = faiss.read_index(self.index_path)
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            return index, metadata
        except Exception as e:
            print(f"[QueryProcessor] Error loading index: {e}")
            return None, []

    def _distance_to_similarity(self, l2_distance: float) -> float:
        """
        Convert FAISS L2 distance to a 0-1 similarity score.

        L2 distance of 0 = perfect match (similarity = 1.0)
        Higher distance = lower similarity

        Args:
            l2_distance: The L2 (Euclidean) distance from FAISS

        Returns:
            Similarity score between 0 and 1
        """
        # Formula: 1 / (1 + distance) gives values in (0, 1]
        return float(1 / (1 + l2_distance))