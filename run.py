"""
======================================================
run.py — Application Startup Script
======================================================
This is the MAIN FILE you run to start the chatbot.

Usage:
    python run.py

What it does:
  1. Loads environment variables from .env file
  2. Validates configuration (warns if API key missing)
  3. Starts the Flask development server

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
    """
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    
    if not os.path.exists(env_path):
        print("[run.py] WARNING: .env file not found!")
        print("[run.py] Copy .env.example to .env and set your GEMINI_API_KEY")
        return

    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            # Parse KEY=VALUE
            if "=" in line:
                key, value = line.split("=", 1)
                key   = key.strip()
                value = value.strip()
                # Only set if not already in environment
                if key not in os.environ:
                    os.environ[key] = value

    print("[run.py] Environment loaded from .env")


# ─────────────────────────────────────────────────────
# Validate Setup
# ─────────────────────────────────────────────────────
def validate_setup():
    """Check that everything is configured correctly."""
    print("\n" + "=" * 60)
    print("  AI College Chatbot — Startup Check")
    print("=" * 60)

    # Check Gemini API key
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("⚠️  GEMINI_API_KEY not set — will use local model only")
        print("   Get a free key: https://makersuite.google.com/app/apikey")
    else:
        masked = api_key[:8] + "..." + api_key[-4:]
        print(f"✅  Gemini API Key: {masked}")

    # Check Python version
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌  Python {version.major}.{version.minor} detected — Python 3.8+ required!")
        sys.exit(1)
    else:
        print(f"✅  Python {version.major}.{version.minor}")

    # Check key packages
    packages_ok = True
    required = ["flask", "fitz", "faiss", "sentence_transformers", "numpy"]
    for pkg in required:
        try:
            __import__(pkg)
            print(f"✅  {pkg}")
        except ImportError:
            print(f"❌  {pkg} — not installed (run: pip install -r requirements.txt)")
            packages_ok = False

    if not packages_ok:
        print("\n❌ Some packages are missing. Run:")
        print("   pip install -r requirements.txt")
        sys.exit(1)

    print("=" * 60)
    print("  All checks passed! Starting server...")
    print("=" * 60 + "\n")


# ─────────────────────────────────────────────────────
# Main Entry Point
# ─────────────────────────────────────────────────────
if __name__ == "__main__":
    # Step 1: Load .env file
    load_env_file()

    # Step 2: Validate setup
    validate_setup()

    # Step 3: Start Flask app
    # We import here (after env is loaded) so modules pick up env vars
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
    from app import app

    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"

    print(f"🚀 Server running at: http://localhost:{port}")
    print(f"⚙️  Admin panel at:   http://localhost:{port}/admin")
    print("   Press Ctrl+C to stop\n")

    app.run(host=host, port=port, debug=debug)
