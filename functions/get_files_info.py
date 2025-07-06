import os

def get_files_info(working_directory, directory=None):
  files_list = []
  full_path = os.path.join(working_directory, directory)
  full_path_abs = os.path.abspath(full_path)
  work_dir_abs_path = os.path.abspath(working_directory)
  try:
    if not full_path_abs.startswith(work_dir_abs_path):
      return f'Error: Cannot list "{full_path}" as it is outside the permitted working directory'
    if os.path.isdir(full_path_abs) == False:
      return f'Error: "{directory}" is not a directory'


    else:
      for file in os.listdir(full_path_abs):
        file_path = os.path.join(full_path_abs,file)
        string = f"- {file}: file_size={os.path.getsize(file_path)}, is_dir={os.path.isdir(file_path)}"
        files_list.append(string)
    list_of_strings = "\n".join(files_list)


  except ValueError as e:
    return f"Error {e}"
  except Exception as e:
    return f"Error {e}"
  except TypeError as e:
    return f"Error {e}"

  return list_of_strings