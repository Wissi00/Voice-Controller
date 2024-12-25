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

def write(text):
    pyautogui.write(text)
    print(f"Writing '{text}'.")

def cmd_tab():
    pyautogui.keyDown('command')
    time.sleep(0.1)  # Add a small delay to simulate natural pressing
    pyautogui.press('tab')  # Press the 'tab' key
    pyautogui.keyUp('command')  # Release the 'command' key
    print("Switching applications.")

def wait(seconds):
    time.sleep(int(seconds))
    print(f"Waiting for {seconds} seconds.")

def press_enter():
    pyautogui.press('enter')
    print("Enter key pressed.")

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

write_tool = {
    'type': 'function',
    'function': {
        'name': 'write',
        'description': 'Write a given text',
        'parameters': {
            'type': 'object',
            'required': ['text'],
            'properties': {
                'text': {'type': 'string', 'description': 'The text to write'}
            },
        },
    },
}

cmd_tab_tool = {
    'type': 'function',
    'function': {
        'name': 'cmd_tab',
        'description': 'Presses Command and then Tab to Switch tabs or applications, it is commonly referred to as Alt-Tab. This command is called usually when the user says "Switch tabs"',
        'parameters': {
            'type': 'object',
            'required': [],
            'properties': {}
        },
    },
}

wait_tool = {
    'type': 'function',
    'function': {
        'name': 'wait',
        'description': 'Wait for a given number of seconds',
        'parameters': {
            'type': 'object',
            'required': ['seconds'],
            'properties': {
                'seconds': {'type': 'integer', 'description': 'The number of seconds to wait'}
            },
        },
    },
}

press_enter_tool = {
    'type': 'function',
    'function': {
        'name': 'press_enter',
        'description': 'Press the Enter key',
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
    write_tool,
    cmd_tab_tool,
    wait_tool,
    press_enter_tool,
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
    'write': write,
    'cmd_tab': cmd_tab,
    'wait': wait,
    'press_enter': press_enter,
}