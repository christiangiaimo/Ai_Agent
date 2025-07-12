from functions.get_files_info import get_files_info
from functions.get_files_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from google.genai import types

def call_function(function_call_part, verbose=False):

  function_map = {"get_file_content": get_file_content,
                  "get_files_info": get_files_info,
                  "run_python_file": run_python_file,
                  "write_file": write_file}


  func = function_map.get(function_call_part.name)

  args = dict(function_call_part.args)
  args["working_directory"] = "./calculator"


  if func is None:
    return types.Content(
    role="tool",
    parts=[
      types.Part.from_function_response(
            name=function_call_part.name,
            response={"error": f"Unknown function: {function_call_part.name}"},
        )
    ],
)
  result = func(**args)
  processed_result = str(result) if result is not None else ""
  if verbose:
    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
  else:
    print(f" - Calling function: {function_call_part.name}")

  return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": processed_result},
        )
    ],
)


