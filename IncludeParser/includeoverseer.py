from filesearcher import FileSearcher
from includeparser import IncludeParser
from SystemModules.FileOpener.fileopener import FileOpener
from SystemModules.RepoPath.repopath import RepoPath
import re



class IncludeOverseer:
    def __init__(self, path_to_header_class_file):
        self._repo_path = RepoPath.get_repository_path()
        self._header_class_path = ''
        self._source_class_path = ''
        self._regex_header_pattern = r"^.*\.(h|hpp)$"
        self._includeparser_obj = IncludeParser()
        self._file_opener_obj = FileOpener()

        self._file_includes_list = []
        self._headers_to_stub_list = []

        if self._is_correct_header_file_type(path_to_header_class_file):
            self._header_class_path = path_to_header_class_file
            self._convert_header_to_source_file()

            code_str = self._file_opener_obj.read_all_from_file(self._header_class_path)
            self._includeparser_obj.parse_content(code_str)
            code_str = self._file_opener_obj.read_all_from_file(self._source_class_path)
            self._includeparser_obj.parse_content(code_str)

            self._file_includes_list = self._includeparser_obj.get_headers()



            print self._file_includes_list

            self._headers_to_stub_list.extend(self.find_inludes_path(self._file_includes_list,self._repo_path))
            print self._headers_to_stub_list

        else:
            print ("ERROR")
    
    def get_headers_for_stub(self):
        return self._headers_to_stub_list


    def _parse_file(self):
        pass


    def find_inludes_path(self, include_list, start_path):
        include_searcher = FileSearcher(start_path)
        include_searcher.find_file_path(include_list)
        list = include_searcher.get_found_file_list()
        return list


    def _convert_header_to_source_file(self):
        if self._header_class_path.rfind('.h'):
            self._source_class_path = self._header_class_path.replace(".h", ".c")
        elif self._header_class_path.rfind('.hpp'):
            self._source_class_path = self._header_class_path.replace(".hpp", ".cpp")
        else:
            pass
    
    def _is_correct_header_file_type(self, path_to_header_class_file):
        result = re.findall(self._regex_header_pattern, path_to_header_class_file)
        if result:
            return True
        return False
         




o = IncludeOverseer("c:\\R_PC\\My_Programs\\UT_Parser\\Parser\\IncludeParser\\test\\Project_Bagno\\Lugiks\\Engine\\Modules\\ModuleTest\\ModuleTest.hpp")
