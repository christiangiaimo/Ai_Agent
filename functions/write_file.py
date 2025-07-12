
import os
from config import MAX_CHARS
#This function enables the ai to write in the file#
# If the file or the directory doesnt exists it creates it and overwrites it

def write_file(working_directory, file_path, content):
  full_path = os.path.join(working_directory, file_path)
  full_path_abs = os.path.abspath(full_path)
  work_dir_abs_path = os.path.abspath(working_directory)
  try:
    if not full_path_abs.startswith(work_dir_abs_path):
      return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    os.makedirs(os.path.dirname(full_path_abs), exist_ok = True)
    with open(full_path_abs, "w") as f:
      f.write(content)
      return(f'Succesfully wrote to "{file_path}" ({len(content)} characters written)')

  except ValueError as e:
    return f"Error {e}"
  except Exception as e:
    return f"Error {e}"
  except TypeError as e:
    return f"Error {e}"
  except IOError as e:
    return f"Error {e}"

