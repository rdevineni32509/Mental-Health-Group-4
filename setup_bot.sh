#!/bin/bash

# LUNA - Neurodivergent Mental Health Companion Setup Script
# Single command setup: ./setup_bot.sh && python neurodivergent_chatbot.py

set -e  # Exit on any error

echo "🌙 Setting up LUNA - Neurodivergent Mental Health Companion..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ This will install all dependencies and set up LUNA locally"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check system requirements
echo "🔍 Checking system requirements..."

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
    cd build
    cmake ..
    make -j$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
    cd ..
    echo "✅ llama.cpp built successfully"
else
    echo "✅ llama.cpp already built"
fi

cd ..

# Download model if not exists
MODEL_FILE="llama.cpp/models/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"
if [ ! -f "$MODEL_FILE" ]; then
    echo "📥 Downloading TinyLlama model (this may take a few minutes)..."
    mkdir -p llama.cpp/models
    cd llama.cpp/models
    
    # Try different download methods
    if command_exists wget; then
        wget -q --show-progress -O TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    elif command_exists curl; then
        curl -L -o TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    else
        echo "❌ Neither wget nor curl found. Please install one of them to download the model."
        exit 1
    fi
    cd ../..
    echo "✅ TinyLlama model downloaded"
else
    echo "✅ TinyLlama model already exists"
fi

echo ""
echo "🎉 LUNA setup completed successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 To start LUNA, run: python neurodivergent_chatbot.py"
echo "🌐 LUNA will be available at: http://127.0.0.1:7860"
echo "⏹️  Press Ctrl+C to stop LUNA when running"
echo ""
echo "💡 Quick start: ./setup_bot.sh && python neurodivergent_chatbot.py"
echo "🌙 Welcome to your neurodivergent-friendly mental health companion!"
echo ""
