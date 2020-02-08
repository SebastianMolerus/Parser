class Preproc:
    
    def __init__(self, source):
        self._source = source
        self._single_line_comment = False
        self._multiline_comment = False
    
    def Preprocess(self):
        self._source_after_processing = []

        for index, char in enumerate(self._source):

            if len(self._source) - 1 > index and char == '/': 
                if self._source[index + 1] == '/':
                    self._single_line_comment = True
                if self._source[index + 1] == '*':
                    self._multiline_comment = True


            if char == '\n':
                self._single_line_comment = False
            
            if not self._single_line_comment and not self._multiline_comment:
                self._source_after_processing.append(char)

            if len(self._source) - 1 > index and char == '/': 
                if self._source[index - 1] == '*':
                    self._multiline_comment = False

        return self._source_after_processing
            

            
