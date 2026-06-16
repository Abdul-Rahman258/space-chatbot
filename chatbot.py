import os
import gradio as gr
from groq import Groq

# Load your API key (replace with your actual key or use os.getenv for security)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))  # Or: os.getenv("GROQ_API_KEY")

# System prompt to define the domain and behavior
SYSTEM_PROMPT = """
You are a Space Exploration Expert chatbot. You only answer questions related to space exploration, astronomy, planets, stars, galaxies, space missions (e.g., NASA, SpaceX), black holes, asteroids, extraterrestrial life, or similar topics.
If the user's question is not related to space exploration, respond exactly with: "I'm sorry, I can't help with that. I'm specialized in space exploration topics only."
Do not answer out-of-domain questions under any circumstances. Keep responses informative, engaging, and under 300 words.
"""

def chat_with_bot(message, history):
    # Format the conversation history for the API
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})
    messages.append({"role": "user", "content": message})
    
    # Call the Groq API (using Llama 3.1 8B as an example model from Groq's offerings; it's fast and capable)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", # You can change to other free models like "mixtral-8x7b-32768"
        messages=messages,
        max_tokens=300,
        temperature=0.7  # Adjust for creativity; lower for factual responses
    )
    
    return response.choices[0].message.content

# Launch the Gradio interface
demo = gr.ChatInterface(
    fn=chat_with_bot,
    title="Space Exploration Expert Chatbot",
    description="Ask me anything about space! (e.g., 'What is the Artemis program?')",
    examples=["Tell me about black holes.", "How does SpaceX's Starship work?", "What's the nearest exoplanet?"]
)

demo.launch()