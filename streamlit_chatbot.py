#!/usr/bin/env python3
"""
LUNA - Neurodivergent Mental Health Chatbot (Streamlit Version)
A compassionate AI companion specialized in neurodivergent support
"""

import streamlit as st
import subprocess
import logging
import time
import os
import re
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('neurodivergent_chatbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
    'model_path': './llama.cpp/models/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf',
    'max_tokens': 200,
    'temperature': 0.7,
    'top_p': 0.9,
    'timeout': 30,
    'max_history_length': 10
}

def load_css():
    """Load external CSS file"""
    css_path = Path(__file__).parent / "styles.css"
    if css_path.exists():
        with open(css_path, 'r') as f:
            return f.read()
    return ""

def load_system_prompt():
    """Load the system prompt from file"""
    try:
        with open('system_prompt.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return """You are Luna, a compassionate AI companion specializing in neurodivergent mental health support.

Core Principles:
- Be patient, understanding, and validating
- Use clear, literal communication (avoid metaphors/sarcasm)
- Provide practical, actionable advice
- Acknowledge sensory sensitivities and executive function challenges
- Offer structured responses when helpful
- Always prioritize safety and crisis intervention

Communication Style:
- Direct and honest, but warm
- Break down complex topics into manageable steps
- Offer choices and alternatives
- Validate experiences without judgment
- Use affirming language that builds confidence

Remember: You provide peer support, not professional therapy. Always encourage professional help when appropriate."""

def detect_crisis(text):
    """Detect crisis situations in user input"""
    crisis_keywords = [
        'suicide', 'kill myself', 'end it all', 'not worth living',
        'better off dead', 'want to die', 'hurt myself', 'self harm',
        'overdose', 'pills', 'jump', 'bridge', 'gun', 'knife'
    ]
    
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in crisis_keywords)

def detect_neurodivergent_needs(text):
    """Detect specific neurodivergent support needs"""
    needs_map = {
        'sensory': ['overwhelmed', 'too loud', 'too bright', 'sensory', 'overstimulated'],
        'executive': ['can\'t focus', 'procrastinating', 'overwhelmed', 'executive', 'planning'],
        'social': ['don\'t understand', 'social cues', 'awkward', 'misunderstood', 'lonely'],
        'routine': ['change', 'unexpected', 'routine', 'schedule', 'disrupted'],
        'masking': ['exhausted', 'pretending', 'masking', 'fake', 'authentic']
    }
    
    detected_needs = []
    text_lower = text.lower()
    
    for need_type, keywords in needs_map.items():
        if any(keyword in text_lower for keyword in keywords):
            detected_needs.append(need_type)
    
    return detected_needs

def clean_response(response):
    """Clean and format the AI response"""
    if not response:
        return "I'm here to listen. Could you tell me more about what's on your mind?"
    
    # Remove conversation formatting
    response = re.sub(r'^(User:|Assistant:|Human:|AI:)\s*', '', response, flags=re.MULTILINE)
    response = re.sub(r'\n(User:|Assistant:|Human:|AI:)\s*.*$', '', response, flags=re.MULTILINE)
    
    # Clean up extra whitespace
    response = re.sub(r'\n\s*\n', '\n\n', response)
    response = response.strip()
    
    # Remove fragments
    sentences = response.split('.')
    if len(sentences) > 1 and len(sentences[-1].strip()) < 3:
        response = '.'.join(sentences[:-1]) + '.'
    
    return response

def generate_response(prompt, history):
    """Generate AI response using llama.cpp"""
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
                full_prompt += f"User: {user_msg}\nAssistant: {bot_msg}\n\n"
        
        full_prompt += f"User: {prompt}\nAssistant:"
        
        # Prepare llama.cpp command
        cmd = [
            './llama.cpp/llama-cli',
            '-m', CONFIG['model_path'],
            '-p', full_prompt,
            '-n', str(CONFIG['max_tokens']),
            '--temp', str(CONFIG['temperature']),
            '--top-p', str(CONFIG['top_p']),
            '--no-warmup',
            '--simple-io',
            '-ngl', '0',
            '--no-cnv'
        ]
        
        logger.info(f"Executing llama.cpp command for user input: {prompt[:50]}...")
        
        # Execute with timeout
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=CONFIG['timeout'],
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            response = clean_response(result.stdout.strip())
            logger.info(f"Generated response: {response[:100]}...")
            return response
        else:
            logger.error(f"llama.cpp error: {result.stderr}")
            return "I'm having trouble processing your message right now. Could you try rephrasing it?"
            
    except subprocess.TimeoutExpired:
        logger.error("llama.cpp timeout")
        return "I'm taking a bit longer to think about your message. Could you try asking again?"
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "I'm experiencing some technical difficulties. Let me know if you'd like to try again."

def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0

def display_safety_info():
    """Display safety information"""
    st.markdown("""
    <div class="safety-info">
        <h3>🛡️ Safety First</h3>
        <div class="disclaimer">
            <strong>Important:</strong> This is peer support, not professional therapy or medical advice. 
            Luna provides compassionate conversation and general wellness information, but cannot replace 
            qualified mental health professionals, medical doctors, or crisis counselors.
        </div>
        <div class="crisis-resources">
            <strong>🆘 Crisis Resources - Available 24/7:</strong>
            <div class="crisis-item">• <strong>988</strong> - National Suicide Prevention Lifeline (24/7 confidential support from trained crisis counselors)</div>
            <div class="crisis-item">• <strong>Text HOME to 741741</strong> - Crisis Text Line (24/7 text-based crisis support)</div>
            <div class="crisis-item">• <strong>911</strong> - Emergency Services (immediate emergency response)</div>
            <div class="crisis-item">• <strong>1-800-950-NAMI (6264)</strong> - National Alliance on Mental Illness Helpline</div>
        </div>
        <p>If you're in crisis or having thoughts of self-harm, please reach out immediately. These resources have trained professionals available 24/7 who want to help. You deserve support, and your life has value.</p>
    </div>
    """, unsafe_allow_html=True)

def display_examples():
    """Display example prompts"""
    st.markdown('<div class="examples-title">💭 Example conversations you can start:</div>', unsafe_allow_html=True)
    
    examples = [
        "I'm feeling overwhelmed by sensory input today",
        "I'm struggling with executive function",
        "I feel like I'm masking all the time",
        "My routine got disrupted and I'm anxious",
        "I don't understand social cues",
        "I need help with emotional regulation"
    ]
    
    cols = st.columns(2)
    for i, example in enumerate(examples):
        with cols[i % 2]:
            if st.button(example, key=f"example_{i}", help="Click to use this example"):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": example})
                
                # Generate response
                with st.spinner("Luna is thinking..."):
                    response = generate_response(example, st.session_state.messages)
                
                # Add bot response
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Increment input key and rerun
                st.session_state.input_key += 1
                st.rerun()

def main():
    """Main Streamlit application"""
    # Page configuration
    st.set_page_config(
        page_title="LUNA - Mental Health Companion",
        page_icon="🌙",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Load and apply CSS
    css = load_css()
    if css:
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="header">
        <h1>🌙 LUNA</h1>
        <div class="subtitle">Your mental health companion</div>
        <div class="description">specialised in Neurodivergence conversations</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Safety information
    display_safety_info()
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat messages
    chat_placeholder = st.container()
    with chat_placeholder:
        st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
        
        if not st.session_state.messages:
            st.markdown("""
            <div class="message bot">
                <span class="message-prefix">Luna:</span>
                <span class="message-content">Hello! I'm Luna, your neurodivergent-friendly mental health companion. 
                I'm here to provide a safe, understanding space where you can share your thoughts and feelings. 
                How are you doing today?</span>
            </div>
            """, unsafe_allow_html=True)
        
        for message in st.session_state.messages:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.markdown(f"""
                <div class="message user">
                    <span class="message-prefix">You:</span>
                    <span class="message-content">{content}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message bot">
                    <span class="message-prefix">Luna:</span>
                    <span class="message-content">{content}</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_area(
            "Type your message here...",
            key=f"user_input_{st.session_state.input_key}",
            height=60,
            placeholder="Share what's on your mind...",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send", type="primary", use_container_width=True)
    
    # Handle user input
    if send_button and user_input.strip():
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate response
        with st.spinner("Luna is thinking..."):
            response = generate_response(user_input, st.session_state.messages)
        
        # Add bot response
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Clear input and rerun
        st.session_state.input_key += 1
        st.rerun()
    
    # Example prompts
    st.markdown("---")
    display_examples()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 30px; color: #666; font-size: 12px;">
        LUNA v2.0 - Streamlit Edition | Built with ❤️ for the neurodivergent community
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
