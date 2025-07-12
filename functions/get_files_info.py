import os




def get_files_info(working_directory, directory=None):
  files_list = []
  if directory is None:
      target_path = working_directory
  else:
      target_path = os.path.join(working_directory, directory)

  full_path_abs = os.path.abspath(target_path)
  work_dir_abs_path = os.path.abspath(working_directory)

  if not full_path_abs.startswith(work_dir_abs_path):
      return f'Error: Cannot list "{target_path}" as it is outside the permitted working directory'


  try:
    if os.path.isdir(full_path_abs) == False:
      return f'Error: "{target_path}" is not a directory or does not exist.'
    else:
      for file in os.listdir(full_path_abs):
        file_path = os.path.join(full_path_abs, file)

        try:
            file_size = os.path.getsize(file_path)
        except OSError:
            file_size = "N/A"

        string = f"- {file}: file_size={file_size}, is_dir={os.path.isdir(file_path)}"
        files_list.append(string)


      list_of_strings = "\n".join(files_list)

      if not list_of_strings and os.path.isdir(full_path_abs):
          return f"Directory '{target_path}' is empty."

      return list_of_strings

  except ValueError as e:
    return f"Error processing path: {e}"
  except FileNotFoundError:
      return f"Error: Directory not found: {target_path}"
  except PermissionError:
      return f"Error: Permission denied to access directory: {target_path}"
  except Exception as e:
    return f"An unexpected error occurred while listing files: {e}"






