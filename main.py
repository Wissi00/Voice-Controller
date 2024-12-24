import speech_recognition as sr
from tools import *
from ollama import chat, ChatResponse
import time

def get_tools(command):
    # Example User Message: "move the mouse left by 100 pixels and then up by 50 pixels"
    messages = [{'role': 'user', 'content': command}]
    print('Prompt:', messages[0]['content'])
    # Call to the Chat API with the tools
    response: ChatResponse = chat(
        'llama3.1:8b',  # The model to use (you can change it as needed)
        messages=messages,  # User message list
        tools=tools,  # Tools for the chatbot to use
    )
    return response

def execute_tools(response):
    for tool in response.message.tool_calls:
        if function_to_call := available_functions.get(tool.function.name):
            print(f'Calling function: {tool.function.name}')
            print(f'Arguments: {tool.function.arguments}')            
            # Call the function with the correct argument type
            function_to_call(**tool.function.arguments)
        else:
            print(f'Function {tool.function.name} not found')

  
recognizer = sr.Recognizer()  # Ensure recognizer is inside the function to avoid scoping issues

while True:
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for command...")
        audio = recognizer.listen(source)

    try:
        # Recognizing the command
        command = recognizer.recognize_google(audio).lower()
        start_time = time.time()
        response = get_tools(command)
        end_time = time.time()
        get_tools_Time = end_time - start_time
        print(f'LLM took: {get_tools_Time:.2f} seconds to respond')
        if response.message.tool_calls: # Check if there are any tool calls in the response and process them
            execute_tools(response)
    except sr.UnknownValueError:
        print("Could not understand the audio.")
    