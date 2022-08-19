import os

def get_all_files(path_input: str, endswith=".txt"):
    """
    อ่านทุกๆไฟล์ที่อยู่ใน path ที่กำหนด(อ่านเข้าไปในโฟลเดอร์ย่อยด้วย)
    """
    if os.path.isfile(path_input):
        return [path_input]
    buffer_files = []
    for root, dirs, files in os.walk(path_input):
        for file in files:
            if file.endswith(endswith):
                buffer_files.append(os.path.join(root, file))
    return buffer_files


def get_current_folder_name(path_file: str):
    if os.path.isfile(path_file):
        return os.path.basename(os.path.dirname(path_file))
    return os.path.basename((os.path.abspath(path_file)))


def get_previous_path(dir: str, previous=1):
    if previous < 1:
        return dir
    dir = os.path.abspath(dir)
    for i in range(previous):
        state_dir = dir
        dir = os.path.dirname(dir)
        if state_dir == dir:
            break
    return dir

def get_all_directory(path_input):
    """
    get all directory in your path input
    return list of path is directory
    """
    path_input = os.path.abspath(path_input)
    return [os.path.join(path_input, name) for name in os.listdir(path_input)
            if os.path.isdir(os.path.join(path_input, name))]