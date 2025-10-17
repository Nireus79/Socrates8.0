@echo off
REM ============================================================================
REM Socrates 8.0 - One-Click Project Starter
REM ============================================================================
REM This script starts both backend and frontend with all required setup
REM Simply run this file and follow the prompts
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================================
echo          SOCRATES 8.0 - Project Startup Script
echo ============================================================================
echo.

REM Check if we're in the right directory
if not exist "Socrates-8.0" (
    echo ERROR: This script must be run from the Socrates-8.0 project root
    echo Current directory: %cd%
    pause
    exit /b 1
)

echo [1/5] Checking Prerequisites...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11+ and add to PATH
    pause
    exit /b 1
)
echo ✓ Python found: %errorlevel%

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)
echo ✓ Node.js found

REM Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: npm not found
    pause
    exit /b 1
)
echo ✓ npm found

REM Check PostgreSQL
psql --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: PostgreSQL not found or not in PATH
    echo If you haven't set up PostgreSQL, please do so first
    echo See README.md "Running Without Docker" section
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "!continue!"=="y" exit /b 1
)
echo ✓ PostgreSQL check complete

echo.
echo [2/5] Setting up Backend...
echo.

cd Socrates-8.0\backend

REM Check if venv exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate venv
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

REM Install backend dependencies
echo Installing backend dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
echo ✓ Backend dependencies installed

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env >nul
    echo.
    echo ⚠ IMPORTANT: Edit the .env file and add your Claude API key!
    echo File: Socrates-8.0\backend\.env
    echo.
    echo Required variables:
    echo   CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxx
    echo   DATABASE_URL=postgresql://socrates:socrates123@localhost:5432/socrates_db
    echo.
    pause
) else (
    echo ✓ .env file already exists
)

cd ..\..

echo.
echo [3/5] Setting up Frontend...
echo.

cd Socrates-8.0\frontend

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env >nul
    echo ✓ Frontend .env created
) else (
    echo ✓ Frontend .env already exists
)

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing frontend dependencies (this may take a minute)...
    call npm install --silent
    if errorlevel 1 (
        echo ERROR: Failed to install npm dependencies
        pause
        exit /b 1
    )
    echo ✓ Frontend dependencies installed
) else (
    echo ✓ node_modules already exists
)

cd ..\..

echo.
echo [4/5] Summary and Next Steps
echo.
echo ============================================================================
echo Setup Complete! The project is ready to run.
echo ============================================================================
echo.
echo You now have TWO options:
echo.
echo OPTION 1: Automatic Start (Recommended)
echo   - Press any key to start both backend and frontend automatically
echo.
echo OPTION 2: Manual Start
echo   - Press 'M' to get manual start commands to run in separate terminals
echo.

set /p choice="Enter your choice (press Enter for auto-start, or M for manual): "

if /i "%choice%"=="M" (
    goto manual_start
) else (
    goto auto_start
)

:auto_start
echo.
echo [5/5] Starting Backend and Frontend...
echo.
echo Starting backend on port 8000...
echo.

REM Start backend in a new window
start "Socrates 8.0 - Backend (FastAPI)" cmd /k "cd Socrates-8.0\backend && venv\Scripts\activate.bat && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
timeout /t 3 /nobreak

echo Starting frontend on port 3000...
echo.

REM Start frontend in a new window
start "Socrates 8.0 - Frontend (React)" cmd /k "cd Socrates-8.0\frontend && npm start"

echo.
echo ============================================================================
echo                    ✓ PROJECT STARTED SUCCESSFULLY!
echo ============================================================================
echo.
echo Services running:
echo   • Backend API: http://localhost:8000
echo   • Frontend:    http://localhost:3000
echo   • API Docs:    http://localhost:8000/docs
echo.
echo Two new terminal windows should have opened:
echo   1. Backend (FastAPI on port 8000)
echo   2. Frontend (React on port 3000)
echo.
echo Opening browser in 5 seconds...
timeout /t 5 >nul

REM Open browser to frontend
start http://localhost:3000

echo.
echo Press any key to close this window...
pause >nul
exit /b 0

:manual_start
echo.
echo ============================================================================
echo                      MANUAL START INSTRUCTIONS
echo ============================================================================
echo.
echo Open TWO separate PowerShell/Command Prompt windows and run:
echo.
echo TERMINAL 1 - Backend (FastAPI):
echo ────────────────────────────────────────────────────────────────────────
cd /d %cd%
echo cd Socrates-8.0\backend
echo .\venv\Scripts\activate.bat
echo uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo TERMINAL 2 - Frontend (React):
echo ────────────────────────────────────────────────────────────────────────
echo cd Socrates-8.0\frontend
echo npm start
echo.
echo Then open in browser:
echo   http://localhost:3000
echo.
echo ============================================================================
echo.
pause
exit /b 0
