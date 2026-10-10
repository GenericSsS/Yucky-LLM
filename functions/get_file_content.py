import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Finds a file in a specified directory relative to the working directory, providing file content up to 10,000 characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File to list content from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, file_path))
        if os.path.commonpath([abs_path, target_path]) != abs_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(target_path, "r") as f:
                content = f.read(10000)
                if f.read(1):
                    content += f'[...File "{file_path}" truncated at 10000 characters]'
            return content
    except Exception:
        return "Error: Your arguments are invalid"
