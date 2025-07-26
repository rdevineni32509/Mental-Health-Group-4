# 🌱 Mental Health Chatbot

A compassionate, neurodivergent-friendly chatbot designed to provide mental health support using local AI inference.

## ✨ Features

- **Neurodivergent-Friendly Design**: Clear, literal communication with patience and understanding
- **Privacy-First**: Runs entirely locally - no data sent to external servers
- **Comprehensive Error Handling**: Robust error management and graceful failure recovery
- **Safety Features**: Built-in crisis detection and resource sharing
- **Modern UI**: Clean, accessible Gradio interface
- **Logging**: Detailed logging for debugging and monitoring

## 🚀 Quick Start

1. **Clone or download this repository**
2. **Run the setup script**:
   ```bash
   chmod +x setup_bot.sh
   ./setup_bot.sh
   ```
3. **The chatbot will launch automatically** at `http://localhost:7860`

## 📋 Requirements

- **Python 3.8+**
- **Git**
- **Build tools** (Xcode Command Line Tools on macOS, build-essential on Linux)
- **curl**
- **~2GB free disk space** (for model and dependencies)

## 🛠️ Manual Setup

If the automated setup doesn't work, you can set up manually:

```bash
# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Build llama.cpp
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make
cd ..

# 4. Download model
mkdir -p llama.cpp/models
cd llama.cpp/models
curl -L -o TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf \
  https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf
cd ../../

# 5. Run the chatbot
python run_bot.py
```

## 🎯 Usage

1. **Start the chatbot** using `./setup_bot.sh` or `python run_bot.py`
2. **Open your browser** to `http://localhost:7860`
3. **Begin chatting** - the bot is designed to be patient and understanding

- **Operating System**: macOS, Linux, or Windows
- **Python**: 3.9 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 2GB free space for model files
- **Tools**: Git, CMake (auto-installed if missing)

## 🔧 Manual Setup (If Needed)

If the single command doesn't work, you can set up manually:

```bash
# 1. Clone the repository
git clone https://github.com/rdevineni32509/Mental-Health-Group-4.git
cd Mental-Health-Group-4

# 2. Make setup script executable
chmod +x setup_bot.sh

# 3. Run setup
./setup_bot.sh

# 4. Launch LUNA
python neurodivergent_chatbot.py
```
├── setup_bot.sh            # Automated setup script
├── system_prompt.txt       # Comprehensive system prompt for the AI
├── requirements.txt        # Python dependencies
├── README.md              # This documentation
├── chatbot.log            # Application logs (created at runtime)
├── .venv/                 # Python virtual environment
└── llama.cpp/             # Local LLM inference engine
    ├── main               # Compiled executable
    └── models/            # AI model files
        └── TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf
```

## 🔧 Configuration

Key settings can be modified in `run_bot.py`:

```python
CONFIG = {
    'system_prompt_file': 'system_prompt.txt',
    'llama_executable': './llama.cpp/main',
    'model_path': 'llama.cpp/models/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf',
    'max_tokens': 200,
    'max_input_length': 1000,
    'max_history_length': 10
}
```

## 🐛 Troubleshooting

### Common Issues

1. **"llama.cpp executable not found"**
   - Run `./setup_bot.sh` to build llama.cpp
   - Ensure build tools are installed

2. **"Model file not found"**
   - Check internet connection and re-run setup
   - Manually download model if needed

3. **Python import errors**
   - Activate virtual environment: `source .venv/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`

4. **Port already in use**
   - The app runs on port 7860 by default
   - Kill existing processes or modify the port in `run_bot.py`

### Logs

Check `chatbot.log` for detailed error information and debugging output.

## 🤝 Contributing

This project is designed to support neurodivergent individuals. When contributing:

1. **Maintain accessibility** - clear, literal language
2. **Preserve safety features** - never remove crisis detection
3. **Test thoroughly** - ensure error handling works
4. **Document changes** - update README and comments

## ⚠️ Important Notes

- **Not a replacement for professional care**: This is peer support, not therapy
- **Privacy**: All processing happens locally, but logs are stored on disk
- **Limitations**: AI responses may not always be perfect - use judgment
- **Crisis situations**: Always prioritize professional help for serious concerns

## 📄 License

This project is intended for educational and support purposes. Please use responsibly and in accordance with mental health best practices.

---

**Remember**: You deserve support, understanding, and care. This tool is here to help, but professional mental health resources are always available when you need them. 💙
