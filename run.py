"""
======================================================
run.py — Application Startup Script
======================================================
This is the MAIN FILE you run to start the chatbot.

Usage:
    python run.py

What it does:
  1. Loads environment variables from .env file
  2. Starts the Flask server

Never run backend/app.py directly — use this file.
"""

import os
import sys

# ─────────────────────────────────────────────────────
# Load Environment Variables from .env
# ─────────────────────────────────────────────────────
def load_env_file():
    """
    Manually load key=value pairs from .env file.
    We do this without python-dotenv to minimize dependencies.
    On Render, environment variables are already injected by the platform,
    so this is mainly useful for local development.
    """
    env_path = os.path.join(os.path.dirname(__file__), ".env")

    if not os.path.exists(env_path):
        print("[run.py] No .env file found (this is normal on Render — "
              "env vars are set in the dashboard).")
        return

    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                key   = key.strip()
                value = value.strip()
                if key not in os.environ:
                    os.environ[key] = value

    print("[run.py] Environment loaded from .env")


# ─────────────────────────────────────────────────────
# Main Entry Point
# ─────────────────────────────────────────────────────
if __name__ == "__main__":
    load_env_file()

    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'

    print(f"[run.py] Starting Flask server on {host}:{port} ...")
    print("[run.py] Loading the app (this includes loading the embedding "
          "model and may take a minute on first start) ...")

    from backend.app import app
    app.run(host=host, port=port, debug=False)