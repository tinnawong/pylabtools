import codecs
import json
import pathlib
from typing import Generator, Union


def read_file_to_text(path: str, encoding: str = "utf-8", stream_line: bool = False) -> Union[str, Generator[str, None, None]]:
    """
    Reads the contents of a file and returns either the entire text or a generator of lines.

    Args:
        path (str): The path to the file.
        encoding (str, optional): The encoding of the file. Defaults to "utf-8".
        stream_line (bool, optional): If True, returns a generator of lines. Defaults to False.

    Returns:
        Union[str, Generator[str, None, None]]: Either the entire text or a generator of lines.
    """
    if stream_line:
        with open(path, "r", encoding=encoding) as f:
            for line in f:
                yield line.rstrip('\r\n')
    else:
        with open(path, "r", encoding=encoding) as f:
            text = f.read()
        return text


def write_text(path_file: str, content: str, encoding="utf-8"):
    """Write text to file

    Args:
        path_file (str): path to file output
        content (str): content to write
        encoding (str, optional): encoding of file. Defaults to "utf-8".
    """
    with codecs.open(path_file, "w", encoding=encoding) as f:
        f.write(content)


def read_file_config(path_config: str) -> dict:
    """Read file config format json
    Args:
        path_config (str): path to file config

    Returns:
        dict: config in dict
    """
    with codecs.open(path_config, "r", encoding="utf-8") as f:
        config = f.read()
        preprocess_config = json.loads(config)
    return preprocess_config


def get_file_name_without_extension(path_file: str) -> str:
    """Get file name without extension

    Args:
        path_file (str): path to file

    Returns:
        _type_: file name without extension
    """
    return pathlib.Path(path_file).stem


def get_file_name(path_file: str, tail: str = "", set_extension=None, without_extension=False) -> str:
    """ get file name with tail and extension

    Args:
        path_file (str): path to file
        tail (str, optional): tail of file name. Defaults empty.
        without_extension (bool, optional): if True, return file name without extension. Defaults to False.
        set_extension (str, optional): set extension of file name. Defaults to None.
    Returns:
        str: file name with tail and extension
    """
    if without_extension:
        return pathlib.Path(path_file).stem+"%s" % (tail)
    if set_extension == None:
        set_extension = pathlib.Path(path_file).suffix
    return pathlib.Path(path_file).stem+"%s%s" % (tail, set_extension)
