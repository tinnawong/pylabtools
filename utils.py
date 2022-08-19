import logging
import os
import re
import codecs
import json
import pathlib



def read_file_to_text(path: str):
    with codecs.open(path, "r", encoding='utf-8') as f:
        text = f.read()
    return text


def write_text(path_file="output.txt", content="", encoding="utf-8"):
    with codecs.open(path_file, "w", encoding=encoding) as f:
        f.write(content)


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


def normalize_text_transcription(text: str):
    """
    ตัดคำที่มีวงเล็ปออก
    """
    regex = r"\[\S+]|\([ก-ฮ][\S]+\)"
    pattern = re.findall(regex, text)
    print(pattern)
    text_clearn = re.sub(regex, "", text)
    return text_clearn


def normalize_transcription(path_input: str, path_output: str):
    list_path = get_all_files(path_input)
    text_removed_buffer = []
    for p in list_path:
        print(p)
        text = read_file_to_text(p)
        text_removed = normalize_text_transcription(text)
        text_removed_buffer.append(text_removed)
    total_text = "\n".join(text_removed_buffer)
    with codecs.open(os.path.join(path_output, "transcription.txt"), "w", encoding="utf-8")as f:
        f.write(total_text)


def read_file_config(path_config: str):
    with codecs.open(path_config, "r", encoding="utf-8") as f:
        config = f.read()
        preprocess_config = json.loads(config)
    return preprocess_config


def get_file_name(path_file: str, tail="", without_extension=False, set_extension=None):
    """
    สำหรับ
    extension 
    """
    if without_extension and set_extension:
        log_level(
            1, "parameter without_extension is true but set extension", logging.WARNING)
    if set_extension == None:
        set_extension = pathlib.Path(path_file).suffix
    if without_extension:
        return pathlib.Path(path_file).stem+"%s" % (tail)
    return pathlib.Path(path_file).stem+"%s%s" % (tail, set_extension)


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


def search_word_in_all_files(path_corpus: str, word: str):
    list_file = get_all_files(path_corpus)
    for p in list_file:
        text = read_file_to_text(p)
        if text.find(word) != -1:
            print(p)


def delete_all_files(path_dir: str, isConfirm=True):
    list_path = get_all_files(path_dir)
    for p in list_path:
        print("path file:", p)
    print("total files :",len(list_path))
    if isConfirm:
        ch = input("Do you want to delete all files? (y/n):")
        if ch == "y":
            for p in list_path:
                if os.path.exists(p):
                    os.remove(p)
                else:
                    print("The file does not exist :", p)
    else:
        for p in list_path:
            if os.path.exists(p):
                os.remove(p)
            else:
                print("The file does not exist :", p)


if __name__ == '__main__':
    # path_corpus = "transcription"
    # path_output = "./corpus/transcription/"
    # normalize_transcription(path_corpus,path_output)
    path_file = "D:/python/ngram_corrector/corpus/train and test/Corpus 5 Million/novel/novel_00107.ss.txt"
    log_level(1, "sdfkjsdkf")
    log_level(2, "sdfkjsdkf")
    print(get_file_name(path_file, tail="_sdfkit", without_extension=True))
