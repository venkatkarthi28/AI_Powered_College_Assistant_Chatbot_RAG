"""
======================================================
Module: Chat History
======================================================
Stores and retrieves conversation history using SQLite.

SQLite is used because:
  - No external database server needed
  - File-based (just one .db file)
  - Built into Python standard library
  - Perfect for small to medium applications

Table: chat_history
  - id:         Auto-increment primary key
  - question:   User's question
  - answer:     Bot's answer
  - sources:    JSON array of source filenames
  - model_used: Which LLM generated the answer
  - timestamp:  When the conversation happened
"""

import sqlite3
import json
from datetime import datetime


class ChatHistory:
    """
    Manages chat history persistence using SQLite.
    
    Usage:
        history = ChatHistory("path/to/history.db")
        history.save("What is the fee?", "The fee is ₹50,000/year", ["fees.pdf"], "gemini")
        recent = history.get_recent(limit=10)
    """

    def __init__(self, db_path: str):
        """
        Initialize ChatHistory with a SQLite database.

        Args:
            db_path: Full path to the SQLite database file
                     (file is created if it doesn't exist)
        """
        self.db_path = db_path
        self._initialize_database()
        print(f"[ChatHistory] SQLite database ready: {db_path}")

    # ─────────────────────────────────────────────────
    # PUBLIC METHODS
    # ─────────────────────────────────────────────────

    def save(self, question: str, answer: str, sources: list, model_used: str) -> int:
        """
        Save a conversation to the database.

        Args:
            question:   User's question text
            answer:     Bot's generated answer
            sources:    List of source filenames (e.g., ["admission.pdf"])
            model_used: Model that generated the answer ("gemini-1.5-flash", "local-llm", etc.)

        Returns:
            ID of the newly inserted row
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO chat_history (question, answer, sources, model_used, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    question,
                    answer,
                    json.dumps(sources),               # Store list as JSON string
                    model_used,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Human-readable timestamp
                )
            )
            conn.commit()
            row_id = cursor.lastrowid
            print(f"[ChatHistory] Saved conversation ID: {row_id}")
            return row_id
        finally:
            conn.close()

    def get_recent(self, limit: int = 20) -> list:
        """
        Retrieve the most recent conversations.

        Args:
            limit: Maximum number of records to return

        Returns:
            List of dicts with keys: id, question, answer, sources, model_used, timestamp
            Ordered newest first
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, question, answer, sources, model_used, timestamp
                FROM chat_history
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (limit,)
            )
            rows = cursor.fetchall()

            # Convert rows to list of dicts for JSON serialization
            result = []
            for row in rows:
                result.append({
                    "id":         row[0],
                    "question":   row[1],
                    "answer":     row[2],
                    "sources":    json.loads(row[3]) if row[3] else [],  # Parse JSON back to list
                    "model_used": row[4],
                    "timestamp":  row[5]
                })
            return result
        finally:
            conn.close()

    def get_all(self) -> list:
        """Retrieve all conversations (for export or analysis)."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, question, answer, sources, model_used, timestamp FROM chat_history ORDER BY timestamp")
            rows = cursor.fetchall()
            return [
                {
                    "id":         r[0],
                    "question":   r[1],
                    "answer":     r[2],
                    "sources":    json.loads(r[3]) if r[3] else [],
                    "model_used": r[4],
                    "timestamp":  r[5]
                }
                for r in rows
            ]
        finally:
            conn.close()

    def count(self) -> int:
        """Return total number of conversations stored."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM chat_history")
            return cursor.fetchone()[0]
        finally:
            conn.close()

    def clear(self) -> int:
        """
        Delete all chat history.
        
        Returns:
            Number of records deleted
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM chat_history")
            count = cursor.fetchone()[0]
            cursor.execute("DELETE FROM chat_history")
            conn.commit()
            return count
        finally:
            conn.close()

    # ─────────────────────────────────────────────────
    # PRIVATE METHODS
    # ─────────────────────────────────────────────────

    def _initialize_database(self):
        """
        Create the database and chat_history table if they don't exist.
        
        This is safe to call multiple times — it won't overwrite existing data.
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_history (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    question    TEXT NOT NULL,
                    answer      TEXT NOT NULL,
                    sources     TEXT,          -- JSON array stored as text
                    model_used  TEXT,
                    timestamp   TEXT NOT NULL  -- "YYYY-MM-DD HH:MM:SS"
                )
                """
            )
            conn.commit()
        finally:
            conn.close()

    def _get_connection(self) -> sqlite3.Connection:
        """
        Create and return a SQLite database connection.
        
        We create a new connection per operation (not pooled) because:
        - Flask is multi-threaded
        - SQLite connections are not thread-safe when shared
        
        Returns:
            sqlite3.Connection object
        """
        return sqlite3.connect(self.db_path)
