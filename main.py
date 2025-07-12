import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.schema_declarations import available_functions
from functions.call_function import *
from config import MAX_ITERS
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key = api_key)

def generate_content_turn(client, messages, verbose_mode, system_prompt, available_functions):

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    # Si estamos en modo verbose, imprime los detalles de tokens
    if verbose_mode:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)


    if not response.function_calls:
        return response.text


    function_responses = []
    for function_call_part in response.function_calls:
        print(f" - Calling function: {function_call_part.name}")

        result = call_function(function_call_part, verbose=verbose_mode)

        if(not result.parts
            or not result.parts[0].function_response
        ):
            raise Exception("Empty or malformed function call result from tool.")

        function_responses.append(result.parts[0])

        if verbose_mode:

            print(f"-> {result.parts[0].function_response.response}")

    if function_responses:
        messages.append(types.Content(role="tool", parts=function_responses))

    return None


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt_parts = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    verbose_mode = "--verbose" in sys.argv[1:]

    if not user_prompt_parts:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)
    user_prompt = " ".join(user_prompt_parts)

    print("Hello from ai-agent!")
    if verbose_mode:
        print(f"User prompt: {user_prompt}\n")


    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]


    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached without a final response.")
            sys.exit(1)

        try:

            final_response_text = generate_content_turn(
                client, messages, verbose_mode, system_prompt, available_functions
            )

            if final_response_text:
                print("Final response:")
                print(final_response_text)
                break

        except Exception as e:
            print(f"Error during agent turn: {e}")
            sys.exit(1) #



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unhandled error occurred: {e}")
        sys.exit(1)