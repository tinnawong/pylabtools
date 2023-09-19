import os
from typing import List

def get_all_files(path_input: str, endswith: str = None, recursive: bool = True) -> List[str]:
    """
    Get all files from the specified path.

    Args:
    - path_input (str): Path to start the search from.
    - endswith (str, optional): File extension filter. If None, returns all files.
    - recursive (bool, optional): If True, search for files recursively. Defaults to True.

    Returns:
    - List[str]: List of file paths.
    """
    if os.path.isfile(path_input):
        return [path_input]

    if recursive:
        files = [
            os.path.join(root, file)
            for root, _, files in os.walk(path_input)
            for file in files
            if endswith is None or file.endswith(endswith)
        ]
    else:
        files = [
            os.path.join(path_input, file)
            for file in os.listdir(path_input)
            if os.path.isfile(os.path.join(path_input, file)) and (endswith is None or file.endswith(endswith))
        ]

    return files

def get_current_folder_name(path: str) -> str:
    """
    Get the name of the folder containing the specified path.

    Args:
    - path (str): Path to a file or folder.

    Returns:
    - str: Name of the containing folder.
    """
    return os.path.basename(os.path.dirname(os.path.abspath(path)))

def get_previous_path(path_input: str, previous: int = 1) -> str:
    """
    Returns the path `previous` directories above `path_input`.

    Args:
    - path_input (str): The starting path.
    - previous (int, optional): The number of directories to go up. Defaults to 1.

    Returns:
    - str: The resulting path.
    """
    path = os.path.abspath(path_input)
    for _ in range(previous):
        path = os.path.dirname(path)
    return path

def get_all_directories(path_input: str) -> List[str]:
    """
    Get all directories from the specified path.

    Args:
    - path_input (str): Path to start the search from.

    Returns:
    - List[str]: List of directory paths.
    """
    path_input = os.path.abspath(path_input)
    return [
        os.path.join(path_input, name)
        for name in os.listdir(path_input)
        if os.path.isdir(os.path.join(path_input, name))
    ]
