import os
import shutil
import subprocess
import sys

def copy_files_to_program_files(source_dir, file_names):
    """
    Copies all files from the source directory to the Program Files directory.

    Args:
    source_dir (str): The directory where the files are located.
    file_names (list): List of filenames to copy.

    Returns:
    str: The installation path where files were copied.
    """
    processor_architecture = os.environ.get('PROCESSOR_ARCHITECTURE')
    if processor_architecture == 'AMD64':
        install_path = os.path.join(os.environ['ProgramFiles'], 'MyAppName')
    else:
        install_path = os.path.join(os.environ['ProgramFiles(x86)'], 'MyAppName')
    
    try:
        os.makedirs(install_path, exist_ok=True)
        for file_name in file_names:
            shutil.copy(os.path.join(source_dir, file_name), install_path)
        print(f"All files have been copied to {install_path}")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except Exception as e:
        print(f"Failed to copy files: {e}")

    return install_path

def add_to_startup(install_path, script_name):
    """
    Adds a script to Windows Task Scheduler to run at startup.

    Args:
    install_path (str): The directory where the script is installed.
    script_name (str): The name of the script to schedule.

    Returns:
    None
    """
    python_executable = sys.executable
    task_name = f"{script_name}Startup"
    task_command = f'"{python_executable}" "{os.path.join(install_path, script_name)}"'
    full_command = [
        'schtasks', '/create', '/tn', task_name, '/tr', task_command, '/sc', 'onlogon', '/rl', 'highest', '/f'
    ]
    try:
        subprocess.run(full_command, check=True)
        print(f"Task {task_name} has been created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create scheduled task: {e}")

# Usage example
source_directory = "./"
files_to_copy = ["filter.py", "main.py", "get_logs.py","log_filtering.py"]
install_directory = copy_files_to_program_files(source_directory, files_to_copy)
add_to_startup(install_directory, "script1.py")  # Choose which file to add to startup
path=copy_files_to_program_files(source_directory,files_to_copy)
add_to_startup(path,"get_logs.py")