import re

class IncludeParser:
    def __init__(self, fileToParse = None, textToParse = None):

        self._headers = []
        self._systemHeaders = []
        self._regexPattern = r"\s*#include\s*(<|\")(\w+.\w+)(>|\")"

        if fileToParse and textToParse:
            raise Exception("Defined two resources of data.")
        
        if textToParse:
            self._parse_content(textToParse)
        else:
            #Open FIle
            self._parse_content(' ')
            pass


    def get_headers(self):
        return self._headers
    
    def get_system_headers(self):
        return self._systemHeaders
    
    def _parse_content(self, contentToParse):
        #matches = re.finditer(self._regexPattern, self._contentToParse, re.MULTILINE)
        result = re.findall(self._regexPattern, contentToParse) 
        for match in result:
            if (match[0] == '"' and match[2] == '"'):
                self._headers.append(match[1])
            elif (match[0] == '<' and match[2] == '>'):
                self._systemHeaders.append(match[1])
            else:
                pass

