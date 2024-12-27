# Voice Controller

A voice-controlled system that allows you to execute commands on your computer using voice recognition. It leverages OpenAI tools, Groq, and speech recognition for seamless interaction.

## Features

- Detect and respond to wake words (`"hey controller"`, `"hello controller"`, etc.).
- Recognize and process voice commands using Google Speech Recognition.
- Execute system commands like opening applications or controlling the mouse.
- Integrate with AI models (Ollama and Groq) for intelligent command handling and tool usage.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Wissi00/Voice-Controller.git
   cd voice-controller
   pip install -r requirements.txt
   export GROQ_API_KEY=your_api_key_here
   python main.py
   ```
