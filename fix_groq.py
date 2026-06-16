# fix_groq.py
# Run: python fix_groq.py
import os

CODE = '''"""
LLM Handler - Groq API (Fast, Free, No quota issues)
"""

import os
import requests
from typing import Tuple


class LLMHandler:

    def __init__(self):
        self.groq_api_key   = os.environ.get("GROQ_API_KEY", "")
        self.groq_available = bool(self.groq_api_key)
        self.groq_model     = "llama3-8b-8192"
        self.groq_url       = "https://api.groq.com/openai/v1/chat/completions"

        if self.groq_available:
            print(f"[LLMHandler] Groq API ready. Model: {self.groq_model}")
        else:
            print("[LLMHandler] WARNING: GROQ_API_KEY not set.")

        self.gemini_api_key  = os.environ.get("GEMINI_API_KEY", "")
        self.gemini_available = bool(self.gemini_api_key)
        self.local_model_loaded = False

    def generate_answer(self, question: str, context_chunks: list) -> Tuple[str, str]:
        context = self._build_context(context_chunks)
        prompt  = self._build_prompt(question, context)

        # Try Groq first
        if self.groq_available:
            try:
                answer = self._call_groq(prompt)
                if answer:
                    print("[LLMHandler] Answer from Groq")
                    return answer, "groq-llama3"
            except Exception as e:
                print(f"[LLMHandler] Groq failed: {e}")

        # Fallback: extract from context
        answer = self._extract_from_context(question, context_chunks)
        return answer, "context-extraction"

    def _call_groq(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type":  "application/json"
        }
        payload = {
            "model": self.groq_model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful college assistant. Answer questions in 1-2 short sentences only. Be specific and direct. Only use the provided context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2,
            "max_tokens":  150
        }

        response = requests.post(
            self.groq_url,
            headers=headers,
            json=payload,
            timeout=15
        )

        if response.status_code != 200:
            raise Exception(f"Groq API error {response.status_code}: {response.text}")

        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    def _build_context(self, chunks: list) -> str:
        return "\\n\\n".join([f"[{c[\'source\']}]\\n{c[\'text\']}" for c in chunks])

    def _build_prompt(self, question: str, context: str) -> str:
        return f"""Answer this college question in 1-2 sentences using ONLY the context below.
If not in context, say "I don\\'t have that information."

CONTEXT:
{context}

QUESTION: {question}

SHORT ANSWER:"""

    def _extract_from_context(self, question: str, chunks: list) -> str:
        if not chunks:
            return "I don\\'t have enough information to answer this question."
        return f"Based on the college documents:\\n\\n{chunks[0][\'text\']}"
'''

with open(os.path.join("backend", "modules", "llm_handler.py"), "w", encoding="utf-8") as f:
    f.write(CODE)
print("SUCCESS: llm_handler.py updated with Groq")
print("Now run: python run.py")
