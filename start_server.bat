@echo off
where python >nul 2>&1
if %errorlevel% neq 0 (
  echo [ERROR] Python is not installed.
  echo Please download from https://python.org
  pause
  exit /b 1
)

echo [1/2] Installing packages...
python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
  echo [ERROR] Package installation failed.
  pause
  exit /b 1
)

echo [2/2] Starting server...
echo.
echo  Open http://localhost:3000 in your browser.
echo  Press Ctrl+C to stop the server.
echo.

python server.py
pause
