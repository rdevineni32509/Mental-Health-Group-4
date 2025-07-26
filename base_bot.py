from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import gradio as gr
import torch
 
# Load DialoGPT
chat_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
chat_tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
 
# Load sentiment analysis
sentiment_analyzer = pipeline("sentiment-analysis")
 
# Optional: Simple rule-based filtering
danger_keywords = ["kill myself", "suicide", "die", "end it all", "worthless", "i want to die"]
 

def safe_response(user_input, history):
    # 1. Keyword detection
    if any(phrase in user_input.lower() for phrase in danger_keywords):
        return "I'm really sorry you're feeling this way. You're not alone. Please consider talking to a professional or calling a helpline in your country. 💙", history
 
    # 2. Sentiment detection
    sentiment = sentiment_analyzer(user_input)[0]
    label = sentiment['label']
    score = sentiment['score']
 
    if label == "NEGATIVE" and score > 0.85:
        return "That sounds really tough. I'm here with you. Sometimes sharing a little more can help. 💬", history
 
    # 3. Fallback to DialoGPT
    new_input_ids = chat_tokenizer.encode(user_input + chat_tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([history, new_input_ids], dim=-1) if history is not None else new_input_ids
    history = chat_model.generate(bot_input_ids, max_length=1000, pad_token_id=chat_tokenizer.eos_token_id)
    response = chat_tokenizer.decode(history[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
 
    return response, history
 

with gr.Blocks() as demo:
    gr.Markdown("## 🧘 Mental Health Companion Bot\n_I'm here to listen. Let's talk._")
 
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Your message")
    model_state = gr.State(None)
    chat_state = gr.State([])
 
    def user_respond(message, chat_history, model_history):
        response, model_history = safe_response(message, model_history)
        chat_history.append((message, response))
        return chat_history, model_history
 
    msg.submit(user_respond, [msg, chat_state, model_state], [chatbot, model_state])
 
demo.launch()