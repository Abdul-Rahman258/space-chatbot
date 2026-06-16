# 🌌 Space Chatbot

An interactive, AI-powered conversational agent that operates within a specific spatial or astronomical domain, complete with an audio-processing version.

## 🚀 Overview
This repository contains a Python-based chatbot built using the blazing-fast **Groq API**. It utilizes a tailored System Prompt to guide the Large Language Model's persona and knowledge base.

## 🌟 Features
- **Text-based Chat**: A lightweight terminal or script-based conversational AI (`chatbot.py`).
- **Audio Integration**: An experimental version of the chatbot that handles audio input/output (`Chatbot with audio/chatbot.py`).
- **Groq API**: Leveraging LPU inference engines for ultra-low latency responses.

## 🛠️ Built With
- Python 3.10
- Groq Cloud API
- Virtual Environments (`venv310`)

## 🔑 Setup
To run this project locally, you must provide your own API key:
1. Create a `.env` file in the root directory.
2. Add your Groq API key: `GROQ_API_KEY=gsk_your_key_here`
3. Install dependencies and run `python chatbot.py`.
