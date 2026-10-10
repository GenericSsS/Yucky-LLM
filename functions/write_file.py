import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Overwrites a python file in a specified directory relative to the working directory. If no such file exists, it is created and written.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File to overwrite or write, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file specified with file_path."
                }
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, file_path))
        if os.path.commonpath([abs_path, target_path]) != abs_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        else:
            try:
                if  len(os.path.dirname(file_path)) != 0:
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(target_path, "w") as f:
                    f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            except Exception:
                return "Error: Could not write content"
    except Exception:
        return "Error: Your arguments are invalid"
