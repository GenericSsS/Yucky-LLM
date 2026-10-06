import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, directory))
        if os.path.commonpath([abs_path, target_path]) != abs_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'
        else:
            try:
                stuff_in_here = []
                for file in os.listdir(target_path):
                    filepath = os.path.normpath(os.path.join(target_path, file))
                    stuff_in_here.append(f"- {file}: file_size={os.path.getsize(filepath)} bytes, is_dir={os.path.isdir(filepath)}")
                return "\n".join(stuff_in_here)
            except Exception:
                return "Error: Could not read data"
    except Exception:
        return "Error: Your arguments are invalid"
