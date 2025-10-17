# Troubleshooting Guide - Socrates 8.0

This document provides solutions to common issues encountered when running Socrates 8.0.

## Frontend Compilation Issues

### Issue: "The `active:bg-primary-800` class does not exist"

**Symptoms:**
- Frontend fails to compile with error about missing Tailwind CSS classes
- Error appears even though colors are defined in `tailwind.config.js`
- Usually happens on first run or after updates

**Root Cause:**
This is typically caused by a stale or incomplete npm installation. The npm cache or node_modules directory can become corrupted, preventing Tailwind CSS from properly compiling the color classes.

**Solution:**

1. **Stop the current processes:**
   ```bash
   # Press Ctrl+C in both terminal windows if running
   ```

2. **Clear npm cache:**
   ```bash
   cd Socrates-8.0/frontend
   npm cache clean --force
   ```

3. **Delete node_modules and package-lock.json:**
   ```bash
   # On Windows Command Prompt:
   rmdir /s /q node_modules
   del package-lock.json

   # Or on PowerShell:
   Remove-Item -Recurse -Force node_modules
   Remove-Item package-lock.json -Force
   ```

4. **Reinstall dependencies:**
   ```bash
   npm install
   ```

5. **Retry the startup script:**
   ```bash
   python start_project.py
   ```

**Prevention:**
The updated `start_project.py` now automatically cleans the npm cache on subsequent runs. On first run, it does a fresh install. This should prevent this issue from recurring.

---

## Port Already in Use

### Issue: "Something is already running on port 3000" or "Address already in use" on port 8000

**Symptoms:**
- Frontend or backend fails to start
- Port conflict error appears
- Usually happens when restarting quickly or after a crash

**Root Cause:**
A previous instance of the backend or frontend is still running and hasn't released the port.

**Solution:**

1. **The startup script now handles this automatically:**
   - It checks for lingering processes on ports 8000 and 3000
   - It kills them before starting new instances
   - No manual intervention needed

2. **Manual solution (if needed):**
   ```bash
   # Find process on port 3000:
   netstat -ano | findstr :3000

   # Kill it (replace XXXX with the PID from above):
   taskkill /PID XXXX /F

   # Repeat for port 8000:
   netstat -ano | findstr :8000
   taskkill /PID XXXX /F
   ```

---

## Backend Issues

### Issue: "ModuleNotFoundError" or missing backend dependencies

**Symptoms:**
- Backend crashes on startup
- Error about missing Python packages
- Usually happens after updating requirements.txt

**Solution:**

1. **Reinstall backend dependencies:**
   ```bash
   cd Socrates-8.0/backend

   # Activate virtual environment:
   venv\Scripts\activate.bat  # Windows CMD
   source venv/bin/activate   # Linux/Mac or PowerShell

   # Reinstall:
   pip install -r requirements.txt
   ```

2. **Or use the startup script:**
   ```bash
   python start_project.py
   ```
   The script will detect and reinstall missing dependencies.

### Issue: PostgreSQL connection error

**Symptoms:**
- Backend fails to connect to database
- Error: "could not translate host name"
- Error: "connection refused"

**Root Cause:**
PostgreSQL is not running or database URL is incorrect.

**Solution:**

1. **Verify PostgreSQL is running:**
   ```bash
   # Windows: Check if service is running
   Get-Service | findstr postgresql

   # Or restart the service:
   net start postgresql-x64-XX  # Replace XX with version
   ```

2. **Verify database URL in `.env`:**
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/socrates_db
   ```

3. **Create the database if it doesn't exist:**
   ```bash
   createdb -U postgres socrates_db
   ```

---

## Frontend Issues

### Issue: Blank page or "Cannot GET /"

**Symptoms:**
- Frontend loads but shows blank page
- Console errors about API connection
- "Cannot GET /" or similar 404 error

**Root Cause:**
Usually caused by:
- Backend not running
- Incorrect API URL in frontend `.env`
- CORS configuration issue

**Solution:**

1. **Verify backend is running:**
   - Check that port 8000 is listening: `netstat -ano | findstr :8000`
   - Or check: http://localhost:8000/docs (should show Swagger UI)

2. **Check frontend `.env` file:**
   ```
   REACT_APP_API_URL=http://localhost:8000
   REACT_APP_WS_URL=ws://localhost:8000
   ```

3. **Clear browser cache:**
   - Press Ctrl+Shift+Delete in browser
   - Clear all cache and cookies
   - Refresh the page

### Issue: CSS not loading or Tailwind styles missing

**Symptoms:**
- UI looks unstyled (no colors, wrong layout)
- Tailwind classes not applying
- Same appearance as when Tailwind.config.js was not working

**Solution:**

1. **Clear browser cache:**
   ```bash
   # In browser: Ctrl+Shift+Delete
   # Or hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
   ```

2. **Rebuild frontend:**
   ```bash
   cd Socrates-8.0/frontend
   npm run build
   ```

3. **If problem persists, do a clean install:**
   ```bash
   npm cache clean --force
   rmdir /s /q node_modules
   del package-lock.json
   npm install
   npm start
   ```

---

## Virtual Environment Issues

### Issue: "venv: No module named..."

**Symptoms:**
- Backend virtual environment fails to activate
- Error about Python installation
- Backend won't start

**Solution:**

1. **Recreate the virtual environment:**
   ```bash
   cd Socrates-8.0/backend

   # Remove old venv
   rmdir /s /q venv

   # Create new one
   python -m venv venv

   # Activate and install dependencies
   venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```

2. **Or use the startup script:**
   ```bash
   python start_project.py
   ```

---

## Debugging Tips

### Check if services are running:

```bash
# Backend:
curl http://localhost:8000/docs

# Frontend:
curl http://localhost:3000

# Check ports:
netstat -ano | findstr ":8000\|:3000"
```

### View logs:

```bash
# Backend logs are shown in the terminal window
# Frontend logs are shown in the terminal window
# Look for errors starting with ERROR or ✗
```

### Enable verbose logging:

**Backend:**
- Edit `Socrates-8.0/backend/src/main.py`
- Add logging configuration

**Frontend:**
- Open browser DevTools (F12)
- Check Console tab for errors

---

## Still Having Issues?

If none of these solutions work:

1. **Check that all prerequisites are installed:**
   - Python 3.8+
   - Node.js 16+
   - PostgreSQL 14+

2. **Try a complete clean restart:**
   ```bash
   # Kill all Node and Python processes
   taskkill /IM node.exe /F
   taskkill /IM python.exe /F

   # Wait 5 seconds
   timeout /t 5

   # Run startup script
   python start_project.py
   ```

3. **Check file permissions:**
   - Ensure you have write access to `Socrates-8.0/` directory
   - Especially for `.env` files and `node_modules/`

4. **Review the README.md** for complete setup instructions

---

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'uvicorn'` | Backend deps not installed | Run `pip install -r requirements.txt` |
| `Port XXXX already in use` | Process still running | Kill it or use different port |
| `CORS policy: No 'Access-Control-Allow-Origin'` | Backend not running or CORS not configured | Start backend, check CORS settings |
| `Cannot find module 'react'` | Frontend deps not installed | Run `npm install` |
| `SyntaxError: Unexpected token...` | Tailwind/CSS compilation error | Do clean npm install |
| `psql: FATAL: role "postgres" does not exist` | PostgreSQL not properly installed | Reinstall PostgreSQL or use correct user |

---

## Performance Tips

1. **Frontend builds slowly:**
   - Close other heavy applications
   - Ensure antivirus isn't scanning node_modules
   - Use an SSD for better performance

2. **Backend starts slowly:**
   - First start after reboot is slower
   - Subsequent starts are faster
   - Check database connection speed

3. **High memory usage:**
   - npm/Node.js can use significant memory
   - Try: `npm ci` instead of `npm install` (faster)
   - Close other applications if needed

---

## Getting Help

- Check this file first for common issues
- Review error messages carefully - they usually indicate the problem
- Check the README.md for setup instructions
- Review `.env` file configuration
- Ensure all prerequisites are installed

Last updated: October 17, 2025
