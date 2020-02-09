import re

class IncludeParser:
    def __init__(self, headerfile):
        self._regexPattern = r"\s*#include\s*(<|\")(\w+.\w+)(>|\")"
        self._headerFileStr = headerfile
        self._headers = []
        self._parse_file()

    def get_headers(self):
        return self._headers
    
    def _parse_file(self):
        #matches = re.finditer(self._regexPattern, self._headerFileStr, re.MULTILINE)
        result = re.findall(self._regexPattern, self._headerFileStr) 
        for match in result:
            self._headers.append(match[1])



test_str = ("#include <stdio.h>\n\n"
	"//#include\n"
	"       #include\"hello.hpp\"")

obj = IncludeParser(test_str)
print obj.get_headers()
