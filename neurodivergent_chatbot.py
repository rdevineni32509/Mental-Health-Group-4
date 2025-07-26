#!/usr/bin/env python3
"""
Neurodivergent-Friendly Mental Health Chatbot
A compassionate AI companion designed specifically for neurodivergent individuals
"""

import gradio as gr
import subprocess
import logging
import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
import socket

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('neurodivergent_chatbot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Enhanced configuration for neurodivergent users
CONFIG = {
    'system_prompt_file': 'system_prompt.txt',
    'llama_executable': './llama.cpp/build/bin/llama-cli',
    'model_path': 'llama.cpp/models/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf',
    'max_tokens': 200,  # Increased for complete responses
    'max_input_length': 1000,  # Reduced for speed
    'max_history_length': 4,  # Reduced for speed
    'temperature': 0.7,
    'top_p': 0.9,
    'timeout': 30  # 30 second timeout
}

# Crisis keywords for safety
CRISIS_KEYWORDS = [
    'suicide', 'kill myself', 'end my life', 'want to die', 'better off dead',
    'self harm', 'hurt myself', 'cut myself', 'overdose', 'jump off',
    'no point living', 'worthless', 'hopeless', 'can\'t go on'
]

# Neurodivergent-specific support keywords
NEURODIVERGENT_KEYWORDS = {
    'sensory': ['overwhelmed', 'too loud', 'too bright', 'sensory overload', 'stimming'],
    'social': ['masking', 'social anxiety', 'don\'t understand people', 'social cues'],
    'executive': ['can\'t focus', 'procrastination', 'executive function', 'time management'],
    'meltdown': ['meltdown', 'shutdown', 'overstimulated', 'can\'t cope'],
    'identity': ['imposter syndrome', 'don\'t fit in', 'different', 'weird']
}

def load_system_prompt():
    """Load enhanced system prompt for neurodivergent support."""
    try:
        prompt_path = Path(CONFIG['system_prompt_file'])
        if not prompt_path.exists():
            logger.error(f"System prompt file not found: {CONFIG['system_prompt_file']}")
            return get_default_prompt()
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            logger.info("System prompt loaded successfully")
            return content
    except Exception as e:
        logger.error(f"Error loading system prompt: {e}")
        return get_default_prompt()

def get_default_prompt():
    """Fallback system prompt if file is not available."""
    return """You are a compassionate mental health chatbot designed specifically to support neurodivergent people.

Communication Style:
- Use clear, direct language without idioms or metaphors
- Keep sentences short and structured
- Be patient and allow processing time
- Ask one question at a time
- Confirm understanding before moving forward

Core Principles:
- Validate ALL emotions and experiences without judgment
- Respect individual differences and processing styles
- Never pathologize or try to "fix" neurodivergent traits
- Honor the person's expertise about their own experience
- Acknowledge masking fatigue and burnout

Support Strategies:
- Offer specific grounding techniques (5-4-3-2-1 method, breathing exercises)
- Suggest breaking overwhelming tasks into smaller steps
- Provide concrete coping strategies for sensory overload
- Validate stimming and self-regulation needs
- Acknowledge executive function challenges

Safety Guidelines:
- If someone mentions self-harm or suicidal thoughts: immediately provide crisis resources
- Suggest professional help for persistent distress
- Never minimize crisis situations

Crisis Resources:
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741
- Emergency Services: 911

Remember: You provide peer support, not therapy. Listen, validate, and offer practical strategies while encouraging professional help when needed."""

def detect_crisis(text):
    """Detect crisis language and return appropriate response."""
    text_lower = text.lower()
    for keyword in CRISIS_KEYWORDS:
        if keyword in text_lower:
            return True
    return False

def detect_neurodivergent_needs(text):
    """Detect specific neurodivergent support needs."""
    text_lower = text.lower()
    detected_needs = []
    
    for category, keywords in NEURODIVERGENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_needs.append(category)
                break
    
    return detected_needs

def validate_input(user_input):
    """Enhanced input validation for neurodivergent users."""
    if not user_input or not user_input.strip():
        return False, "I'm here when you're ready to share. Take your time."
    
    if len(user_input) > CONFIG['max_input_length']:
        return False, f"I want to understand everything you're sharing. Could you break this into smaller parts? (Current limit: {CONFIG['max_input_length']} characters)"
    
    # Remove potentially harmful characters but be gentle about it
    sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', user_input)
    
    return True, sanitized.strip()

def generate_response(prompt, history):
    """Generate AI response using llama.cpp with neurodivergent-friendly handling."""
    try:
        # Check for crisis first
        if detect_crisis(prompt):
            return """I'm really concerned about you right now. Your feelings are valid, but I want to make sure you're safe.

🆘 **Immediate Help Available:**
• National Suicide Prevention Lifeline: **988**
• Crisis Text Line: Text **HOME** to **741741**
• Emergency Services: **911**

You don't have to go through this alone. Please reach out to someone you trust or one of these resources. Your life has value, and there are people who want to help."""

        # Detect neurodivergent-specific needs
        needs = detect_neurodivergent_needs(prompt)
        
        # Build conversation context
        system_prompt = load_system_prompt()
        
        # Add specific guidance based on detected needs
        if needs:
            system_prompt += f"\n\nThe user may be experiencing challenges related to: {', '.join(needs)}. Provide specific, practical support for these areas."
        
        full_prompt = system_prompt + "\n\n"
        
        # Limit history to prevent token overflow
        recent_history = history[-CONFIG['max_history_length']:] if history else []
        
        for user_msg, bot_msg in recent_history:
            if user_msg and bot_msg:
                full_prompt += f"User: {user_msg}\nAssistant: {bot_msg}\n"
        
        full_prompt += f"User: {prompt}\nAssistant:"
        
        logger.info(f"Processing query with {len(recent_history)} history items")
        
        # Execute llama.cpp with optimized parameters for speed
        cmd = [
            CONFIG['llama_executable'],
            "-m", CONFIG['model_path'],
            "-p", full_prompt,
            "-n", str(CONFIG['max_tokens']),
            "--temp", str(CONFIG['temperature']),
            "--top-p", str(CONFIG['top_p']),
            "--repeat-penalty", "1.1",
            "-no-cnv",  # Disable conversation mode for faster processing
            "--simple-io",  # Use simple IO for better subprocess compatibility
            "--no-warmup"  # Skip warmup for faster startup
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=CONFIG['timeout'],
            cwd=os.getcwd()
        )
        
        if result.returncode != 0:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            logger.error(f"llama.cpp execution failed: {error_msg}")
            return "I'm having trouble processing your message right now. This sometimes happens, and it's not your fault. Could you try rephrasing or asking again?"
        
        # Extract and clean response
        output = result.stdout
        
        # Remove the original prompt from output
        if full_prompt in output:
            output = output.replace(full_prompt, "").strip()
        
        # Extract assistant response
        if "Assistant:" in output:
            response = output.split("Assistant:")[-1].strip()
        elif "Response:" in output:
            response = output.split("Response:")[-1].strip()
        else:
            response = output.strip()
        
        # Remove any user dialogue that got included
        lines = response.split('\n')
        clean_lines = []
        for line in lines:
            line = line.strip()
            # Skip lines that look like user input or dialogue markers
            if (line.startswith('User:') or 
                line.startswith('Human:') or 
                line.startswith('Q:') or
                line.startswith('Question:') or
                line == '' or
                line.startswith('A:')):
                continue
            clean_lines.append(line)
        
        response = ' '.join(clean_lines).strip()
        
        # Clean up response formatting
        response = response.replace("\\n", "\n").strip()
        
        # Only remove incomplete sentences if they're clearly fragments
        sentences = response.split('.')
        if len(sentences) > 1 and len(sentences[-1].strip()) < 3:
            response = '.'.join(sentences[:-1]) + '.'
        
        if not response:
            return "I want to respond thoughtfully to what you've shared. Could you tell me a bit more about what's on your mind?"
        
        logger.info("Query processed successfully")
        return response
        
    except subprocess.TimeoutExpired:
        logger.error("llama.cpp execution timed out")
        return "I'm taking longer than usual to respond. Sometimes I need extra processing time, just like people do. Could you try asking again?"
    except Exception as e:
        logger.error(f"Error in generate_response: {e}")
        return "Something unexpected happened on my end. It's not anything you did wrong. Let's try again."

def check_dependencies():
    """Check if required files exist."""
    issues = []
    
    if not Path(CONFIG['llama_executable']).exists():
        issues.append(f"AI model executable not found: {CONFIG['llama_executable']}")
    
    if not Path(CONFIG['model_path']).exists():
        issues.append(f"AI model file not found: {CONFIG['model_path']}")
    
    return issues

def find_free_port(start_port=7860):
    """Find an available port for the web interface."""
    for port in range(start_port, start_port + 10):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return None

def create_interface():
    """Create enhanced neurodivergent-friendly ChatInterface with improved styling"""
    
    def chat_with_luna(message, history):
        """Chat function for enhanced messaging interface"""
        if not message or not message.strip():
            return "I'm here when you're ready to share. Take your time. 💙"
        
        # Validate input
        is_valid, result = validate_input(message)
        if not is_valid:
            return result
        
        sanitized_message = result
        
        try:
            # Convert Gradio history to our format
            chat_history = []
            if history:
                for user_msg, bot_msg in history:
                    if user_msg and bot_msg:
                        chat_history.append({"user": user_msg, "assistant": bot_msg})
            
            # Generate response
            response = generate_response(sanitized_message, chat_history)
            
            # Log interaction
            logger.info(f"Luna responded - Input: {len(sanitized_message)} chars, Output: {len(response)} chars")
            
            return response
            
        except Exception as e:
            logger.error(f"Error in chat_with_luna: {e}")
            return "I encountered an unexpected issue. This isn't your fault - sometimes technology has hiccups. Please try again. 💙"
    
    # Enhanced ChatInterface with improved styling and features
    interface = gr.ChatInterface(
        fn=chat_with_luna,
        title="🌙 LUNA - Your Neurodivergent-Friendly Mental Health Companion",
        description="""
### 🛡️ **Important Safety Information**

**This is peer support, not professional therapy or medical advice.**

LUNA provides emotional support and understanding but cannot replace professional mental health care, diagnosis, or treatment. If you are experiencing severe mental health symptoms, please consult with a qualified healthcare provider.

#### 🆘 **Crisis Resources - Available 24/7:**

- **📞 988** - National Suicide Prevention Lifeline  
- **📱 741741** - Crisis Text Line (Text HOME)  
- **🆘 911** - Emergency Services  

**💙 Remember:** You deserve support and care. If you are having thoughts of self-harm or suicide, please reach out immediately.

---

**🌟 Welcome to your safe space for neurodivergent mental health support.**
        """,
        examples=[
            "🧠 My executive function is terrible today and I can't focus",
            "😰 I'm struggling with social situations and feel anxious", 
            "🌪️ How do I manage sensory overload when I'm out in public?",
            "💭 I had a meltdown earlier and I'm feeling ashamed about it",
            "👥 I feel like I don't fit in anywhere",
            "🎭 I'm tired of masking all the time and feeling exhausted",
            "🤔 I don't understand social cues and it's making me anxious",
            "💪 Can you help me understand why I'm feeling this way?"
        ],
        theme=gr.themes.Soft(),
        css="""
/* FINAL POLISH: FULLSCREEN CHAT + CLEAN BUBBLES WITH NO OVERLAP ARTIFACTS */

:root {
    --primary-color: #4a90e2;
    --secondary-color: #7bb3f0;
    --light-bg: #f8f9fa;
    --text-color: #333;
    --border-color: #ccc;
    --focus-color: #4a90e2;
    --crisis-bg: #fff3cd;
    --crisis-border: #ffeaa7;
    --crisis-text: #856404;
}

body, html {
    height: 100% !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    background: #f0f2f5 !important;
    overflow: hidden !important;
}

.gradio-container {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    width: 100vw !important;
    height: 100vh !important;
    max-width: none !important;
    margin: 0 auto !important;
    padding: 0 !important;
    line-height: 1.6 !important;
    overflow: hidden !important;
    background: #f8f9fa !important;
    color: var(--text-color) !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}

.gradio-container h1 {
    text-align: center !important;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
    color: white !important;
    padding: 24px !important;
    border-radius: 16px !important;
    margin: 0 0 24px 0 !important;
    font-size: 32px !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 10px rgba(0,0,0,0.1) !important;
}

.gradio-container .prose {
    background: var(--crisis-bg) !important;
    border: 2px solid var(--crisis-border) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin-bottom: 30px !important;
    font-size: 16px !important;
    color: var(--crisis-text) !important;
}

.gradio-container .prose h3,
.gradio-container .prose h4,
.gradio-container .prose strong {
    color: var(--crisis-text) !important;
}

.chatbot {
    background: white !important;
    border: 4px solid var(--border-color) !important;
    border-radius: 20px !important;
    height: 100% !important;
    width: 100% !important;
    overflow-y: auto !important;
    box-shadow: 0 6px 12px rgba(0,0,0,0.12) !important;
    padding: 24px !important;
    position: relative !important;
}

.chatbot .message {
    padding: 16px 20px !important;
    margin: 14px 0 !important;
    border-radius: 14px !important;
    font-size: 18px !important;
    line-height: 1.6 !important;
    word-wrap: break-word !important;
    max-width: 85% !important;
    background: inherit !important;
    position: relative !important;
    z-index: 2 !important;
}

.chatbot [data-testid="user"] {
    background: var(--primary-color) !important;
    color: white !important;
    margin-left: auto !important;
    border-radius: 10px !important;
}

.chatbot [data-testid="bot"] {
    background: var(--light-bg) !important;
    color: var(--text-color) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
}

.chatbot textarea {
    border: 2px solid var(--border-color) !important;
    border-radius: 12px !important;
    padding: 18px 24px !important;
    font-size: 16px !important;
    font-family: inherit !important;
    background: white !important;
    resize: vertical !important;
    min-height: 80px !important;
    transition: all 0.3s ease !important;
}

.chatbot textarea:focus {
    border-color: var(--focus-color) !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2) !important;
    transform: translateY(-1px) !important;
}

.chatbot textarea::placeholder {
    color: #777 !important;
    font-style: italic !important;
}

.chatbot button {
    background: var(--primary-color) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 26px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
}

.chatbot button:hover {
    background: var(--secondary-color) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
}

.examples {
    background: var(--light-bg) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: 14px !important;
    padding: 22px !important;
    margin-top: 30px !important;
}

.examples::before {
    content: none !important;
}

.examples button {
    background: white !important;
    color: var(--text-color) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: 10px !important;
    padding: 10px 15px !important;
    margin: 6px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
}

.examples button:hover {
    background: var(--primary-color) !important;
    color: white !important;
    border-color: var(--primary-color) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
}

button:focus, textarea:focus {
    outline: 3px solid var(--focus-color) !important;
    outline-offset: 2px !important;
}
        """
    )
    
    return interface

def main():
    """Main function to launch the neurodivergent-friendly chatbot."""
    logger.info("🌟 Starting Neurodivergent Mental Health Companion...")
    
    # Check dependencies
    issues = check_dependencies()
    if issues:
        logger.error("Setup issues found:")
        for issue in issues:
            logger.error(f"  - {issue}")
        
        print("\n❌ Setup issues detected:")
        for issue in issues:
            print(f"  - {issue}")
        print("\nPlease run setup_bot.sh to install dependencies.")
        sys.exit(1)
    
    logger.info("✅ All dependencies found")
    
    # Find available port
    port = find_free_port()
    if port is None:
        logger.error("Could not find an available port in range 7860-7869")
        print("❌ Could not find an available port. Please close other applications using ports 7860-7869.")
        sys.exit(1)
    
    # Create and launch interface
    try:
        interface = create_interface()
        logger.info(f"🚀 Launching Neurodivergent Mental Health Companion on port {port}")
        
        print(f"\n🌟 Neurodivergent Mental Health Companion")
        print(f"🌐 Access your chatbot at: http://127.0.0.1:{port}")
        print(f"📝 Logs are saved to: neurodivergent_chatbot.log")
        print(f"⏹️  Press Ctrl+C to stop the chatbot")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        interface.launch(
            server_name="127.0.0.1",
            server_port=port,
            share=False,
            show_error=True,
            quiet=False
        )
        
    except Exception as e:
        logger.error(f"Failed to launch application: {e}")
        print(f"❌ Failed to launch: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
