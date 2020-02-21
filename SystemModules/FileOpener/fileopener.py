class FileOpener:
    def __init__(self):
        pass
        
    def read_all_from_file(self, file_path):
        self._file_handler = open(file_path, 'r')
        str_content = ''
        file_content =  self._file_handler.readlines()
        for line in file_content:
            str_content += line
        self._file_handler.close()
        return str_content


