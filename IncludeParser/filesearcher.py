import os


class FileSearcher:
    def __init__(self, start_path):
        self._root_dir = start_path
        self._found_file_list = []

    def find_file_path(self, to_find_list):
        self._found_file_list = []
        for dirName, subdirList, fileList in os.walk(self._root_dir):
            for fileName in fileList:
                if fileName in to_find_list:
                    strPath = dirName + "\\" + fileName
                    self._found_file_list.append(strPath)

    def get_found_file_list(self):
        return self._found_file_list









# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# ROOT_DIR = ROOT_DIR + '\\test\\Project_Bagno'
# print ROOT_DIR
# includes_to_find = ['timer_sys.h', 'R_LogOut.hpp', 'ICSVFileReader.h']
# include_file_searcher_obj = FileSearcher('C:\\R_PC\\My_Programs\\UT_Parser\\Parser\\IncludeParser\\test\\Project_Bagno')
# include_file_searcher_obj.find_file_path(includes_to_find)
# print include_file_searcher_obj.get_found_file_list()
