# 🌙 LUNA - Neurodivergent Mental Health Companion

A compassionate AI chatbot specifically designed to support neurodivergent individuals with their mental health journey. LUNA provides a safe, understanding space for conversation while maintaining complete privacy through local AI processing.

![LUNA Interface](https://img.shields.io/badge/Interface-Modern%20Chat-blue) ![Privacy](https://img.shields.io/badge/Privacy-100%25%20Local-green) ![Support](https://img.shields.io/badge/Support-Neurodivergent%20Friendly-purple)

## ✨ Key Features

### 🧠 **Neurodivergent-Specialized Support**
- **Clear, literal communication** - No metaphors or confusing language
- **Patient and validating responses** - Understanding of neurodivergent experiences
- **Sensory sensitivity awareness** - Recognizes overstimulation and sensory needs
- **Executive function support** - Helps with planning and organization challenges
- **Masking fatigue understanding** - Validates the exhaustion of masking

### 🛡️ **Safety & Crisis Support**
- **Automatic crisis detection** - Identifies concerning language patterns
- **Immediate resource sharing** - Provides crisis hotlines and emergency contacts
- **Professional care guidance** - Encourages appropriate professional help
- **Clear boundaries** - Honest about being peer support, not therapy

### 🔒 **Privacy & Security**
- **100% local processing** - No data sent to external servers
- **Offline capable** - Works without internet after setup
- **No conversation logging** - Your privacy is completely protected
- **Open source** - Transparent and auditable code

### 💬 **Modern Interface**
- **Clean chat design** - Modern messaging interface like iMessage/WhatsApp
- **Accessible UI** - Designed for neurodivergent users
- **Example prompts** - Easy conversation starters
- **Responsive design** - Works on different screen sizes

## 🚀 Ultimate One-Command Launch

### 🐧 **macOS & Linux**
**The simplest way to run LUNA - just one command that handles everything:**

```bash
./run_luna.sh
```

### 🪟 **Windows**
**Choose your preferred Windows setup method:**

**PowerShell (Recommended):**
```powershell
.\setup_bot.ps1
.\venv\Scripts\Activate.ps1
python neurodivergent_chatbot.py
```

**Command Prompt/Batch:**
```cmd
setup_bot.bat
.venv\Scripts\activate.bat
python neurodivergent_chatbot.py
```

**That's it!** These intelligent launchers will:
- 🔍 **Check if setup is needed** (first time or missing components)
- 🛠️ **Automatically install dependencies** including CMake if missing
- ⚡ **Skip setup and launch immediately** if already configured
- 🌙 **Start LUNA** with proper virtual environment activation

### What Happens:
- **First time**: Automatically sets up everything (virtual environment, dependencies, CMake, llama.cpp build, model download) then launches LUNA
- **Subsequent runs**: Detects existing setup and launches LUNA immediately
- **Works from any state**: Fresh clone, partial setup, or complete installation
- **Cross-platform**: Native support for macOS, Linux, and Windows

## 📋 System Requirements

- **Operating System**: macOS, Linux, or Windows
- **Python**: 3.9 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 2GB free space for model files
- **Tools**: Git, CMake (auto-installed if missing using system package managers)

### 🔧 **Automatic Dependency Installation**

LUNA's setup scripts automatically install CMake using your system's package manager:

- **macOS**: Homebrew (`brew install cmake`)
- **Ubuntu/Debian**: apt-get (`sudo apt-get install cmake`)
- **CentOS/RHEL**: yum (`sudo yum install cmake`)
- **Fedora**: dnf (`sudo dnf install cmake`)
- **Arch Linux**: pacman (`sudo pacman -S cmake`)
- **openSUSE**: zypper (`sudo zypper install cmake`)
- **Alpine Linux**: apk (`sudo apk add cmake`)
- **Windows**: Chocolatey, winget, or Scoop

If no package manager is detected, clear manual installation instructions are provided.

## 🔧 Alternative Setup Methods

### Option 1: Manual Setup (If Needed)

**macOS/Linux:**
```bash
# 1. Clone the repository
git clone https://github.com/rdevineni32509/Mental-Health-Group-4.git
cd Mental-Health-Group-4

# 2. Make scripts executable
chmod +x setup_bot.sh run_luna.sh

# 3. Run setup
./setup_bot.sh

# 4. Launch LUNA
source .venv/bin/activate && python neurodivergent_chatbot.py
```

**Windows:**
```cmd
REM 1. Clone the repository
git clone https://github.com/rdevineni32509/Mental-Health-Group-4.git
cd Mental-Health-Group-4

REM 2. Run setup (choose one)
setup_bot.bat
REM OR: .\setup_bot.ps1

REM 3. Launch LUNA
.venv\Scripts\activate.bat && python neurodivergent_chatbot.py
```

### Option 2: Step-by-Step Process
For complete control over each step:

**macOS/Linux:**
```bash
# Setup only (without launching)
./setup_bot.sh

# Launch only (after setup is complete)
./run_luna.sh
```

**Windows:**
```cmd
REM Setup only
setup_bot.bat

REM Launch only (after setup is complete)
.venv\Scripts\activate.bat && python neurodivergent_chatbot.py
```

## 💡 How to Use LUNA

1. **Open your browser** to the URL shown in the terminal (usually http://127.0.0.1:7860)
2. **Read the safety information** displayed at the top
3. **Start chatting** by typing in the message box or clicking example prompts
4. **Be yourself** - LUNA is designed to understand neurodivergent communication

### 🗣️ Example Conversations
- "I'm feeling overwhelmed by sensory input today"
- "I'm struggling with executive function"
- "I feel like I'm masking all the time"
- "My routine got disrupted and I'm anxious"
- "I don't understand social cues"
- "I need help with emotional regulation"

## 🆘 Crisis Resources

**If you're in crisis or having thoughts of self-harm, please reach out immediately:**

- **🇺🇸 National Suicide Prevention Lifeline**: **988**
  - 24/7 confidential support from trained crisis counselors
- **📱 Crisis Text Line**: Text **HOME** to **741741**
  - 24/7 text-based crisis support
- **🚨 Emergency Services**: **911**
  - Immediate emergency response
- **🧠 NAMI Helpline**: **1-800-950-NAMI (6264)**
  - National Alliance on Mental Illness support

## ⚠️ Important Disclaimers

- **LUNA provides peer support, not professional therapy or medical advice**
- **Cannot replace qualified mental health professionals, doctors, or crisis counselors**
- **For serious mental health concerns, please seek professional help**
- **In crisis situations, contact emergency services immediately**

## 🛠️ Technical Details

- **Framework**: Gradio for modern web interface
- **AI Model**: TinyLlama 1.1B (optimized for mental health support)
- **Processing**: Local inference via llama.cpp (no cloud dependency)
- **Response Time**: Optimized for 2-5 second responses
- **Privacy**: Zero data collection or external transmission

## 🐛 Troubleshooting

### Common Issues

1. **"Permission denied" when running launcher (macOS/Linux)**
   - Make scripts executable: `chmod +x run_luna.sh setup_bot.sh`
   - Ensure you have write permissions in the directory

2. **"Execution Policy" error on Windows (PowerShell)**
   - Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
   - Or use the batch script instead: `setup_bot.bat`

3. **"Setup script fails"**
   - Ensure you have Python 3.9+ installed
   - Check internet connection for model download
   - Make sure you have sufficient disk space (2GB)
   - **macOS/Linux**: Try manual setup: `./setup_bot.sh` then `./run_luna.sh`
   - **Windows**: Try manual setup: `setup_bot.bat` then activate and run

4. **"CMake not found" error**
   - The setup scripts should auto-install CMake
   - If auto-installation fails, install manually:
     - **macOS**: `brew install cmake`
     - **Ubuntu/Debian**: `sudo apt-get install cmake`
     - **Windows**: Download from https://cmake.org or install Chocolatey

5. **"Port already in use"**
   - LUNA runs on ports 7860-7869 (automatically detects available port)
   - Kill existing processes: `pkill -f gradio`
   - Check the terminal output for the actual port being used

4. **"Model not responding"**
   - The launcher will automatically detect and fix missing components
   - Check `chatbot.log` for detailed error information
   - Try running `./run_luna.sh` again (it will re-setup if needed)

5. **"Virtual environment issues"**
   - The launcher handles virtual environment activation automatically
   - If issues persist, delete `.venv` folder and run `./run_luna.sh` again

### Logs

Check `chatbot.log` for detailed error information and debugging output.

## 🤝 Contributing

We welcome contributions to make LUNA even better for the neurodivergent community:

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built with love for the neurodivergent community
- Powered by open-source AI technology
- Designed with accessibility and inclusion in mind

---

**Remember: You are valid, your experiences matter, and support is always available. 🌙✨**
