@echo off
REM LUNA - Neurodivergent Mental Health Companion Setup Script (Windows Batch)
REM Usage: setup_bot.bat

echo 🌙 Setting up LUNA - Neurodivergent Mental Health Companion (Windows)...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ✨ This will install all dependencies and set up LUNA locally
echo.

REM Check system requirements
echo 🔍 Checking system requirements...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 is required but not installed.
    echo    Please install Python 3.9 or higher from https://python.org
    echo    Make sure to check 'Add Python to PATH' during installation
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found

REM Check Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is required but not installed.
    echo    Please install Git from https://git-scm.com
    pause
    exit /b 1
)
echo ✅ Git found

REM Check CMake
cmake --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  CMake not found. Attempting automatic installation...
    
    REM Try Chocolatey first
    choco --version >nul 2>&1
    if not errorlevel 1 (
        echo 📦 Installing CMake using Chocolatey...
        choco install cmake -y
        goto :cmake_check
    )
    
    REM Try winget
    winget --version >nul 2>&1
    if not errorlevel 1 (
        echo 📦 Installing CMake using winget...
        winget install Kitware.CMake
        goto :cmake_check
    )
    
    REM No package manager found
    echo ❌ Could not automatically install CMake.
    echo    Please install CMake manually:
    echo    • Download from: https://cmake.org/download/
    echo    • Or install Chocolatey first: https://chocolatey.org/install
    echo      Then run: choco install cmake
    echo    • Or use winget: winget install Kitware.CMake
    pause
    exit /b 1
    
    :cmake_check
    REM Refresh PATH and check again
    call refreshenv >nul 2>&1
    cmake --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ CMake installation failed. Please install manually.
        pause
        exit /b 1
    )
    echo ✅ CMake installed successfully
) else (
    for /f "tokens=3" %%i in ('cmake --version ^| findstr "cmake version"') do set CMAKE_VERSION=%%i
    echo ✅ CMake %CMAKE_VERSION% found
)

echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv .venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip --quiet
echo ✅ Pip upgraded

REM Install Python dependencies
echo 📚 Installing Python dependencies...
pip install -r requirements.txt --quiet
echo ✅ Python dependencies installed

REM Clone and build llama.cpp if not exists
if not exist "llama.cpp" (
    echo 🤖 Cloning llama.cpp repository...
    git clone https://github.com/ggerganov/llama.cpp.git --quiet
    echo ✅ llama.cpp repository cloned
) else (
    echo ✅ llama.cpp repository already exists
)

cd llama.cpp

REM Build llama.cpp using CMake
if not exist "build\bin\llama-cli.exe" (
    echo 🔨 Building llama.cpp with CMake (this may take a few minutes)...
    
    if not exist "build" mkdir build
    cd build
    
    REM Configure with CMake
    cmake ..
    
    REM Build with parallel processing
    cmake --build . --config Release --parallel %NUMBER_OF_PROCESSORS%
    
    cd ..
    echo ✅ llama.cpp built successfully
) else (
    echo ✅ llama.cpp already built
)

cd ..

REM Download model if not exists
if not exist "llama.cpp\models\TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf" (
    echo 📥 Downloading TinyLlama model (this may take a few minutes)...
    
    if not exist "llama.cpp\models" mkdir "llama.cpp\models"
    cd llama.cpp\models
    
    REM Try to download using PowerShell (available on Windows 10+)
    powershell -Command "& {(New-Object System.Net.WebClient).DownloadFile('https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf', 'TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf')}"
    
    if errorlevel 1 (
        echo ❌ Model download failed.
        echo    Please download manually from:
        echo    https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
        cd ..\..
        pause
        exit /b 1
    )
    
    cd ..\..
    echo ✅ TinyLlama model downloaded
) else (
    echo ✅ TinyLlama model already exists
)

echo.
echo 🎉 LUNA setup completed successfully!
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🚀 To start LUNA, run: .venv\Scripts\activate.bat ^&^& python neurodivergent_chatbot.py
echo 🌐 LUNA will be available at: http://127.0.0.1:7860
echo ⏹️  Press Ctrl+C to stop LUNA when running
echo.
echo 💡 Quick start: setup_bot.bat ^&^& .venv\Scripts\activate.bat ^&^& python neurodivergent_chatbot.py
echo 🌙 Welcome to your neurodivergent-friendly mental health companion!
echo.
pause
