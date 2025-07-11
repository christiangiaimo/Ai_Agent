# This functions runs the python file if not raises some errors, it puts a timeout of 30 seconds so the program doesnt run indefinetly
import os
import subprocess
import sys

def run_python_file(working_directory, file_path):
  full_path = os.path.join(working_directory, file_path)
  full_path_abs = os.path.abspath(full_path)
  work_dir_abs_path = os.path.abspath(working_directory)
  try:
    if not full_path_abs.startswith(work_dir_abs_path):
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(full_path_abs) == False:
      return f'Error: File "{file_path}" not found.'
    if file_path.endswith('.py') == False:
      return f'Error: "{file_path}" is not a Python file.'
    else:
      result = subprocess.run([sys.executable, full_path_abs],
                              cwd=work_dir_abs_path,
                              timeout = 30,
                                capture_output=True,
                                  text=True
                                  )
      if result.stdout == "" and result.stderr == "":
        return f"No output produced"

      elif result.returncode != 0:
        return f"STDOUT: {result.stdout} STDERR: {result.stderr} Process exited with code {result.returncode}"
      elif result.returncode == 0:
        return f"STDOUT: {result.stdout} STDERR: {result.stderr}"


  except ValueError as e:
    return f"Error: executing Python file: {e}"
  except Exception as e:
    return f"Error: executing Python file: {e}"
  except TypeError as e:
    return f"Error: executing Python file: {e}"