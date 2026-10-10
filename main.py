import json
import os
import argparse
from venv import create
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("Well shit... where's the key?")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )
    message = response.choices[0].message
    if response.usage == None:
        raise RuntimeError("There's no usage data!")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    if len(message.tool_calls) != 0:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            if len(result_message["content"]) == 0:
                raise Exception("where's the output?")
            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
