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

## 🚀 Quick Start (Single Command)

**Just run this one command to set up and launch LUNA:**

```bash
./setup_bot.sh && python neurodivergent_chatbot.py
```

That's it! This command will:
1. ✅ Create a virtual environment
2. ✅ Install all Python dependencies
3. ✅ Download and build the AI model (llama.cpp)
4. ✅ Download the TinyLlama model file
5. ✅ Launch LUNA in your browser at http://127.0.0.1:7860

## 📋 System Requirements

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

1. **"Setup script fails"**
   - Ensure you have Python 3.9+ installed
   - Check internet connection for model download
   - Make sure you have sufficient disk space (2GB)

2. **"Port already in use"**
   - LUNA runs on port 7860 by default
   - Kill existing processes: `pkill -f gradio`
   - The app will automatically try ports 7860-7869

3. **"Model not responding"**
   - Check that llama.cpp built successfully
   - Verify model file downloaded completely
   - Check `chatbot.log` for detailed error information

4. **"Permission denied"**
   - Make setup script executable: `chmod +x setup_bot.sh`
   - Ensure you have write permissions in the directory

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
