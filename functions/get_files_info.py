import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, directory))
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'
        if os.path.commonpath([abs_path, target_path]) != abs_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        else:
            return f'Success: "{directory}" is within the working directory'
    except Exception:
        return "Your arguments are invalid"
