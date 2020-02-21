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
        self._regex_header_pattern = r"([^\\]+)\.(h|hpp)$"      #r"^.*\.(h|hpp)$"
        self._includeparser_obj = IncludeParser()
        self._file_opener_obj = FileOpener()

        self._file_includes_list = []
        self._headers_to_stub_list = []

        self._root_class_include_paths = []

        if self._is_correct_header_file_type(path_to_header_class_file):
            self._header_class_path = path_to_header_class_file
            self._convert_header_to_source_file()
            self._pepare_root_includes_path()
            self._headers_to_stub_list.extend(self._find_file_inludes_path(self._file_includes_list,self._repo_path))

            self._root_class_include_paths = self._headers_to_stub_list
        else:
            print ("ERROR")
    
    def print_header_path_list(self):
        print "----------- HEADER LIST ----------- "
        for headerItem in self._headers_to_stub_list:
            print headerItem
        print "-------- END of HEADER LIST -------- "

    def get_headers_for_stub(self):
        return self._headers_to_stub_list

    def parse_all(self):
        print "Start Parsing..."
        for root_class_include in self._root_class_include_paths:
            list = self._get_includes_path_list_from_parsing_file(root_class_include)
            self._headers_to_stub_list.extend(list)
            self._parse_include_files_from_path_list(list)
        print "Parsing End"


    def _parse_include_files_from_path_list(self, header_file_list):
        if not header_file_list:
            return
        for header_file in header_file_list:
            list = self._get_includes_path_list_from_parsing_file(header_file)
            self._headers_to_stub_list.extend(list)
            self._parse_include_files_from_path_list(list)

    def _get_includes_path_list_from_parsing_file(self, header_file_path):
        code_str = self._file_opener_obj.read_all_from_file(header_file_path)
        include_list = self._parse_includes(code_str)
        include_file_path_list = self._find_file_inludes_path(include_list, self._repo_path)
        return include_file_path_list

    def _parse_includes(self, source_file_str):
        self._includeparser_obj.parse_content(source_file_str)
        return self._includeparser_obj.get_headers()


    def _pepare_root_includes_path(self):
        code_str = self._file_opener_obj.read_all_from_file(self._header_class_path)
        self._file_includes_list.extend(self._parse_includes(code_str))
        code_str = self._file_opener_obj.read_all_from_file(self._source_class_path)
        self._file_includes_list.extend(self._parse_includes(code_str))
        self._file_includes_list.remove(self._class_for_test_file_name)

    def _find_file_inludes_path(self, include_list, start_path):
        include_searcher = FileSearcher(start_path)
        include_searcher.find_file_path(include_list)
        return include_searcher.get_found_file_list()

    def _convert_header_to_source_file(self):
        if self._header_class_path.rfind('.h'):
            self._source_class_path = self._header_class_path.replace(".h", ".c")
        elif self._header_class_path.rfind('.hpp'):
            self._source_class_path = self._header_class_path.replace(".hpp", ".cpp")
        else:
            pass
    
    def _is_correct_header_file_type(self, path_to_header_class_file):
        result = re.findall(self._regex_header_pattern, path_to_header_class_file)
        self._class_for_test_file_name = ""
        if result:
            for match in result:
                self._class_for_test_file_name += match[0]
                self._class_for_test_file_name += "."
                self._class_for_test_file_name += match[1]
            return True
        return False
         




#o = IncludeOverseer("c:\\R_PC\\My_Programs\\UT_Parser\\Parser\\IncludeParser\\test\\Project_Bagno\\Lugiks\\Engine\\Modules\\ModuleTest\\ModuleTest.hpp")
#o.print_header_path_list()
#o.parse_all()
#o.print_header_path_list()
#print len(o.get_headers_for_stub())
