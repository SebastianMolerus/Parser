import re

class IncludeParser:
    def __init__(self):
        self._headers = []
        self._system_headers = []
        self._regex_include_pattern = r"\s*#include\s*(<|\")(.+)(>|\")"#r"\s*#include\s*(<|\")(\w+.\w+)(>|\")"

    def get_headers(self):
        return self._headers

    def get_system_headers(self):
        return self._system_headers

    def parse_content(self, contentToParse):
        self._system_headers = []
        self._headers = []
        # matches = re.finditer(self._regexPattern, self._contentToParse, re.MULTILINE)
        result = re.findall(self._regex_include_pattern, contentToParse)
        for match in result:
            if (match[0] == '"' and match[2] == '"'):
                header = self._filter_long_header_path_to_one_header(match[1])
                self._headers.append(header)
            elif (match[0] == '<' and match[2] == '>'):
                #header = self._filter_long_header_path_to_one_header(match[1])
                self._system_headers.append(match[1])
            else:
                pass

    def _filter_long_header_path_to_one_header(self, header):
        header = header.replace("/","\\")
        regex_header_file_pattern = r"([^\\]+)\.(h|hpp)$"
        result = re.findall(regex_header_file_pattern, header)
        parsed_header = ""
        if result:
            for match in result:
                parsed_header += match[0]
                parsed_header += "."
                parsed_header += match[1]
        return parsed_header
