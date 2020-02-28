import os.path

class FileOpener:
    def __init__(self):
        pass
        
    def read_all_from_file(self, file_path):
        str_content = ''
        if not os.path.isfile(file_path):
            return str_content
        file_handler = open(file_path, 'r')
        file_content =  file_handler.readlines()
        for line in file_content:
            str_content += line
        file_handler.close()
        return str_content


