"""
Focus Friend - Unified Application Launcher.
Launches the scalable FastAPI REST API with modular Neo-Brutalist Web UI or Streamlit client.

Usage:
    python run.py                   # Default: Runs FastAPI server + Web UI (http://127.0.0.1:8501)
    python run.py --reload          # Runs with auto-reload for development
    python run.py --port 8000       # Runs on custom port
    python run.py --streamlit       # Runs Streamlit dashboard client
"""

import sys
import argparse
import subprocess
import uvicorn
from backend.config import settings

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def parse_args():
    """Parses command-line arguments for application execution."""
    parser = argparse.ArgumentParser(description="Focus Friend - Local-First Executive Assistant")
    parser.add_argument(
        "--host",
        default=settings.host,
        help=f"Host address to bind (default: {settings.host})"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=settings.port,
        help=f"Port number to bind (default: {settings.port})"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for local development"
    )
    parser.add_argument(
        "--streamlit",
        action="store_true",
        help="Launch the Streamlit dashboard client"
    )
    return parser.parse_args()


def main():
    """Main launcher entrypoint."""
    args = parse_args()

    if args.streamlit:
        print("[Focus Friend] Launching Streamlit dashboard client...")
        try:
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", "clients/streamlit/app.py",
                "--server.port", str(args.port),
                "--server.address", args.host
            ])
        except KeyboardInterrupt:
            print("\n[Focus Friend] Streamlit client stopped.")
    else:
        print("==================================================")
        print("⚡ FOCUS FRIEND: LOCAL-FIRST EXECUTIVE ASSISTANT")
        print("🎨 Aesthetic Neo-Brutalism UI & Scalable API v1")
        print(f"🚀 Web App: http://{args.host}:{args.port}")
        print(f"📚 OpenAPI Interactive Docs: http://{args.host}:{args.port}/docs")
        print("🔒 100% Private · Zero Cloud Telemetry")
        print("==================================================")

        try:
            uvicorn.run(
                "backend.main:app",
                host=args.host,
                port=args.port,
                reload=args.reload,
                log_level=settings.log_level.lower(),
            )
        except KeyboardInterrupt:
            print("\n[Focus Friend] Server stopped gracefully.")


if __name__ == "__main__":
    main()
