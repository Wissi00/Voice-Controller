import speech_recognition as sr
from tools import *
from ollama import chat, ChatResponse
import time
import os
from groq import Groq
import ast  

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def is_app_running(app_name):
    try:
        # Check for the process in the system's running processes
        result = os.popen(f"pgrep -x {app_name}").read()
        return bool(result.strip())  # If `pgrep` finds a process, result is not empty
    except Exception as e:
        print(f"Error checking if {app_name} is running: {e}")
        return False

def open_app(app_name):
    try:
        os.system(f"open /Applications/{app_name}.app")
        print(f"{app_name} opened successfully.")
    except Exception as e:
        print(f"Failed to open {app_name}: {e}")

def get_ollama_response(messages):
    try:
        start_time = time.time()
        response: ChatResponse = chat(
            'llama3.1:8b',  # The model to use (you can change it as needed)
            messages=messages,  # User message list
            tools=tools,  # Tools for the chatbot to use
        )
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'Ollama took: {elapsed_time:.2f} seconds to respond')
    except ConnectionError as e:
        print(f"Error connecting to Ollama: {e}")
    return response

def get_groq_response(messages):
    client=Groq(api_key=GROQ_API_KEY)
    MODEL = 'llama3-groq-70b-8192-tool-use-preview'
    start_time = time.time()

    entire_response = client.chat.completions.create(
        model=MODEL, # LLM to use
        messages=messages, # Conversation history
        stream=False,
        tools=tools, # Available tools (i.e. functions) for our LLM to use
        tool_choice="auto", # Let our LLM decide when to use tools
        max_tokens=4096 # Maximum number of tokens to allow in our response
    )
    end_time = time.time()
    response = entire_response.choices[0]
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(f'Groq took: {elapsed_time:.2f} seconds to respond')
    return response

def get_tools(command):
    # Example User Message: "move the mouse left by 100 pixels and then up by 50 pixels"
    messages = [{'role': 'user', 'content': command}]
    print('Prompt:', messages[0]['content'])
    response = get_groq_response(messages)
        
    return response

def execute_tools(response):
    for tool in response.message.tool_calls:
        if function_to_call := available_functions.get(tool.function.name):
            if isinstance(tool.function.arguments, str): # Convert the arguments to a dictionary if it's a string
                tool.function.arguments = ast.literal_eval(tool.function.arguments)
            print(f'Calling function: {tool.function.name}{tool.function.arguments}')
            # Call the function with the correct argument type
            function_to_call(**tool.function.arguments)
        else:
            print(f'Function {tool.function.name} not found')
        time.sleep(0.1)  # Sleep for .1 second between tool calls 

  
recognizer = sr.Recognizer()  # Ensure recognizer is inside the function to avoid scoping issues
WAKE_WORDS = ["hey controller", "hello controller", "controller"]
while True:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for command...")
        audio = recognizer.listen(source)

    try:
        # Recognizing the command
        command = recognizer.recognize_google(audio).lower()
        print(f"Command: {command}")
        detected_wake_word = next((word for word in WAKE_WORDS if word in command), None)
        if detected_wake_word:
            print(f"Detected wake word: {detected_wake_word}")
            command = command.replace(detected_wake_word, "").strip()
            start_time = time.time()
            response = get_tools(command)
            end_time = time.time()
            get_tools_Time = end_time - start_time
            if response.message.tool_calls: # Check if there are any tool calls in the response and process them
                execute_tools(response)
            else:
                print("No tools to execute.")
    except sr.UnknownValueError:
        print("Could not understand the audio.")
    