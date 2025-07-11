# THese are the schema declarations for the functions so that the ai can call them
from google.genai import types



schema_get_file_content = types.FunctionDeclaration(
  name="get_file_content",
  description="Gets the content of the file constrained in the working directory as a string, if it is more than 10000 characters it truncates it.",
  parameters=types.Schema(
      type=types.Type.OBJECT,
                      properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to get the content, relative to the working directory. If not provided it returns an error.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
  name="run_python_file",
  description="Runs the python file given, with a timeout of 30 seconds, and returning the outputs of the file.",
  parameters=types.Schema(
      type=types.Type.OBJECT,
                      properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file to run.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
  name="write_file",
  description="Writes the file passed with the specificied content, if the file exists it overwrites ir, if the file doesnt exist it creates the directory and the file",
  parameters=types.Schema(
      type=types.Type.OBJECT,
                      properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to be writen, if it doesnt exists in the directory it creates the directory and the file.",
            ),
            "content": types.Schema(
              type=types.Type.STRING,
              description="The content to write the file.",
            )
        },
    ),
)

schema_get_files_info = types.FunctionDeclaration(
  name="get_files_info",
  description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
  parameters=types.Schema(
      type=types.Type.OBJECT,
                      properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)



available_functions = types.Tool(
  function_declarations=[
    schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
  ]
)