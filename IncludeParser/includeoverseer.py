import re
from filesearcher import FileSearcher
from includeparser import IncludeParser
from SystemModules.FileOpener.fileopener import read_all_from_file

class IncludeOverseer:
    def __init__(self, project_path, path_to_header_file, path_to_source_file = None):
        self._project_path = project_path
        self._root_header_file_path = path_to_header_file
        self._root_source_file_path = path_to_source_file
        self._include_parser_obj = IncludeParser()

        self._root_include_list = []
        self._parsed_headers_to_stub_list = []

        self._pepare_root_includes_path()
        self._parsed_headers_to_stub_list.extend(self._find_file_includes_path(self._root_include_list, self._project_path))

    def debug_print_parsed_header_path_list(self):
        print "----------- HEADER LIST ----------- "
        for headerItem in self._parsed_headers_to_stub_list:
            print headerItem
        print "-------- END of HEADER LIST -------- "

    def get_parsed_headers_for_stub(self):
        return self._parsed_headers_to_stub_list

    def parse_all(self):
        if not self._parsed_headers_to_stub_list:
            return
        root_iteration_include_list = []
        root_iteration_include_list = self._parsed_headers_to_stub_list[:]

        #print "Start Parsing..."
        for root_include_id in root_iteration_include_list:
            temp_file_path_include_list = self._get_include_path_list_from_parsing_file(root_include_id)
            self._parsed_headers_to_stub_list.extend(temp_file_path_include_list)
            self._parse_include_files_from_path_list(temp_file_path_include_list)
        
        self._remove_header_duplicates()
        #print "Parsing End"

    def _parse_include_files_from_path_list(self, header_file_list):
        if not header_file_list:
            return
        for header_file in header_file_list:
            temp_include_path_list = self._get_include_path_list_from_parsing_file(header_file)
            self._parsed_headers_to_stub_list.extend(temp_include_path_list)
            self._parse_include_files_from_path_list(temp_include_path_list)

    def _get_include_path_list_from_parsing_file(self, header_file_path):
        code_str = read_all_from_file(header_file_path)
        include_list = self._parse_includes(code_str)
        include_file_path_list = self._find_file_includes_path(include_list, self._project_path)
        return include_file_path_list

    def _parse_includes(self, source_file_str):
        self._include_parser_obj.parse_content(source_file_str)
        return self._include_parser_obj.get_headers()

    def _pepare_root_includes_path(self):
        if self._root_header_file_path:
            header_code_str = read_all_from_file(self._root_header_file_path)
            if not header_code_str:
                return
            self._root_include_list.extend(self._parse_includes(header_code_str))

        if self._root_source_file_path:
            source_code_str = read_all_from_file(self._root_source_file_path)
            if not source_code_str:
                return
            self._root_include_list.extend(self._parse_includes(source_code_str))
            self._root_include_list.remove(self._get_header_file_name_from_path(self._root_header_file_path))

    def _find_file_includes_path(self, include_list, start_path):
        include_searcher = FileSearcher(start_path)
        include_searcher.find_file_path(include_list)
        return include_searcher.get_found_file_list()
    
    def _remove_header_duplicates(self):
        copy_header_list = []
        for item in self._parsed_headers_to_stub_list:
            if item not in copy_header_list:
                copy_header_list.append(item)
        del self._parsed_headers_to_stub_list[:]
        self._parsed_headers_to_stub_list = copy_header_list[:]
    
    def _get_header_file_name_from_path(self, path_to_header_file):
        regex_header_pattern = r"([^\\]+)\.(h|hpp)$"
        found_header_file_name = re.findall(regex_header_pattern, path_to_header_file)
        header_file_name = ""
        if found_header_file_name:
            for match in found_header_file_name:
                header_file_name += match[0]
                header_file_name += "."
                header_file_name += match[1]
        return header_file_name

