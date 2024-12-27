from tools import *
from groq import Groq
import os
import time
import ast
import json
from datetime import datetime


GROQ_API_KEY = os.getenv('GROQ_API_KEY')

models = [
    "llama3-groq-8b-8192-tool-use-preview",
    'llama3-groq-70b-8192-tool-use-preview',
    "llama-3.1-8b-instant",
]

prompts_to_test = [
    {
        "prompt" : "move the mouse up by 100 pixels",
        "expected function calls" : [move_mouse_up],
        "expected arguments" : [{"pixels": 100}],
        "tags" : ["mouse", "single"]
    },

    {
        "prompt" : "move the mouse down by 100 pixels and then right by 50 pixels and then click the mouse and write hello world",
        "expected function calls" : [move_mouse_down, move_mouse_right, click_mouse, write],
        "expected arguments" : [{"pixels": 100}, {"pixels": 50}, {}, {"text": "hello world"}],
        "tags" : ["mouse", "multiple", "keys"]
    },

    {
        "prompt" : "move the mouse left by 100 pixels and then up by 50 pixels",
        "expected function calls" : [move_mouse_left, move_mouse_up],
        "expected arguments" : [{"pixels": 100}, {"pixels": 50}],
        "tags" : ["mouse", "multiple"]
    },

    {
        "prompt" : "switch tabs wait one second and then left click then write hello world wait 1 more second and then switch tabs again",
        "expected function calls" : [cmd_tab, wait, click_mouse, write, wait, cmd_tab],
        "expected arguments" : [{}, {"seconds": 1}, {}, {"text": "hello world"}, {"seconds": 1}, {}],
        "tags" : ["mouse", "keys", "multiple"]
    },

    {
        "prompt" : "press enter",
        "expected function calls" : [press_enter],
        "expected arguments" : [{}],
        "tags" : ["keys", "single"]
    },

    {
        "prompt" : "left click and then right hello worlds",
        "expected function calls" : [click_mouse, write],
        "expected arguments" : [{}, {"text": "hello worlds"}],
        "tags" : ["mouse", "keys", "multiple", "wrong word"]
    },

    {
        "prompt" : "remove the mouse up by 100 pixels",
        "expected function calls" : [],
        "expected arguments" : [],
        "tags" : ["mouse", "single", "wrong word"]
    }

]

def get_groq_response(messages, model):
    client=Groq(api_key=GROQ_API_KEY)
    start_time = time.time()
    while True:
        try:
            # Attempt to send the request
            entire_response = client.chat.completions.create(
                model=model, # LLM to use
                messages=messages, # Conversation history
                stream=False,
                tools=tools, # Available tools (i.e. functions) for our LLM to use
                tool_choice="auto", # Let our LLM decide when to use tools
            )
            break  # Exit the loop if the request is successful

        except Exception as e:
            print(f"Error: {e}, retrying in 2 seconds...")
            time.sleep(2)  # Wait for 2 seconds before retrying

        # except Groq.InternalServerError as e:
        #     # If a 503 error occurs, print and retry after 2 seconds
        #     print("Error: Service unavailable. Retrying in 2 seconds...")
        #     time.sleep(2)  # Wait for 2 seconds before retrying
        # except Groq.BadRequestError as e:
        #     # If a 400 error occurs, print and break the loop
        #     print("Error: Bad request. retrying...")
            
    end_time = time.time()
    response = entire_response.choices[0]
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(f'Groq took: {elapsed_time:.2f} seconds to respond')
    return response, elapsed_time


def test_models(models, prompts_to_test):
    all_models_results = []
    for model in models:  # test each model
        print(f"Testing model: {model}")
        model_results = {
            "model": model,
            "correct": 0,
            "incorrect": 0,
            "accuracy": 0,
            "total": len(prompts_to_test),
            "reponse_times": [],
            "avg_response_time": 0,
            "tags": {}
        }
        for test in prompts_to_test:  # test each prompt
            messages=[{'role': 'system', 'content': 'You are a Large Language Model. You are given a transcript of a command and you have to determine the tools to use to execute the command or series of command. Take into account that since its a transcript the command may contain errors, so try to deduce what word the user meant to say from the context. For context the commands are all related to controlling a computer using the mouse and keyboard.'}]
            command = {'role': 'user', 'content': test["prompt"]}
            messages.append(command)
            response,response_time = get_groq_response(messages, model)
            model_results["reponse_times"].append(response_time)
            tools = response.message.tool_calls if response.message and response.message.tool_calls else []
            function_calls = []
            arguments = []
            for tool in tools:  # get the function calls and arguments
                function_calls.append(tool.function.name)
                arguments.append(ast.literal_eval(tool.function.arguments) if isinstance(tool.function.arguments, str) else tool.function.arguments)
            expected_function_calls = [func.__name__ for func in test["expected function calls"]]
            if function_calls == expected_function_calls and arguments == test["expected arguments"]:  # check if matches
                model_results["correct"] += 1  # increment the correct count
                for tag in test["tags"]:  # increment the correct count for each tag
                    if tag not in model_results:
                        model_results["tags"][tag] = {"correct": 0, "incorrect": 0, "total": 0}
                    model_results["tags"][tag]["correct"] += 1
                    model_results["tags"][tag]["total"] += 1
            else:
                model_results["incorrect"] += 1  # increment the incorrect count
                for tag in test["tags"]:  # increment the incorrect count for each tag
                    if tag not in model_results:
                        model_results["tags"][tag] = {"correct": 0, "incorrect": 0, "total": 0}
                    model_results["tags"][tag]["incorrect"] += 1
                    model_results["tags"][tag]["total"] += 1
        response_times = model_results["reponse_times"] #setups the response times
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        model_results["avg_response_time"] = avg_response_time # calculate the average response time
        model_results["accuracy"] = (model_results["correct"] / model_results["total"])*100 if model_results["total"] else 0 # calculate the accuracy
        all_models_results.append(model_results)
    return all_models_results

results = test_models(models, prompts_to_test)

try:
    with open("test_results.json", "r") as file:
        existing_data = json.load(file)  # Load existing data as a dictionary
except FileNotFoundError:
    existing_data = []  # Create an empty dictionary if file doesn't exist
except json.decoder.JSONDecodeError:
    existing_data = []

added_data = {
    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "notes" : "None",
    "results": results
}

notes = input("Enter notes (empty for no notes): ")
if notes:
    added_data["notes"] = notes


existing_data.append(added_data)  # Append the new data to the existing data


with open("test_results.json", "w") as file:
    json.dump(existing_data, file, indent=4)  # Save the dictionary to the file

def summarize_results(data):
    summary = {}
    for entry in data:
        for result in entry["results"]:
            model = result["model"]
            if model not in summary:
                summary[model] = {
                    "total_accuracy": 0,
                    "total_response_time": 0,
                    "entries_count": 0
                }
            summary[model]["total_accuracy"] += result["accuracy"]
            summary[model]["total_response_time"] += result["avg_response_time"]
            summary[model]["entries_count"] += 1
    
    overview = []
    for model, values in summary.items():
        overview.append({
            "LLM": model,
            "accuracy": values["total_accuracy"] / values["entries_count"],
            "avg_response_time": values["total_response_time"] / values["entries_count"]
        })
    return overview

overview_results = summarize_results(existing_data)

with open("test_results_overview.json", "w") as file:
    json.dump(overview_results, file, indent=4)  # Save the dictionary to the file

