import os


class FileSearcher:
    def __init__(self, start_path):
        self._root_dir = start_path
        self._found_file_list = []

    def find_file_path(self, to_find_list):
        for dirName, subdirList, fileList in os.walk(self._root_dir):
            for fileName in fileList:
                if fileName in to_find_list:
                    strPath = dirName + "\\" + fileName
                    self._found_file_list.append(strPath)

    def get_found_file_list(self):
        return self._found_file_list
