import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.schema_declarations import available_functions
from functions.call_function import *

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key = api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""



is_verbose_mode = False
if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    is_verbose_mode = True

def main():

    response = client.models.generate_content(model="gemini-2.0-flash-001",
                                           contents = messages,
                                             config = types.GenerateContentConfig(
                                                 tools=[available_functions],
                                                   system_instruction=system_prompt
                                                   )
                                                   )



    print("Hello from ai-agent!")
    if len(sys.argv) > 1 and len(sys.argv[1]) > 0:
        if response.function_calls:
            for func_call in response.function_calls:
                result= call_function(func_call, verbose = is_verbose_mode)
                try:
                    response_obj = result.parts[0].function_response.response
                except (IndexError, AttributeError):
                    raise Exception("Fatal: function call result missing expected response structure")
                if is_verbose_mode:
                    print(f"-> {response_obj}")
                else:
                    print(response_obj)

        else:
            print(response.text)

        if is_verbose_mode:
            print(f"User prompt: {sys.argv[1]}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


    else:
        print ("No prompt given")
        sys.exit(1)


if __name__ == "__main__":
    main()


