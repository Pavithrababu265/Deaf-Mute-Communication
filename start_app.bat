@echo off
set TF_CPP_MIN_LOG_LEVEL=2
set TF_ENABLE_ONEDNN_OPTS=0
echo Checking Python environment...

REM Try using Python Launcher to find 3.11
py -3.11 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Found Python 3.11!
    echo Installing dependencies...
    py -3.11 -m pip install -r requirements.txt
    py -3.11 -m pip install pyopenssl
    echo Starting Relay Server...
    start "EchoServer" py -3.11 src/server.py
    echo Starting Web Bridge...
    start "EchoWeb" py -3.11 src/web_bridge.py
    timeout /t 2
    echo Starting Main App...
    py -3.11 src/welcome_gui.py
    pause
    exit /b
)

REM Try using Python Launcher to find 3.10
py -3.10 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Found Python 3.10!
    echo Installing dependencies...
    py -3.10 -m pip install -r requirements.txt
    echo Starting Relay Server...
    start "EchoServer" py -3.10 src/server.py
    echo Starting Web Bridge...
    start "EchoWeb" py -3.10 src/web_bridge.py
    timeout /t 2
    echo Starting Main App...
    py -3.10 src/welcome_gui.py
    pause
    exit /b
)

REM Fallback: Check default python version
python --version > temp_ver.txt
set /p VER=<temp_ver.txt
del temp_ver.txt
echo Default Python is: %VER%

echo.
echo WARNING: Could not find Python 3.10 or 3.11 specifically.
echo If your default python is 3.14+, this will likely fail.
echo.
echo Attempting to run with default 'python'...
python -m pip install -r requirements.txt
python src/welcome_gui.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Main app crushed or failed to start.
    echo Launching MOCK MODE for demonstration...
    timeout /t 3
    python src/mock_main.py
)

pause
