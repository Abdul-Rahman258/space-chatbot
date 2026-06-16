import os
import gradio as gr
from groq import Groq

# Load your API key (use .env for security as before)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))  # Or os.getenv("GROQ_API_KEY")

# System prompt (unchanged)
SYSTEM_PROMPT = """
You are a Space Exploration Expert chatbot. You only answer questions related to space exploration, astronomy, planets, stars, galaxies, space missions (e.g., NASA, SpaceX), black holes, asteroids, extraterrestrial life, or similar topics.
If the user's question is not related to space exploration, respond exactly with: "I'm sorry, I can't help with that. I'm specialized in space exploration topics only."
Do not answer out-of-domain questions under any circumstances. Keep responses informative, engaging, and under 300 words.
"""

def process_input(text_input, audio_input, history):
    # Step 1: Handle input (text or audio)
    if audio_input:  # If audio provided, transcribe it
        with open(audio_input, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-large-v3-turbo",  # Fast Whisper model
                file=audio_file,
                response_format="text"  # Get plain text output
            )
        user_message = transcription.text.strip()
    else:
        user_message = text_input.strip()
    
    if not user_message:
        return history, None  # No input, do nothing
    
    # Step 2: Build message history for LLM
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})
    messages.append({"role": "user", "content": user_message})
    
    # Step 3: Call LLM for response
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # Updated model
        messages=messages,
        max_tokens=300,
        temperature=0.7
    )
    bot_response = response.choices[0].message.content
    
    # Step 4: Generate TTS audio for the response
    audio_response = client.audio.speech.create(
        model="playai-tts",  # English TTS model
        voice="Fritz-PlayAI",  # Choose a voice (feel free to swap, e.g., "Celeste-PlayAI" for female)
        input=bot_response,
        response_format="wav"  # Output as WAV (Gradio supports it)
    )
    
    # Save audio to a temporary file for Gradio
    audio_path = "response.wav"
    with open(audio_path, "wb") as f:
        f.write(audio_response.content)  # Assuming .content has the binary data
    
    # Update history
    history.append((user_message, bot_response))
    
    return history, audio_path

# Build the Gradio interface with Blocks for audio support
with gr.Blocks(title="Space Exploration Expert Chatbot with Audio") as demo:
    gr.Markdown("Ask me anything about space! Use text or record audio. Responses include voice playback.")
    
    chatbot = gr.Chatbot(height=400)
    with gr.Row():
        text_input = gr.Textbox(label="Type your question", placeholder="E.g., What is a black hole?")
        audio_input = gr.Audio(source="microphone", type="filepath", label="Or record audio")
    submit_btn = gr.Button("Submit")
    
    audio_output = gr.Audio(label="Voice Response", autoplay=True, interactive=False)
    
    # On submit: Process input, update chatbot and audio
    submit_btn.click(
        process_input,
        inputs=[text_input, audio_input, chatbot],
        outputs=[chatbot, audio_output]
    )
    
    # Clear inputs after submit (optional)
    submit_btn.click(lambda: ("", None), outputs=[text_input, audio_input])
    
    gr.Examples(
        examples=["Tell me about black holes.", "How does SpaceX's Starship work?", "What's the nearest exoplanet?"],
        inputs=text_input
    )

demo.launch()