import base64
import typing
import concurrent.futures
import subprocess
from functools import partial
import time
import ast
import os

def encode_base64url(url: str) -> str:
    # Convert the string URL to bytes
    url_bytes = url.encode('utf-8')
    
    # Encode the bytes in base64
    base64_encoded = base64.urlsafe_b64encode(url_bytes)
    
    # Convert the encoded bytes back to string and return
    return base64_encoded.decode('utf-8')

def extract_submodels_id(data: typing.Dict) -> typing.List[str]:
    # Initialize a list to store the filtered values
    filtered_values: typing.List[str] = []
    
    # Iterate through the submodels
    for submodel in data.get("submodels", []):
        if submodel.get("type") == "ModelReference":
            value = submodel.get("keys", [{}])[0].get("value")
            if value:
                filtered_values.append(value)
    
    return filtered_values

def check_python_syntax(code: str) -> bool:
    """
    Checks if the given Python code has valid syntax.
    
    Parameters:
    - code (str): Python code as a string.
    
    Returns:
    - bool: True if the syntax is valid, False otherwise.
    """
    try:
        # Attempt to parse the code to an AST
        ast.parse(code)
        return True  # Syntax is valid
    except SyntaxError:
        return False  # Syntax is invalid
    
def check_bash_syntax(script: str) -> bool:
    """
    Checks if the given Bash script has valid syntax.
    
    Parameters:
    - script (str): Bash script as a string.
    
    Returns:
    - bool: True if the syntax is valid, False otherwise.
    """
    try:
        # Write the script to a temporary file
        with open('temp_script.sh', 'w') as f:
            f.write(script)
        
        # Check syntax without executing the script
        result = subprocess.run(['bash', '-n', 'temp_script.sh'], capture_output=True, text=True)
        
        # Remove the temporary file
        subprocess.run(['rm', 'temp_script.sh'])
        
        return result.returncode == 0  # Return True if return code is 0 (success)
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
def check_same_format(file1: str, file2: str) -> bool:
    """
    Checks if two files have the same format by comparing their extensions.

    Parameters:
    - file1 (str): The filename of the first file.
    - file2 (str): The filename of the second file.

    Returns:
    - bool: True if both files have the same format (extension), False otherwise.
    """
    # Extract the file extensions
    ext1 = os.path.splitext(file1)[1]
    ext2 = os.path.splitext(file2)[1]

    # Compare the file extensions
    return ext1.lower() == ext2.lower()

def overwrite_script(original_script_path: str, updated_script_content: str, new_script_path: typing.Optional[str] = None) -> typing.Tuple[typing.Dict[str, str], int]:
    """
    Overwrites a script with updated content or moves it to a new path.

    Parameters:
    - original_script_path (str): The path to the original script file.
    - updated_script_content (str): The new content to write to the script.
    - new_script_path (str, optional): The new path for the script. If provided, the updated script will be moved to this path.

    Returns:
    - Tuple[Dict[str, str], int]: A tuple containing a dictionary with a 'message' or 'error' key describing the result of the operation, and an integer indicating success (200) or failure (500).
    """
    if not check_same_format(original_script_path, new_script_path if new_script_path else original_script_path):
        return {"error": "The original and new script must have the same format (extension)."}, 500
    
    if original_script_path.endswith(".py"):
        if not check_python_syntax(updated_script_content):
            return {"error": "Invalid Python syntax in the updated script content."}, 500
    elif original_script_path.endswith(".sh"):
        if not check_bash_syntax(updated_script_content):
            return {"error": "Invalid Bash syntax in the updated script content."}, 500
        
    if not os.path.exists(original_script_path):
        return {"error": "Original script does not exist."}, 500
    
    target_script_path = new_script_path if new_script_path else original_script_path
    temporary_script_path = target_script_path + '.tmp'
    
    try:
        with open(temporary_script_path, 'w') as temp_file:
            temp_file.write(updated_script_content)
        
        os.replace(temporary_script_path, target_script_path)
        
        if new_script_path and new_script_path != original_script_path:
            os.remove(original_script_path)
        
        return {"message": "Script has been updated successfully."}, 200
        
    except Exception as e:
        try:
            if os.path.exists(temporary_script_path):
                os.remove(temporary_script_path)
        except Exception as e_rm:
            return {"error": f"Failed to remove temporary file after error: {e_rm}"}, 500
        
        return {"error": f"Error occurred while updating script: {e}"}, 500


def extract_file_parts(filename: str) -> typing.Tuple[bool, str, int]:
    """
    Extracts parts from a filename structured as 'active-state-file_name-intervall.py'
    and returns a tuple of (boolean, string, integer).

    Parameters:
    - filename (str): The filename to extract parts from.

    Returns:
    - tuple: A tuple containing a boolean, a string, and an integer.
    """
    # Remove the ".py" extension
    filename_without_extension = filename.rsplit('.', 1)[0]

    # Split the filename by hyphen
    parts = filename_without_extension.split('-')

    # Ensure there are exactly three parts after splitting
    if len(parts) != 3:
        raise ValueError("Filename does not conform to the expected format 'active-state-file_name-intervall'")

    # Extract the individual parts
    active_state, file_name, intervall_str = parts

    # Convert active_state to boolean
    active_state_bool = active_state.lower() == 'active'

    # Convert intervall to integer
    try:
        intervall_int = int(intervall_str)
    except ValueError:
        raise ValueError(f"Expected an integer value for intervall, got '{intervall_str}' instead.")

    # Return the extracted parts as a tuple
    return (active_state_bool, file_name, intervall_int)

def execute_files_in_folder(folder_path: str) -> None:
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # List all files in the folder
        files = os.listdir(folder_path)
        files.remove("__init__.py")
        execute_files(files, folder_path)
    
def execute_files(files: typing.List[str], folder_path: str) -> None:
    execute_function = partial(execute_single_file, folder_path=folder_path)
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        executor.map(execute_function, files)

def execute_single_file(file: str, folder_path: str) -> None:
    if file.endswith(".py"):
        active_state, file_name, intervall = extract_file_parts(file)
        if active_state:
            # if int(time.time()) % intervall == 0:
            #     subprocess.run(['python', f'{folder_path}/{file}'])
            subprocess.run(['python', f'{folder_path}/{file}'])
        
            # elif file.endswith(".sh"):
            #     subprocess.run(['bash', f'{folder_path}/{file}'])
    else:
        pass

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        result.check_returncode()  # Check if the command ran successfully
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

import asyncio
async def run_bash_script(script):
    process = await asyncio.create_subprocess_exec('bash', script, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        print(f"cannot execute {script}")
        return None

    return stdout.decode()