import codecs
import json
import pathlib

def read_file_to_text(path: str,encoding = "utf-8"):
    with codecs.open(path, "r", encoding= encoding) as f:
        text = f.read()
    return text

def write_text(path_file="output.txt", content="", encoding="utf-8"):
    with codecs.open(path_file, "w", encoding=encoding) as f:
        f.write(content)

def read_file_config(path_config: str):
    """
    return dict of config 
    """
    with codecs.open(path_config, "r", encoding="utf-8") as f:
        config = f.read()
        preprocess_config = json.loads(config)
    return preprocess_config

def get_file_name_without_extension(path_file: str):
    return pathlib.Path(path_file).stem

def get_file_name(path_file: str, tail="", without_extension=False, set_extension=None):
    """
    for rename filename from path or filename
    """
    if set_extension == None:
        set_extension = pathlib.Path(path_file).suffix
    if without_extension:
        return pathlib.Path(path_file).stem+"%s" % (tail)
    return pathlib.Path(path_file).stem+"%s%s" % (tail, set_extension)

