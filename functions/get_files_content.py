
import os
from config import MAX_CHARS
#This functios return the contents of the file to search.

def get_file_content(working_directory, file_path):

  full_path = os.path.join(working_directory, file_path)
  full_path_abs = os.path.abspath(full_path)
  work_dir_abs_path = os.path.abspath(working_directory)
  try:
    if not full_path_abs.startswith(work_dir_abs_path):
      return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(full_path_abs) == False:
      return f'Error: File not found or it is not a regular file: "{file_path}" '


    else:
      with open(full_path_abs, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if f.read(1):
          return f'{file_content_string}[... File "{file_path}" truncated at 10000 characters] '
        return file_content_string

  except ValueError as e:
    return f"Error {e}"
  except Exception as e:
    return f"Error {e}"
  except TypeError as e:
    return f"Error {e}"





