# ============================================================================
# Socrates 8.0 - One-Click Project Starter (PowerShell Version)
# ============================================================================
# This script starts both backend and frontend with all required setup
# Simply run this file and follow the prompts
# ============================================================================

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "          SOCRATES 8.0 - Project Startup Script" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "Socrates-8.0")) {
    Write-Host "ERROR: This script must be run from the Socrates-8.0 project root" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[1/5] Checking Prerequisites..." -ForegroundColor Yellow
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: Python not found. Please install Python 3.11+ and add to PATH" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: Node.js not found. Please install from https://nodejs.org/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check npm
try {
    $npmVersion = npm --version 2>&1
    Write-Host "✓ npm found: $npmVersion" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: npm not found" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check PostgreSQL
try {
    $psqlVersion = psql --version 2>&1
    Write-Host "✓ PostgreSQL found: $psqlVersion" -ForegroundColor Green
}
catch {
    Write-Host "⚠ WARNING: PostgreSQL not found or not in PATH" -ForegroundColor Yellow
    Write-Host "  If you haven't set up PostgreSQL, please do so first" -ForegroundColor Yellow
    Write-Host "  See README.md 'Running Without Docker' section" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit 0
    }
}

Write-Host ""
Write-Host "[2/5] Setting up Backend..." -ForegroundColor Yellow
Write-Host ""

Push-Location "Socrates-8.0\backend"

# Check if venv exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}
else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

# Activate venv
& ".\venv\Scripts\Activate.ps1"

# Install backend dependencies
Write-Host "Installing backend dependencies..."
pip install -q -r requirements.txt
Write-Host "✓ Backend dependencies installed" -ForegroundColor Green

# Create .env if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..."
    Copy-Item ".env.example" ".env"
    Write-Host ""
    Write-Host "⚠ IMPORTANT: Edit the .env file and add your Claude API key!" -ForegroundColor Yellow
    Write-Host "File: Socrates-8.0\backend\.env" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Required variables:" -ForegroundColor Yellow
    Write-Host "  CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxx" -ForegroundColor Yellow
    Write-Host "  DATABASE_URL=postgresql://socrates:socrates123@localhost:5432/socrates_db" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to continue"
}
else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

Pop-Location

Write-Host ""
Write-Host "[3/5] Setting up Frontend..." -ForegroundColor Yellow
Write-Host ""

Push-Location "Socrates-8.0\frontend"

# Create .env if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..."
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Frontend .env created" -ForegroundColor Green
}
else {
    Write-Host "✓ Frontend .env already exists" -ForegroundColor Green
}

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing frontend dependencies (this may take a minute)..."
    npm install --silent
    Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green
}
else {
    Write-Host "✓ node_modules already exists" -ForegroundColor Green
}

Pop-Location

Write-Host ""
Write-Host "[4/5] Summary and Next Steps" -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Setup Complete! The project is ready to run." -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You now have TWO options:" -ForegroundColor Cyan
Write-Host ""
Write-Host "OPTION 1: Automatic Start (Recommended)" -ForegroundColor Green
Write-Host "  - Press Enter to start both backend and frontend automatically" -ForegroundColor Green
Write-Host ""
Write-Host "OPTION 2: Manual Start" -ForegroundColor Green
Write-Host "  - Type 'M' to get manual start commands for separate terminals" -ForegroundColor Green
Write-Host ""

$choice = Read-Host "Enter your choice (press Enter for auto-start, or M for manual)"

if ($choice -eq "M" -or $choice -eq "m") {
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host "                      MANUAL START INSTRUCTIONS" -ForegroundColor Cyan
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Open TWO separate PowerShell windows and run:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "TERMINAL 1 - Backend (FastAPI):" -ForegroundColor Green
    Write-Host "────────────────────────────────────────────────────────────────────────" -ForegroundColor Gray
    Write-Host "cd Socrates-8.0\backend" -ForegroundColor White
    Write-Host ".\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "uvicorn src.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor White
    Write-Host ""
    Write-Host "TERMINAL 2 - Frontend (React):" -ForegroundColor Green
    Write-Host "────────────────────────────────────────────────────────────────────────" -ForegroundColor Gray
    Write-Host "cd Socrates-8.0\frontend" -ForegroundColor White
    Write-Host "npm start" -ForegroundColor White
    Write-Host ""
    Write-Host "Then open in browser:" -ForegroundColor Green
    Write-Host "  http://localhost:3000" -ForegroundColor White
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 0
}

Write-Host ""
Write-Host "[5/5] Starting Backend and Frontend..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Starting backend on port 8000..." -ForegroundColor Green
Write-Host ""

# Start backend in new PowerShell window
$backendScript = {
    cd "Socrates-8.0\backend"
    .\venv\Scripts\Activate.ps1
    uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
}
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "$backendScript" -WindowStyle Normal

# Wait for backend to start
Start-Sleep -Seconds 3

Write-Host "Starting frontend on port 3000..." -ForegroundColor Green
Write-Host ""

# Start frontend in new PowerShell window
$frontendScript = {
    cd "Socrates-8.0\frontend"
    npm start
}
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "$frontendScript" -WindowStyle Normal

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "                    ✓ PROJECT STARTED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Services running:" -ForegroundColor Green
Write-Host "  • Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "  • Frontend:    http://localhost:3000" -ForegroundColor White
Write-Host "  • API Docs:    http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Two new PowerShell windows should have opened:" -ForegroundColor Cyan
Write-Host "  1. Backend (FastAPI on port 8000)" -ForegroundColor White
Write-Host "  2. Frontend (React on port 3000)" -ForegroundColor White
Write-Host ""
Write-Host "Opening browser in 5 seconds..." -ForegroundColor Yellow

Start-Sleep -Seconds 5

# Open browser
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "✓ Browser opened! Press Enter to close this window..." -ForegroundColor Green
Read-Host ""
