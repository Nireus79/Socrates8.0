# How to Start Socrates 8.0 - Quick Guide

## 🚀 Fastest Way to Start

### From File Explorer:
1. Navigate to `C:\Users\themi\PycharmProjects\Socrates8.0`
2. **Double-click** `START_PROJECT.bat` or `START_PROJECT.ps1`
3. Follow the prompts
4. Done! Both services start automatically

### From PyCharm:
1. Open the project in PyCharm
2. Right-click on `START_PROJECT.bat` (or `.ps1`)
3. Click "Run" or "Open in Terminal"
4. Follow the prompts

### From PowerShell/Command Prompt:
```powershell
# Navigate to project root
cd C:\Users\themi\PycharmProjects\Socrates8.0

# Run the startup script
.\START_PROJECT.bat
# OR
.\START_PROJECT.ps1
```

---

## What Each Script Does

### `START_PROJECT.bat` (Windows Batch)
- ✓ Works in any Command Prompt
- ✓ Checks all prerequisites (Python, Node.js, PostgreSQL)
- ✓ Creates Python virtual environment
- ✓ Installs all dependencies
- ✓ Creates .env files from templates
- ✓ Starts both backend and frontend in separate windows
- ✓ Automatically opens browser to http://localhost:3000

### `START_PROJECT.ps1` (PowerShell)
- ✓ Better formatting and colors
- ✓ Same functionality as .bat
- ✓ Recommended for Windows 10+
- ⚠ May need to allow script execution first (see below)

---

## If You Get Permission Error (PowerShell Only)

**Error:** "cannot be loaded because running scripts is disabled"

**Solution:**
```powershell
# Run PowerShell as Administrator and execute:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then you can run the script:
.\START_PROJECT.ps1
```

Or just use the `.bat` file instead - no permission needed!

---

## What Happens When You Run the Script

### Step 1: Prerequisites Check
```
✓ Python found
✓ Node.js found
✓ npm found
✓ PostgreSQL found (or warning if not installed)
```

### Step 2: Backend Setup
```
✓ Virtual environment created (first time only)
✓ Virtual environment activated
✓ Backend dependencies installed (first time only)
✓ .env file created from template (first time only)
```

### Step 3: Frontend Setup
```
✓ Frontend .env created (first time only)
✓ Frontend dependencies installed (first time only)
```

### Step 4: Start Services
```
Two new terminal windows open:
  Terminal 1: Backend (FastAPI) on port 8000
  Terminal 2: Frontend (React) on port 3000
Browser opens automatically to http://localhost:3000
```

---

## What to Do After Services Start

### First Time Setup Only:
1. **Edit backend .env file:**
   - File: `Socrates-8.0/backend/.env`
   - Add your Claude API key: `CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxx`
   - Save the file

2. **Wait for backend to say "Application startup complete"**
   - Then refresh your browser

### Every Time After:
- Script does everything automatically!
- Services start in 30-45 seconds
- Just wait for the browser to open

---

## Understanding the Output

### Backend Terminal (Port 8000):
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Started server process [1234]
INFO:     Application startup complete.
```
✓ Backend is ready when you see "Application startup complete"

### Frontend Terminal (Port 3000):
```
Local:            http://localhost:3000
On Your Network:  http://192.168.x.x:3000

webpack compiled successfully
```
✓ Frontend is ready when you see "webpack compiled successfully"

---

## How to Access Services

Once running, open these in your browser:

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Main app (Register, Login, Chat) |
| Backend API | http://localhost:8000 | REST API endpoints |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| Health Check | http://localhost:8000/health | Check if backend is running |

---

## Stopping Services

### Manual Stop:
- Click the X button on each terminal window
- Or press `Ctrl+C` in each terminal

### Keep Running:
- Leave the terminals open
- Services run as long as you leave terminals open
- Closing terminals stops the services

---

## Restarting Services

### To Restart:
1. Close both terminal windows (or press Ctrl+C)
2. Run the startup script again:
   ```powershell
   .\START_PROJECT.bat
   # or
   .\START_PROJECT.ps1
   ```

### It's Fast the Second Time:
- No reinstalling dependencies (only first time)
- Starts in ~30 seconds instead of 2-3 minutes

---

## Troubleshooting

### "Python not found"
- Install Python 3.11+ from https://python.org/
- During installation, **CHECK** "Add Python to PATH"
- Restart your terminal

### "Node.js not found"
- Install Node.js 18+ from https://nodejs.org/
- Install will add npm automatically
- Restart your terminal

### "PostgreSQL not found"
- Backend won't work without PostgreSQL
- See README.md "Running Without Docker" section
- Or install from https://postgresql.org/

### "Port 3000 already in use"
- Another service is using the port
- Close that service or edit `.env` to use different port

### "Port 8000 already in use"
- Another service is using the port
- Close that service or edit `.env` to use different port

### Frontend shows blank page
- Wait 10 seconds for it to fully load
- Refresh the browser (F5)
- Check backend is running at http://localhost:8000/docs

### Backend won't start
- Check .env file has correct DATABASE_URL
- Make sure PostgreSQL is running
- Check logs in backend terminal for errors

---

## Advanced Options (Manual Start)

If you want more control, run the script and choose **Option 2: Manual Start**

This will show you the exact commands to run in separate terminals:

```powershell
# Terminal 1 - Backend
cd Socrates-8.0\backend
.\venv\Scripts\Activate.ps1
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd Socrates-8.0\frontend
npm start
```

---

## Quick Checklist

Before running the script, make sure you have:

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] PostgreSQL 15+ installed (or you accept the warning)
- [ ] Claude API key ready
- [ ] Project folder downloaded/cloned

---

## Environment Variables (First Time Only)

### Backend .env (Socrates-8.0/backend/.env)
```
DATABASE_URL=postgresql://socrates:socrates123@localhost:5432/socrates_db
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxx
JWT_SECRET_KEY=your-secret-key-here
```

### Frontend .env (Socrates-8.0/frontend/.env)
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
```

Script creates these automatically - you just need to add Claude API key!

---

## That's It!

You're ready to go! 🚀

```
Run: .\START_PROJECT.bat
Wait: 30-45 seconds
Enjoy: http://localhost:3000
```

If you have any issues, check the troubleshooting section above or see README.md for more details.
