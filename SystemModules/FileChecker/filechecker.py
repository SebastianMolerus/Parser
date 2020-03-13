import re
import os.path

def is_file_exists(file_path):
    if not os.path.isfile(file_path):
        return False
    return True

def is_correct_path_to_header_file(path_to_header_file):
    regex_header_pattern = r"([^\\]+)\.(h|hpp)$"      #r"^.*\.(h|hpp)$"
    result = re.findall(regex_header_pattern, path_to_header_file)
    if result:
        return True
    return False

def is_correct_path_to_source_file(path_to_source_file):
    regex_header_pattern = r"([^\\]+)\.(c|cpp)$"
    result = re.findall(regex_header_pattern, path_to_source_file)
    if result:
        return True
    return False

