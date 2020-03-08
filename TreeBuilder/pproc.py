class PreProcess:
    def __init__(self, source):
        self._source = source
        self._single_line_comment = False
        self._multi_line_comment = False
        self.source_after_processing = []
    
    def pre_process(self):
        '''
        
        Removes all chars from // to '\n' 
        
        Removes all chars from /* to */
  
        '''

        for index, char in enumerate(self._source):

            if len(self._source) - 1 > index and char == '/': 
                if self._source[index + 1] == '/':
                    self._single_line_comment = True
                if self._source[index + 1] == '*':
                    self._multi_line_comment = True

            if char == '\n':
                self._single_line_comment = False
            
            if not self._single_line_comment and not self._multi_line_comment:
                self.source_after_processing.append(char)

            if len(self._source) - 1 > index and char == '/': 
                if self._source[index - 1] == '*':
                    self._multi_line_comment = False

        return self.source_after_processing
