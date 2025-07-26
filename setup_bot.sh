#!/bin/bash

# Mental Health Chatbot Setup Script
# Enhanced with error handling and dependency checks

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check system requirements
check_requirements() {
    log "Checking system requirements..."
    
    if ! command_exists python3; then
        log_error "Python 3 is required but not installed."
        echo "Please install Python 3 and try again."
        exit 1
    fi
    
    if ! command_exists git; then
        log_error "Git is required but not installed."
        echo "Please install Git and try again."
        exit 1
    fi
    
    if ! command_exists make; then
        log_error "Make is required but not installed."
        echo "Please install build tools (Xcode Command Line Tools on macOS) and try again."
        exit 1
    fi
    
    if ! command_exists cmake; then
        log_error "CMake is required but not installed."

# Check Python 3.9+
if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed."
    echo "   Please install Python 3.9 or higher from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $PYTHON_VERSION found"

# Check Git
if ! command_exists git; then
    echo "❌ Git is required but not installed."
    echo "   Please install Git from https://git-scm.com"
    exit 1
fi
echo "✅ Git found"

# Check/Install CMake
if ! command_exists cmake; then
    echo "⚠️  CMake not found. Attempting to install..."
    if command_exists brew; then
        brew install cmake
    elif command_exists apt-get; then
        sudo apt-get update && sudo apt-get install -y cmake
    elif command_exists yum; then
        sudo yum install -y cmake
    else
        echo "❌ Please install CMake manually from https://cmake.org"
        exit 1
    fi
fi
echo "✅ CMake found"

echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ Pip upgraded"

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt --quiet
echo "✅ Python dependencies installed"

# Clone and build llama.cpp if not exists
if [ ! -d "llama.cpp" ]; then
    echo "🤖 Cloning llama.cpp repository..."
    git clone https://github.com/ggerganov/llama.cpp.git --quiet
    echo "✅ llama.cpp repository cloned"
else
    echo "✅ llama.cpp repository already exists"
fi

cd llama.cpp

# Build llama.cpp using CMake
if [ ! -f "build/bin/llama-cli" ]; then
    echo "🔨 Building llama.cpp with CMake (this may take a few minutes)..."
    if [ ! -d "build" ]; then
        mkdir build
    fi
    log "Building llama.cpp with CMake..."
    
    # Create build directory
    mkdir -p build
    cd build
    
    # Configure with CMake
    if cmake ..; then
        log_success "CMake configuration successful"
    else
        log_error "CMake configuration failed"
        echo "Please ensure CMake is installed and try again."
        exit 1
    fi
    
    # Build the project
    if cmake --build . --config Release; then
        log_success "llama.cpp built successfully"
    else
        log_error "Failed to build llama.cpp"
        echo "Please check the error messages above and ensure you have the necessary build tools installed."
        exit 1
    fi
    
    # Move back to llama.cpp directory
    cd ..
    
    cd ..
}

# Download model
download_model() {
    log "⬇️ Downloading TinyLlama model..."
    
    MODEL_DIR="llama.cpp/models"
    MODEL_FILE="TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"
    MODEL_PATH="$MODEL_DIR/$MODEL_FILE"
    MODEL_URL="https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"
    
    mkdir -p "$MODEL_DIR"
    
    if [ -f "$MODEL_PATH" ]; then
        log_warning "Model file already exists, skipping download"
        # Verify file size (should be around 669MB)
        FILE_SIZE=$(stat -f%z "$MODEL_PATH" 2>/dev/null || stat -c%s "$MODEL_PATH" 2>/dev/null || echo "0")
        if [ "$FILE_SIZE" -lt 600000000 ]; then
            log_warning "Model file seems incomplete, re-downloading..."
            rm -f "$MODEL_PATH"
        else
            log_success "Model file verified"
            return 0
        fi
    fi
    
    cd "$MODEL_DIR"
    
    log "Downloading model (this may take a few minutes)..."
    if curl -L --progress-bar -o "$MODEL_FILE" "$MODEL_URL"; then
        log_success "Model downloaded successfully"
    else
        log_error "Failed to download model"
        echo "Please check your internet connection and try again."
        exit 1
    fi
    
    cd ../../
}

# Verify installation
verify_installation() {
    log "🔍 Verifying installation..."
    
    # Check if all required files exist
    REQUIRED_FILES=(
        "llama.cpp/build/bin/llama-cli"
        "llama.cpp/models/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"
        "system_prompt.txt"
        "run_bot.py"
    )
    
    for file in "${REQUIRED_FILES[@]}"; do
        if [ ! -f "$file" ]; then
            log_error "Required file missing: $file"
            exit 1
        fi
    done
    
    # Test llama.cpp executable
    if ./llama.cpp/build/bin/llama-cli --help >/dev/null 2>&1; then
        log_success "llama.cpp executable is working"
    else
        log_error "llama.cpp executable is not working properly"
        exit 1
    fi
    
    log_success "Installation verified successfully"
}

# Main setup function
main() {
    echo "🤖 Mental Health Chatbot Setup"
    echo "=============================="
    echo
    
    check_requirements
    setup_venv
    install_python_deps
    setup_llama
    download_model
    verify_installation
    
    echo
    log_success "Setup completed successfully!"
    echo
    echo "To start the chatbot, run:"
    echo "  source .venv/bin/activate"
    echo "  python run_bot.py"
    echo
    echo "Or simply run this script again - it will detect the existing setup and launch the bot."
}

# Check if this is a fresh setup or if we should just launch
if [ -f "llama.cpp/build/bin/llama-cli" ] && [ -f "llama.cpp/models/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf" ] && [ -d ".venv" ]; then
    log "🚀 Setup detected, launching chatbot..."
    source .venv/bin/activate
    python run_bot.py
else
    main
fi
