import speech_recognition as sr
import pyautogui
from openai import OpenAI

API_KEY = "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"
API_ENDPOINT = "https://api.groq.com/openai/v1"

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
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key="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",  # Fetch the API key from environment variables
    )
    command_list = ', '.join(command_map.keys())

    messages = [
        {"role": "system", "content": f'''You are an assistant that takes a string and finds the closest matching command from the list. The list of commands is: {command_list}. You should return only the exact name of the matched command without any additional words. Return None if no match is found.'''},  # Initial instruction for the AI system
    ]
    messages.append({"role": "user", "content": command})  # Append user's input to the messages list
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Use the model defined in environment variables
        messages=messages,  # Pass the conversation history (including system and user messages)
        stream=False,  # Disable streaming, wait for the full response
        max_tokens=5
    )
    ai_response = response.choices[0].message.content  # Get the AI's reply from the response object
    return ai_response

def listen_and_execute():
    print("Listening for commands...")
    global running
    running = True

    recognizer = sr.Recognizer()  # Ensure recognizer is inside the function to avoid scoping issues

    while running:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            print("Listening for command...")
            audio = recognizer.listen(source)

        try:
            # Recognizing the command
            command = recognizer.recognize_google(audio).lower()
            print(f"Command: {command}")

            # Get the best matching command using Groq API
            best_match = get_best_match_command(command)
            if best_match:
                print(f"Best match: {best_match}")
                # Execute the corresponding function if a match is found
                if best_match in command_map:
                    command_map[best_match]()  # Call the corresponding function
                else:
                    print("Best match command not recognized.")
            else:
                print("Error in finding the best match.")

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
        except sr.RequestError as e:
            print(f"Error with the Speech Recognition service: {e}")
        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == "__main__":
    listen_and_execute()