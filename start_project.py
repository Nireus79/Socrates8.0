#!/usr/bin/env python3
"""
Socrates 8.0 - One-Click Project Starter (Python Version)
This script starts both backend and frontend with all required setup
Simply run this file and follow the prompts
"""

import os
import sys
import subprocess
import shutil
import time
from pathlib import Path


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_step(step_num, title):
    """Print a step header"""
    print(f"\n[{step_num}/5] {title}")
    print("-" * 80)


def print_success(message):
    """Print success message"""
    print(f"✓ {message}")


def print_error(message):
    """Print error message"""
    print(f"✗ ERROR: {message}")
    sys.exit(1)


def check_command(cmd, name):
    """Check if a command is available"""
    if shutil.which(cmd):
        print_success(f"{name} found")
        return True
    else:
        print(f"⚠ WARNING: {name} not found")
        return False


def check_prerequisites():
    """Check all prerequisites"""
    print_step(1, "Checking Prerequisites")

    has_python = check_command("python", "Python")
    has_node = check_command("node", "Node.js")
    has_npm = check_command("npm", "npm")
    has_psql = check_command("psql", "PostgreSQL")

    if not (has_python and has_node and has_npm):
        print_error("Missing required tools. Please install Python, Node.js, and npm.")

    if not has_psql:
        response = input("\nContinue without PostgreSQL? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)


def setup_backend():
    """Setup backend"""
    print_step(2, "Setting up Backend")

    backend_dir = Path("Socrates-8.0/backend")
    venv_dir = backend_dir / "venv"

    # Create venv if it doesn't exist
    if not venv_dir.exists():
        print("Creating Python virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        print_success("Virtual environment created")
    else:
        print_success("Virtual environment already exists")

    # Get the python executable in venv
    if sys.platform == "win32":
        python_exe = venv_dir / "Scripts" / "python.exe"
    else:
        python_exe = venv_dir / "bin" / "python"

    # Install dependencies
    print("Installing backend dependencies...")
    subprocess.run([str(python_exe), "-m", "pip", "install", "-q", "-r", str(backend_dir / "requirements.txt")], check=True)
    print_success("Backend dependencies installed")

    # Create .env if it doesn't exist
    env_file = backend_dir / ".env"
    if not env_file.exists():
        print("Creating .env file from template...")
        env_example = backend_dir / ".env.example"
        if env_example.exists():
            shutil.copy(env_example, env_file)
        print("\n⚠ IMPORTANT: Edit the .env file and add your Claude API key!")
        print(f"File: {env_file}")
        print("\nRequired variables:")
        print("  CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxx")
        print("  DATABASE_URL=postgresql://socrates:socrates123@localhost:5432/socrates_db")
        input("\nPress Enter to continue...")
    else:
        print_success(".env file already exists")


def setup_frontend():
    """Setup frontend"""
    print_step(3, "Setting up Frontend")

    frontend_dir = Path("Socrates-8.0/frontend")

    # Create .env if it doesn't exist
    env_file = frontend_dir / ".env"
    if not env_file.exists():
        print("Creating .env file from template...")
        env_example = frontend_dir / ".env.example"
        if env_example.exists():
            shutil.copy(env_example, env_file)
        print_success("Frontend .env created")
    else:
        print_success("Frontend .env already exists")

    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print("Installing frontend dependencies (this may take a minute)...")
        subprocess.run(["npm", "install", "--silent"], cwd=str(frontend_dir), check=True)
        print_success("Frontend dependencies installed")
    else:
        print_success("node_modules already exists")


def show_summary():
    """Show summary and ask for start method"""
    print_step(4, "Summary and Next Steps")
    print("=" * 80)
    print("Setup Complete! The project is ready to run.")
    print("=" * 80)
    print("\nYou now have TWO options:\n")
    print("OPTION 1: Automatic Start (Recommended)")
    print("  - Press Enter to start both backend and frontend automatically\n")
    print("OPTION 2: Manual Start")
    print("  - Type 'M' to get manual start commands for separate terminals\n")

    choice = input("Enter your choice (press Enter for auto-start, or M for manual): ").strip().lower()
    return choice


def start_automatic():
    """Start backend and frontend automatically"""
    print_step(5, "Starting Backend and Frontend")

    print("Starting backend on port 8000...")
    print("Starting frontend on port 3000...")
    print()

    backend_dir = Path("Socrates-8.0/backend")
    frontend_dir = Path("Socrates-8.0/frontend")

    # Get paths
    if sys.platform == "win32":
        python_exe = backend_dir / "venv" / "Scripts" / "python.exe"
        activate_script = backend_dir / "venv" / "Scripts" / "activate.ps1"
    else:
        python_exe = backend_dir / "venv" / "bin" / "python"
        activate_script = backend_dir / "venv" / "bin" / "activate"

    # Start backend
    if sys.platform == "win32":
        backend_cmd = f"cd '{backend_dir}'; & '{activate_script}'; uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"
        subprocess.Popen(["powershell", "-NoExit", "-Command", backend_cmd])
    else:
        subprocess.Popen(
            f"cd {backend_dir} && source venv/bin/activate && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000",
            shell=True
        )

    # Wait a bit for backend to start
    time.sleep(3)

    # Start frontend
    if sys.platform == "win32":
        frontend_cmd = f"cd '{frontend_dir}'; npm start"
        subprocess.Popen(["powershell", "-NoExit", "-Command", frontend_cmd])
    else:
        subprocess.Popen(
            f"cd {frontend_dir} && npm start",
            shell=True
        )

    print()
    print("=" * 80)
    print("✓ PROJECT STARTED SUCCESSFULLY!")
    print("=" * 80)
    print()
    print("Services running:")
    print("  • Backend API: http://localhost:8000")
    print("  • Frontend:    http://localhost:3000")
    print("  • API Docs:    http://localhost:8000/docs")
    print()
    print("Two new terminal windows should have opened:")
    print("  1. Backend (FastAPI on port 8000)")
    print("  2. Frontend (React on port 3000)")
    print()
    print("Opening browser in 5 seconds...")

    time.sleep(5)

    # Open browser
    import webbrowser
    webbrowser.open("http://localhost:3000")

    print("✓ Browser opened!")


def start_manual():
    """Show manual start commands"""
    print()
    print("=" * 80)
    print("MANUAL START INSTRUCTIONS")
    print("=" * 80)
    print()
    print("Open TWO separate PowerShell windows and run:\n")
    print("TERMINAL 1 - Backend (FastAPI):")
    print("-" * 80)
    print("cd Socrates-8.0\\backend")
    print(".\\venv\\Scripts\\Activate.ps1")
    print("uvicorn src.main:app --reload --host 0.0.0.0 --port 8000")
    print()
    print("TERMINAL 2 - Frontend (React):")
    print("-" * 80)
    print("cd Socrates-8.0\\frontend")
    print("npm start")
    print()
    print("Then open in browser:")
    print("  http://localhost:3000")
    print()
    print("=" * 80)


def main():
    """Main function"""
    print_header("SOCRATES 8.0 - Project Startup Script")

    # Check if we're in the right directory
    if not Path("Socrates-8.0").exists():
        print_error("This script must be run from the Socrates-8.0 project root")

    try:
        # Check prerequisites
        check_prerequisites()

        # Setup backend
        setup_backend()

        # Setup frontend
        setup_frontend()

        # Show summary
        choice = show_summary()

        if choice == 'm':
            start_manual()
        else:
            start_automatic()

    except KeyboardInterrupt:
        print("\n\nCancelled by user")
        sys.exit(0)
    except Exception as e:
        print_error(str(e))


if __name__ == "__main__":
    main()
