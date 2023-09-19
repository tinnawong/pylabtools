import json
from pathlib import Path
from typing import Generator

def read_file_all_text(path: str, encoding: str = "utf-8") -> str:
    """
    Reads the entire content of a file and returns it as a single string.

    Args:
        path (str): The path to the file.
        encoding (str, optional): The encoding of the file. Defaults to "utf-8".

    Returns:
        str: The entire content of the file.
    """
    with open(path, "r", encoding=encoding) as f:
        return f.read()

def stream_file_by_line(path: str, encoding: str = "utf-8") -> Generator[str, None, None]:
    """
    Streams the content of a file line by line.

    Args:
        path (str): The path to the file.
        encoding (str, optional): The encoding of the file. Defaults to "utf-8".

    Yields:
        Generator[str, None, None]: Each line from the file.
    """
    with open(path, "r", encoding=encoding) as f:
        for line in f:
            yield line.rstrip('\r\n')


def write_text_to_file(path: str, content: str, encoding: str = "utf-8") -> None:
    """Write text to file

    Args:
        path (str): Path to the output file.
        content (str): Content to write.
        encoding (str, optional): Encoding of the file. Defaults to "utf-8".
    """
    with open(path, "w", encoding=encoding) as f:
        f.write(content)


def read_json_config(path: str) -> dict:
    """Read JSON config file

    Args:
        path (str): Path to the config file.

    Returns:
        dict: Configuration as a dictionary.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_file_name_without_extension(path: str) -> str:
    """Get file name without extension

    Args:
        path (str): Path to the file.

    Returns:
        str: File name without extension.
    """
    return Path(path).stem


def get_file_name(path: str, tail: str = "", set_extension: str = None, without_extension: bool = False) -> str:
    """Get file name with optional modifications

    Args:
        path (str): Path to the file.
        tail (str, optional): Additional tail for the file name. Defaults to "".
        set_extension (str, optional): Desired file extension. If None, uses original extension. Defaults to None.
        without_extension (bool, optional): If True, returns file name without extension. Defaults to False.

    Returns:
        str: Modified file name.
    """
    file_name = Path(path).stem
    if without_extension:
        return file_name + tail
    if not set_extension:
        set_extension = Path(path).suffix
    return file_name + tail + set_extension
