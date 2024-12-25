from tools import *
from groq import Groq
import os
import time
import ast
import json

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

models = [
    "llama3-groq-8b-8192-tool-use-preview",
    'llama3-groq-70b-8192-tool-use-preview',
    "llama-3.1-70b-versatile",
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

    entire_response = client.chat.completions.create(
        model=model, # LLM to use
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

def test_models(models, prompts_to_test):
    all_results = []
    for model in models:  # test each model
        print(f"Testing model: {model}")
        model_results = {
            "model": model,
            "correct": 0,
            "incorrect": 0,
            "total": len(prompts_to_test)
        }
        for test in prompts_to_test:  # test each prompt
            messages = [{'role': 'user', 'content': test["prompt"]}]
            response = get_groq_response(messages, model)
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
                        model_results[tag] = {"correct": 0, "incorrect": 0, "total": 0}
                    model_results[tag]["correct"] += 1
                    model_results[tag]["total"] += 1
            else:
                model_results["incorrect"] += 1  # increment the incorrect count
                for tag in test["tags"]:  # increment the incorrect count for each tag
                    if tag not in model_results:
                        model_results[tag] = {"correct": 0, "incorrect": 0, "total": 0}
                    model_results[tag]["incorrect"] += 1
                    model_results[tag]["total"] += 1
        all_results.append(model_results)

    return all_results


results = test_models(models, prompts_to_test)
with open("modelsTestSave.json", "w") as file:
    json.dump(results, file, indent=4) 
