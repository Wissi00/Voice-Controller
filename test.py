import pyautogui
from openai import OpenAI
from ollama import generate


# Define actions as functions
import pyautogui

def move_mouse_left(pixels):
    pyautogui.move(-pixels, 0)
    print("Moving mouse left.")

def move_mouse_right(pixels):
    pyautogui.move(pixels, 0)
    print("Moving mouse right.")

def move_mouse_up(pixels):
    pyautogui.move(0, -pixels)
    print("Moving mouse up.")

def move_mouse_down(pixels):
    pyautogui.move(0, pixels)
    print("Moving mouse down.")

def click_spacebar():
    pyautogui.press('space')  # Press the space bar
    print("Space bar clicked.")

def stop_listening():
    print("Stopping the listening process.")
    global running
    running = False

# Mapping of commands to functions
def click_mouse():
    pyautogui.click()  # Perform a mouse click
    print("Mouse clicked.")

# Mapping of commands to functions
def double_click_mouse():
    pyautogui.click()  # Perform a mouse click
    pyautogui.click()  # Perform a mouse click
    print("Mouse clicked.")

# Mapping of commands to functions
command_map = {
    "move mouse left": move_mouse_left,
    "move mouse right": move_mouse_right,
    "move mouse up": move_mouse_up,
    "move mouse down": move_mouse_down,
    "click spacebar": click_spacebar,
    "click mouse": click_mouse, 
    "double click mouse": double_click_mouse,
    "stop listening": stop_listening,

}

def get_best_match_command(command):
    command_list = ', '.join(command_map.keys())

    prompt = f'I need you to take this command : {command}, and tell me the closest command from the list: {command_list}. Do not add any additional words, just return the exact name of the command as written in the list word for word. If there is no match, say None.'
    response = generate('llama3.2', prompt)
    print(f"AI response: {response['response']}")


get_best_match_command("click here please")  # Expected output: move mouse left