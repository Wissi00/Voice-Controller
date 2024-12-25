import pyautogui
from groq import Groq
import time
import os

GROQ_API_KEY =os.environ.get("GROQ_API_KEY")

# Function Definitions
def move_mouse_left(pixels):
    pyautogui.move(-int(pixels), 0)
    print(f"Moving mouse left by {pixels} pixels.")

def move_mouse_right(pixels):
    pyautogui.move(int(pixels), 0)
    print(f"Moving mouse right by {pixels} pixels.")

def move_mouse_up(pixels):
    pyautogui.move(0, -int(pixels))
    print(f"Moving mouse up by {pixels} pixels.")

def move_mouse_down(pixels):
    pyautogui.move(0, int(pixels))
    print(f"Moving mouse down by {pixels} pixels.")

# Define Tools for Each Mouse Movement Function
move_mouse_left_tool = {
    'type': 'function',
    'function': {
        'name': 'move_mouse_left',
        'description': 'Move the mouse left by a given number of pixels',
        'parameters': {
            'type': 'object',
            'required': ['pixels'],
            'properties': {
                'pixels': {'type': 'integer', 'description': 'The number of pixels to move the mouse left'}
            },
        },
    },
}

move_mouse_right_tool = {
    'type': 'function',
    'function': {
        'name': 'move_mouse_right',
        'description': 'Move the mouse right by a given number of pixels',
        'parameters': {
            'type': 'object',
            'required': ['pixels'],
            'properties': {
                'pixels': {'type': 'integer', 'description': 'The number of pixels to move the mouse right'}
            },
        },
    },
}

move_mouse_up_tool = {
    'type': 'function',
    'function': {
        'name': 'move_mouse_up',
        'description': 'Move the mouse up by a given number of pixels',
        'parameters': {
            'type': 'object',
            'required': ['pixels'],
            'properties': {
                'pixels': {'type': 'integer', 'description': 'The number of pixels to move the mouse up'}
            },
        },
    },
}

move_mouse_down_tool = {
    'type': 'function',
    'function': {
        'name': 'move_mouse_down',
        'description': 'Move the mouse down by a given number of pixels',
        'parameters': {
            'type': 'object',
            'required': ['pixels'],
            'properties': {
                'pixels': {'type': 'integer', 'description': 'The number of pixels to move the mouse down'}
            },
        },
    },
}

# Available Tools
tools = [
    move_mouse_left_tool,
    move_mouse_right_tool,
    move_mouse_up_tool,
    move_mouse_down_tool
]

# Available Functions Mapping
available_functions = {
    'move_mouse_left': move_mouse_left,
    'move_mouse_right': move_mouse_right,
    'move_mouse_up': move_mouse_up,
    'move_mouse_down': move_mouse_down,
}

# Example User Message: "move the mouse left by 100 pixels and then up by 50 pixels"
messages = [{'role': 'user', 'content': 'move the mouse up 123 pixels and then left 456 pixels'}]
print('Prompt:', messages[0]['content'])
start_time = time.time()
# Call to the Chat API with the tools
client = Groq(api_key=GROQ_API_KEY)
MODEL = 'llama3-groq-70b-8192-tool-use-preview'

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
print(f"tool calls: {response.message.tool_calls}")
# Calculate the elapsed time
elapsed_time = end_time - start_time
print(f'Elapsed Time: {elapsed_time:.2f} seconds')
# Check if there are any tool calls in the response and process them
if response.message.tool_calls:
    for tool in response.message.tool_calls:
        if function_to_call := available_functions.get(tool.function.name):
            print(f'Calling function: {tool.function.name}')
            print(f'Arguments: {tool.function.arguments}')            
            # Call the function with the correct argument type
            function_to_call(**tool.function.arguments)
        else:
            print(f'Function {tool.function.name} not found')
