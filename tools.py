import pyautogui
import time

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

def click_spacebar():
    pyautogui.press('space')  # Press the space bar
    print("Space bar clicked.")

def stop_listening():
    print("Stopping the listening process.")
    global running
    running = False

def click_mouse():
    pyautogui.click()  # Perform a mouse click
    print("Mouse clicked.")

def double_click_mouse():
    pyautogui.click()  # Perform a mouse click
    time.sleep(0.1)
    pyautogui.click()  # Perform a mouse click
    print("Mouse double-clicked.")

def triple_click_mouse():
    pyautogui.click()  # Perform a mouse click
    pyautogui.click()  # Perform a mouse click
    pyautogui.click()  # Perform a mouse click
    print("Mouse triple-clicked.")

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

click_spacebar_tool = {
    'type': 'function',
    'function': {
        'name': 'click_spacebar',
        'description': 'Simulate a spacebar key press',
        'parameters': {
            'type': 'object',
            'required': [],
            'properties': {}
        },
    },
}

stop_listening_tool = {
    'type': 'function',
    'function': {
        'name': 'stop_listening',
        'description': 'Stop the listening process',
        'parameters': {
            'type': 'object',
            'required': [],
            'properties': {}
        },
    },
}

click_mouse_tool = {
    'type': 'function',
    'function': {
        'name': 'click_mouse',
        'description': 'Perform a mouse click',
        'parameters': {
            'type': 'object',
            'required': [],
            'properties': {}
        },
    },
}

double_click_mouse_tool = {
    'type': 'function',
    'function': {
        'name': 'double_click_mouse',
        'description': 'Perform a double-click on the mouse',
        'parameters': {
            'type': 'object',
            'required': [],
            'properties': {}
        },
    },
}

triple_click_mouse_tool = {
    'type': 'function',
    'function': {
        'name': 'triple_click_mouse',
        'description': 'Perform a triple-click on the mouse',
        'parameters': {
            'type': 'object',
            'required': [],
            'properties': {}
        },
    },
}

# Available Tools
tools = [
    move_mouse_left_tool,
    move_mouse_right_tool,
    move_mouse_up_tool,
    move_mouse_down_tool,
    click_spacebar_tool,
    stop_listening_tool,
    click_mouse_tool,
    double_click_mouse_tool,
    triple_click_mouse_tool,
]

# Available Functions Mapping
available_functions = {
    'move_mouse_left': move_mouse_left,
    'move_mouse_right': move_mouse_right,
    'move_mouse_up': move_mouse_up,
    'move_mouse_down': move_mouse_down,
    'click_spacebar': click_spacebar,
    'stop_listening': stop_listening,
    'click_mouse': click_mouse,
    'double_click_mouse': double_click_mouse,
    'triple_click_mouse': triple_click_mouse,
}