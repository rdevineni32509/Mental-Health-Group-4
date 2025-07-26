#!/bin/bash

# LUNA One-Command Launcher
# Automatically handles setup if needed, then runs LUNA

echo "🌙 Starting LUNA - Neurodivergent Mental Health Companion..."

# Check if setup is needed
if [ ! -d ".venv" ] || [ ! -d "llama.cpp" ] || [ ! -f "llama.cpp/models/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf" ]; then
    echo "🔧 Setup required. Running setup process..."
    ./setup_bot.sh
    echo "✅ Setup completed!"
else
    echo "✅ Setup already completed, launching LUNA..."
fi

# Activate virtual environment and run LUNA
echo "🚀 Launching LUNA..."
source .venv/bin/activate && python neurodivergent_chatbot.py
