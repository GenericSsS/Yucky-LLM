import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, file_path))
        if os.path.commonpath([abs_path, target_path]) != abs_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python", target_path]
            command.extend(args) if args is not None else None
            run_command: subprocess.CompletedProcess = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False, cwd=working_directory)
            result_list = []
            result_list.append(f"Process exited with code {run_command.returncode}") if run_command.returncode != 0 else None
            if run_command.stdout == "":
                if run_command.stderr != "":
                    result_list.append(f"STDERR:{run_command.stderr}")
                else:
                    result_list.append("No output produced")
            else:
                result_list.append(f"STDOUT:{run_command.stdout}")
                if run_command.stderr != "":
                    result_list.append(f"STDERR:{run_command.stderr}")
            return "\n".join(result_list)
    except Exception as e:
        return f"Error: executing Python file: {e}"
