#!/usr/bin/env python3
"""
Mental Health Chatbot - Neurodivergent-Friendly Assistant

A compassionate chatbot designed to support neurodivergent individuals
using local LLM inference through llama.cpp.
"""

import gradio as gr
import subprocess
import logging
import os
import sys
from pathlib import Path
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
    'system_prompt_file': 'system_prompt.txt',
    'llama_executable': './llama.cpp/build/bin/llama-cli',
    'model_path': 'llama.cpp/models/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf',
    'max_tokens': 200,
    'max_input_length': 1000,
    'max_history_length': 10
}

def load_system_prompt():
    """Load system prompt with error handling."""
    try:
        prompt_path = Path(CONFIG['system_prompt_file'])
        if not prompt_path.exists():
            logger.error(f"System prompt file not found: {CONFIG['system_prompt_file']}")
            return "You are a helpful assistant."
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            logger.info("System prompt loaded successfully")
            return content
    except Exception as e:
        logger.error(f"Error loading system prompt: {e}")
        return "You are a helpful assistant."

def validate_input(user_input):
    """Validate and sanitize user input."""
    if not user_input or not user_input.strip():
        return False, "Please enter a message."
    
    # Check length
    if len(user_input) > CONFIG['max_input_length']:
        return False, f"Message too long. Please keep it under {CONFIG['max_input_length']} characters."
    
    # Basic sanitization - remove potentially harmful characters
    sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', user_input)
    
    return True, sanitized.strip()

def check_dependencies():
    """Check if required files and executables exist."""
    issues = []
    
    # Check llama.cpp executable
    if not Path(CONFIG['llama_executable']).exists():
        issues.append(f"llama.cpp executable not found: {CONFIG['llama_executable']}")
    
    # Check model file
    if not Path(CONFIG['model_path']).exists():
        issues.append(f"Model file not found: {CONFIG['model_path']}")
    
    # Check system prompt
    if not Path(CONFIG['system_prompt_file']).exists():
        issues.append(f"System prompt file not found: {CONFIG['system_prompt_file']}")
    
    return issues

def query_llama(prompt, history):
    """Query the LLaMA model with proper error handling."""
    try:
        # Validate input
        is_valid, result = validate_input(prompt)
        if not is_valid:
            return result
        
        sanitized_prompt = result
        
        # Build conversation context
        system_prompt = load_system_prompt()
        full_prompt = system_prompt + "\n\n"
        
        # Limit history to prevent token overflow
        recent_history = history[-CONFIG['max_history_length']:] if history else []
        
        for user_msg, bot_msg in recent_history:
            if user_msg and bot_msg:
                full_prompt += f"User: {user_msg}\nBot: {bot_msg}\n"
        
        full_prompt += f"User: {sanitized_prompt}\nBot:"
        
        logger.info(f"Processing query with {len(recent_history)} history items")
        
        # Execute llama.cpp with timeout
        cmd = [
            CONFIG['llama_executable'],
            "-m", CONFIG['model_path'],
            "-p", full_prompt,
            "-n", str(CONFIG['max_tokens']),
            "--temp", "0.7",
            "--top-p", "0.9"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,  # 60 second timeout
            cwd=os.getcwd()
        )
        
        if result.returncode != 0:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            logger.error(f"llama.cpp execution failed: {error_msg}")
            return "I'm sorry, I'm having trouble processing your request right now. Please try again."
        
        # Extract response
        output = result.stdout
        if "Bot:" in output:
            response = output.split("Bot:")[-1].strip()
        else:
            response = output.strip()
        
        # Clean up response
        response = response.replace("\n\n", "\n").strip()
        
        if not response:
            return "I'm sorry, I didn't generate a proper response. Could you please rephrase your question?"
        
        logger.info("Query processed successfully")
        return response
        
    except subprocess.TimeoutExpired:
        logger.error("llama.cpp execution timed out")
        return "I'm taking too long to respond. Please try a shorter message."
    except Exception as e:
        logger.error(f"Error in query_llama: {e}")
        return "I encountered an error while processing your request. Please try again."

def create_interface():
    """Create and configure the Gradio interface."""
    
    def simple_chat(message):
        """Simple chat function that takes a message and returns a response."""
        if not message or not message.strip():
            return "Please enter a message."
        
        try:
            # For simplicity, we'll use empty history for now
            reply = query_llama(message, [])
            return reply
            
        except Exception as e:
            logger.error(f"Error in chat function: {e}")
            return "I'm sorry, something went wrong. Please try again."
    
    # Use the most basic Interface
    interface = gr.Interface(
        fn=simple_chat,
        inputs=gr.Textbox(
            label="Your message",
            placeholder="Type your message here...",
            lines=3
        ),
        outputs=gr.Textbox(
            label="Response",
            lines=5
        ),
        title="🌱 Mental Health Assistant",
        description="A compassionate, neurodivergent-friendly chatbot designed to provide support and guidance.\n\n**Please note:** This is not a replacement for professional mental health care. If you're experiencing a crisis, please contact emergency services or a crisis hotline.",
        examples=[
            "I'm feeling overwhelmed today",
            "Can you help me with anxiety?",
            "I need some grounding techniques"
        ],
        allow_flagging="never"
    )
    
    return interface

def main():
    """Main function to run the chatbot."""
    logger.info("Starting Mental Health Chatbot...")
    
    # Check dependencies
    issues = check_dependencies()
    if issues:
        logger.error("Dependency issues found:")
        for issue in issues:
            logger.error(f"  - {issue}")
        
        print("\n❌ Setup issues detected:")
        for issue in issues:
            print(f"  - {issue}")
        print("\nPlease run setup_bot.sh to install dependencies.")
        sys.exit(1)
    
    logger.info("All dependencies found")
    
    # Create and launch interface
    try:
        app = create_interface()
        logger.info("Launching Gradio interface...")
        
        # Try to find an available port starting from 7860
        import socket
        def find_free_port(start_port=7860):
            for port in range(start_port, start_port + 10):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.bind(('127.0.0.1', port))
                        return port
                except OSError:
                    continue
            return None
        
        port = find_free_port()
        if port is None:
            logger.error("Could not find an available port in range 7860-7869")
            print("❌ Could not find an available port. Please close other applications using ports 7860-7869.")
            sys.exit(1)
        
        logger.info(f"Launching on port {port}")
        app.launch(
            server_name="127.0.0.1",
            server_port=port,
            share=False,
            show_error=True
        )
    except Exception as e:
        logger.error(f"Failed to launch application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
