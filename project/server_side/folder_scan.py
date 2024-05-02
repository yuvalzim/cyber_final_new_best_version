from consts import *
from enable_py_privs import *
import os
import threading
import hash_api as hash_api


def list_files_sub(directory: str) -> list[str]:
    enable_privs()
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


def list_files(directory: str) -> list[str]:
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


def scan(files: list[str]) -> list[str]:
    enable_privs()
    with open(HASHES_FILE_NAME, 'r') as hashes_file:
        content = hashes_file.read().split('\n')
    content_set = set(content)
    corrupted_files = ""
    num_of_files = len(files)
    count = 0
    for i in files:
        if hash_api.calculate_hash(i) in content_set:
            corrupted_files += i + " "
        count += 1
        yield round((count / num_of_files) * 100)

    yield corrupted_files



