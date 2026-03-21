@echo off
title AI SAAS ENTERPRISE INSTALLER
color 0A
echo ========================================
echo    AI SAAS ENTERPRISE - INSTALLATION
echo ========================================
echo.
echo Step 1: Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Installing...
    winget install -e --id Python.Python.3.14
)

echo Step 2: Checking Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo Installing AI Engine...
    winget install -e --id Ollama.Ollama
)

echo Step 3: Downloading AI Model (first time only)...
ollama pull qwen2.5:7b-instruct

echo Step 4: Installing Python Packages...
pip install streamlit pandas pillow pytesseract requests PyPDF2

echo Step 5: Creating Desktop Shortcut...
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = oWS.ExpandEnvironmentStrings("%UserProfile%\\Desktop\\AI SaaS.lnk") >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "C:\AI_Enterprise_Pro\START_APP.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "C:\AI_Enterprise_Pro" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

echo Step 6: Creating Auto-Start Service...
schtasks /create /tn "AIEnterprisePro" /tr "python -m streamlit run C:\AI_Enterprise_Pro\saas_ai_enterprise.py --server.port 8501 --server.address 0.0.0.0" /sc onstart /ru SYSTEM /rl HIGHEST /f >nul 2>&1
schtasks /run /tn "AIEnterprisePro" >nul 2>&1

echo.
echo ========================================
echo ✅ INSTALLATION COMPLETE!
echo.
echo 📍 App is running at: http://localhost:8501
echo 📍 Desktop shortcut created
echo 📍 Auto-starts with Windows
echo.
echo Press any key to open the app...
pause >nul
start http://localhost:8501
echo ========================================
pause