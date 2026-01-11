import os
import sys
import subprocess

def run_cmd(cmd):
    print(f"Executing: {cmd}")
    subprocess.check_call(cmd, shell=True)

def main():
    print("Starting Smart AI PM Tool (MVC Version)...")
    
    # 1. Install dependencies
    print("Installing dependencies...")
    try:
        run_cmd(f"{sys.executable} -m pip install fastapi uvicorn sqlalchemy pydantic jinja2 python-multipart pypdf")
    except Exception as e:
        print(f"Error installing dependencies: {e}")

    # 2. Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # 3. Start the server
    print("\nApp starting at http://localhost:8000")
    print("Press Ctrl+C to stop\n")
    
    try:
        # Note the change to app.controllers.main:app
        subprocess.run([sys.executable, "-m", "uvicorn", "app.controllers.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main()
