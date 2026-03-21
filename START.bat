@echo off
title AI SAAS ENTERPRISE - SAFE LAUNCHER
color 0A
echo ========================================
echo    AI SAAS ENTERPRISE - SAFE LAUNCHER
echo ========================================
echo.

:: Step 1: Kill ALL Python processes
echo [1/4] Stopping all Python processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM streamlit.exe >nul 2>&1
timeout /t 3 /nobreak >nul

:: Step 2: Force kill port 8501
echo [2/4] Cleaning port 8501...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501') do (
    taskkill /F /PID %%a >nul 2>&1
)
timeout /t 2 /nobreak >nul

:: Step 3: Start fresh
echo [3/4] Starting AI SaaS...
start /B python -m streamlit run saas_ai_enterprise.py --server.port 8501 --server.address 127.0.0.1

:: Step 4: Wait and open browser
echo [4/4] Waiting for server...
timeout /t 8 /nobreak >nul
start http://localhost:8501

echo.
echo ========================================
echo ✅ APP IS RUNNING SAFELY!
echo 📍 URL: http://localhost:8501
echo 📍 Close this window to stop
echo ========================================
pause