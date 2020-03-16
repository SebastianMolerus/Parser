from IncludeParser.includeoverseer import IncludeOverseer
from SystemModules.FileChecker.filechecker import is_file_exists
from SystemModules.FileChecker.filechecker import is_dir_exists
from SystemModules.FileChecker.filechecker import is_correct_path_to_header_file
from SystemModules.FileChecker.filechecker import is_correct_path_to_source_file

class ParseDriver:
    def __init__(self, project_path, path_to_header_file, path_to_source_file = None):
        if not is_dir_exists(project_path):
            raise Exception("Project Path does not exist.")
        
        if not is_file_exists(path_to_header_file) and not is_correct_path_to_header_file(path_to_header_file):
            raise Exception("Header file/type does not exist.")

        if path_to_source_file:
            if not is_file_exists(path_to_source_file) and not is_correct_path_to_source_file(path_to_source_file):
                raise Exception("Source file/type does not exist.")
        
        self._project_repo_path = project_path
        self._path_to_header_file = path_to_header_file
        self._path_to_source_file = path_to_source_file
    
    def _parse_headers(self):
        include_overseer_obj = IncludeOverseer(self._project_repo_path, self._path_to_header_file, self._path_to_source_file)
        include_overseer_obj.parse_all()
        return include_overseer_obj.get_parsed_headers_for_stub()