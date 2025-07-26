# LUNA - Neurodivergent Mental Health Companion Setup Script (Windows PowerShell)
# Usage: .\setup_bot.ps1

param(
    [switch]$Force
)

# Set error action preference
$ErrorActionPreference = "Stop"

Write-Host "🌙 Setting up LUNA - Neurodivergent Mental Health Companion (Windows)..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✨ This will install all dependencies and set up LUNA locally" -ForegroundColor Green
Write-Host ""

# Function to check if command exists
function Test-CommandExists {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Function to check if running as administrator
function Test-IsAdmin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check system requirements
Write-Host "🔍 Checking system requirements..." -ForegroundColor Yellow

# Check Python 3.9+
if (-not (Test-CommandExists "python")) {
    Write-Host "❌ Python 3 is required but not installed." -ForegroundColor Red
    Write-Host "   Please install Python 3.9 or higher from https://python.org" -ForegroundColor Red
    Write-Host "   Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    exit 1
}

try {
    $pythonVersion = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    Write-Host "✅ Python $pythonVersion found" -ForegroundColor Green
    
    # Check if Python version is 3.9+
    $version = [version]$pythonVersion
    if ($version -lt [version]"3.9") {
        Write-Host "❌ Python 3.9 or higher is required. Found: $pythonVersion" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ Could not determine Python version" -ForegroundColor Red
    exit 1
}

# Check Git
if (-not (Test-CommandExists "git")) {
    Write-Host "❌ Git is required but not installed." -ForegroundColor Red
    Write-Host "   Please install Git from https://git-scm.com" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Git found" -ForegroundColor Green

# Check/Install CMake
if (-not (Test-CommandExists "cmake")) {
    Write-Host "⚠️  CMake not found. Attempting automatic installation..." -ForegroundColor Yellow
    
    # Try different Windows package managers
    if (Test-CommandExists "choco") {
        Write-Host "📦 Installing CMake using Chocolatey..." -ForegroundColor Blue
        try {
            choco install cmake -y
        }
        catch {
            Write-Host "❌ Chocolatey installation failed: $_" -ForegroundColor Red
        }
    }
    elseif (Test-CommandExists "winget") {
        Write-Host "📦 Installing CMake using winget..." -ForegroundColor Blue
        try {
            winget install Kitware.CMake
        }
        catch {
            Write-Host "❌ winget installation failed: $_" -ForegroundColor Red
        }
    }
    elseif (Test-CommandExists "scoop") {
        Write-Host "📦 Installing CMake using Scoop..." -ForegroundColor Blue
        try {
            scoop install cmake
        }
        catch {
            Write-Host "❌ Scoop installation failed: $_" -ForegroundColor Red
        }
    }
    else {
        Write-Host "❌ Could not automatically install CMake." -ForegroundColor Red
        Write-Host "   Please install CMake manually using one of these methods:" -ForegroundColor Yellow
        Write-Host "   • Download from: https://cmake.org/download/" -ForegroundColor Yellow
        Write-Host "   • Install Chocolatey: Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" -ForegroundColor Yellow
        Write-Host "     Then run: choco install cmake" -ForegroundColor Yellow
        Write-Host "   • Or use winget: winget install Kitware.CMake" -ForegroundColor Yellow
        exit 1
    }
    
    # Refresh PATH to pick up newly installed cmake
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    # Verify installation was successful
    if (-not (Test-CommandExists "cmake")) {
        Write-Host "❌ CMake installation failed. Please install manually from https://cmake.org/download/" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ CMake installed successfully" -ForegroundColor Green
}
else {
    try {
        $cmakeVersion = (cmake --version | Select-Object -First 1) -replace "cmake version ", ""
        Write-Host "✅ CMake $cmakeVersion found" -ForegroundColor Green
    }
    catch {
        Write-Host "✅ CMake found" -ForegroundColor Green
    }
}

Write-Host ""

# Create virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Creating Python virtual environment..." -ForegroundColor Blue
    python -m venv .venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}
else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Blue
& ".venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "⬆️  Upgrading pip..." -ForegroundColor Blue
python -m pip install --upgrade pip --quiet
Write-Host "✅ Pip upgraded" -ForegroundColor Green

# Install Python dependencies
Write-Host "📚 Installing Python dependencies..." -ForegroundColor Blue
pip install -r requirements.txt --quiet
Write-Host "✅ Python dependencies installed" -ForegroundColor Green

# Clone and build llama.cpp if not exists
if (-not (Test-Path "llama.cpp")) {
    Write-Host "🤖 Cloning llama.cpp repository..." -ForegroundColor Blue
    git clone https://github.com/ggerganov/llama.cpp.git --quiet
    Write-Host "✅ llama.cpp repository cloned" -ForegroundColor Green
}
else {
    Write-Host "✅ llama.cpp repository already exists" -ForegroundColor Green
}

Set-Location "llama.cpp"

# Build llama.cpp using CMake
if (-not (Test-Path "build\bin\llama-cli.exe")) {
    Write-Host "🔨 Building llama.cpp with CMake (this may take a few minutes)..." -ForegroundColor Blue
    
    if (-not (Test-Path "build")) {
        New-Item -ItemType Directory -Name "build" | Out-Null
    }
    
    Set-Location "build"
    
    # Configure with CMake
    cmake ..
    
    # Build (use number of processors for parallel build)
    $processors = $env:NUMBER_OF_PROCESSORS
    if (-not $processors) { $processors = 4 }
    
    cmake --build . --config Release --parallel $processors
    
    Set-Location ".."
    Write-Host "✅ llama.cpp built successfully" -ForegroundColor Green
}
else {
    Write-Host "✅ llama.cpp already built" -ForegroundColor Green
}

Set-Location ".."

# Download model if not exists
$modelFile = "llama.cpp\models\TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"
if (-not (Test-Path $modelFile)) {
    Write-Host "📥 Downloading TinyLlama model (this may take a few minutes)..." -ForegroundColor Blue
    
    if (-not (Test-Path "llama.cpp\models")) {
        New-Item -ItemType Directory -Path "llama.cpp\models" -Force | Out-Null
    }
    
    Set-Location "llama.cpp\models"
    
    $modelUrl = "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    $modelPath = "TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"
    
    try {
        # Use PowerShell's built-in web client for download with progress
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($modelUrl, $modelPath)
        Write-Host "✅ TinyLlama model downloaded" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Model download failed: $_" -ForegroundColor Red
        Write-Host "   Please download manually from: $modelUrl" -ForegroundColor Yellow
        Set-Location "..\..\"
        exit 1
    }
    
    Set-Location "..\..\"
}
else {
    Write-Host "✅ TinyLlama model already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 LUNA setup completed successfully!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🚀 To start LUNA, run: .\.venv\Scripts\Activate.ps1; python neurodivergent_chatbot.py" -ForegroundColor Yellow
Write-Host "🌐 LUNA will be available at: http://127.0.0.1:7860" -ForegroundColor Yellow
Write-Host "⏹️  Press Ctrl+C to stop LUNA when running" -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Quick start: .\setup_bot.ps1; .\.venv\Scripts\Activate.ps1; python neurodivergent_chatbot.py" -ForegroundColor Cyan
Write-Host "🌙 Welcome to your neurodivergent-friendly mental health companion!" -ForegroundColor Magenta
Write-Host ""
