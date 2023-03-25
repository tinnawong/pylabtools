import os
from typing import List

def get_all_files(path_input: str, endswith: str = None) -> List[str]:
    """Get all files in your path input

    Args:
        path_input (str): path input
        endswith (str, optional): endswith file. Defaults to None. if None, return all file.

    Returns:
        List[str]: list of path file
    """
    if os.path.isfile(path_input):
        return [path_input]

    file_list = []
    for root, dirs, files in os.walk(path_input):
        for file in files:
            if endswith is None or file.endswith(endswith):
                file_list.append(os.path.join(root, file))

    return file_list

def get_current_folder_name(path_file: str)-> str:
    """Get current folder name

    Args:
        path_file (str): path file

    Returns:
        _type_: current folder name
    """
    if os.path.isfile(path_file):
        return os.path.basename(os.path.dirname(path_file))
    return os.path.basename((os.path.abspath(path_file)))

def get_previous_path(path_input: str, previous: int = 1) -> str:
    """
    Returns the path `previous` directories above `path_input`.

    Args:
        path_input (str): The starting path.
        previous (int, optional): The number of directories to go up. Defaults to 1.

    Returns:
        str: The resulting path.
    """
    if previous < 1:
        return os.path.abspath(path_input)
    
    path_input = os.path.abspath(path_input)
    for i in range(previous):
        path_input = os.path.dirname(path_input)
    return path_input

def get_all_directory(path_input)->str:
    """Get all directory in your path input

    Args:
        path_input (_type_): path input

    Returns:
        str: list of path is directory
    """
    path_input = os.path.abspath(path_input)
    return [os.path.join(path_input, name) for name in os.listdir(path_input)
            if os.path.isdir(os.path.join(path_input, name))]