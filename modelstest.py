import time
import ollama

# Define actions as functions
import pyautogui

def move_mouse_left():
    pyautogui.move(-100, 0)
    print("Moving mouse left.")

def move_mouse_right():
    pyautogui.move(100, 0)
    print("Moving mouse right.")

def move_mouse_up():
    pyautogui.move(0, -100)
    print("Moving mouse up.")

def move_mouse_down():
    pyautogui.move(0, 100)
    print("Moving mouse down.")

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
    pyautogui.click()  # Perform a mouse click
    print("Mouse double-clicked.")

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

def get_best_match_command(command, models):
    command_list = ', '.join(command_map.keys())
    messages = [
        {
            'role': 'system',
            'content': f'You are a bot that takes a string and finds the closest matching command from the list. The list of commands is: {command_list}. You should return only the exact name of the matched command without any additional words. Return None if no match is found. You do not ever respond you just give the exact name of the command as written in the list word for word.',
        },
        {
            "role": "user",
            "content": command,
        },
    ]

    responses = {}

    for model in models:
        start_time = time.time()
        response = ollama.chat(model=model, messages=messages)
        end_time = time.time()

        responses[model] = {
            "response": response['message']['content'],
            "time_taken": round(end_time - start_time, 2),
        }

    return responses

# Example usage
models_to_test = ["llama3.2", "gemma:2b"]  # Replace with actual model names you want to test
command = "click the mouse please"
results = get_best_match_command(command, models_to_test)

# Print the results
for model, result in results.items():
    print(f"Model: {model}")
    print(f"Response: {result['response']}")
    print(f"Time taken: {result['time_taken']} seconds")
    print("-")
