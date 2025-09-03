import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_file_dir = os.path.dirname(abs_file_path)
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.exists(abs_file_path) and not os.path.isfile(abs_file_path):
        return f'Error: File is not a regular file: "{file_path}"'
    try:
        if not os.path.exists(abs_file_dir):
            os.path.makedirs(abs_file_dir)
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writing file "{file_path}": {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=f"Write content to a specified file, constrained to the working directory. Existing files will be overwritten. Missng folders will be created if needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file for which the contents should be written to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that should be written to the file.",
            ),
        },
    ),
)