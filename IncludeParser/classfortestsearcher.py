from filesearcher import FileSearcher
from SystemModules.RepoPath.repopath import RepoPath

class ClassForTestSearcher:
    def __init__(self, class_name_str):
        if class_name_str:
            self._class_header_file_to_search = []
            self._class_source_file_to_search = []
            self._class_header_found = []
            self._class_source_found = []

            #self._class_header_file_to_search.append(class_name_str + ".h")
            self._class_header_file_to_search.append(class_name_str + ".hpp")
            self._class_source_file_to_search.append(class_name_str + ".cpp")
            self._determine_header_file_localization()
            self._determine_source_file_localization()
        else:
            #Error
            pass

    def _determine_header_file_localization(self):
        file_searcher_obj = FileSearcher(RepoPath.get_repository_path())
        file_searcher_obj.find_file_path(self._class_header_file_to_search)
        self._class_header_found = file_searcher_obj.get_found_file_list()

    def _determine_source_file_localization(self):
        file_searcher_obj = FileSearcher(RepoPath.get_repository_path())
        file_searcher_obj.find_file_path(self._class_source_file_to_search)
        self._class_source_found = file_searcher_obj.get_found_file_list()

    def get_class_header_file_localization(self):
        return self._class_header_found

    def get_class_source_file_localization(self):
        return self._class_source_found




