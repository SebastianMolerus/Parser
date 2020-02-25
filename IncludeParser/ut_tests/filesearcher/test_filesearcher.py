import unittest
from IncludeParser.filesearcher import FileSearcher
from SystemModules.RepoPath.repopath import RepoPath


ROOT_DIR_FOR_TEST = RepoPath.get_repository_path()


class Test_FileSearcher(unittest.TestCase):

    def test_find_path_for_current_include(self):
        includes_to_find = ['timer_sys.h', 'R_LogOut.hpp', 'ICSVFileReader.h']
        include_file_searcher_obj = FileSearcher(ROOT_DIR_FOR_TEST)
        include_file_searcher_obj.find_file_path(includes_to_find)
        include_path_found = include_file_searcher_obj.get_found_file_list()

        exp_include_found_paths = [
            ROOT_DIR_FOR_TEST + "\\Lugiks\\EngineR_LogOut.hpp",
            ROOT_DIR_FOR_TEST + "\\Lugiks\\Engine\\Modules\\ICSVFileReader\\ICSVFileReader.h",
            ROOT_DIR_FOR_TEST + "\\Lugiks\Engine\\Modules\SystemIncludes\\timer_sys.h"]

        self.assertEqual(len(include_path_found), len(exp_include_found_paths))
        for includeFound in include_path_found:
            for includeFound in exp_include_found_paths:
                if includeFound in exp_include_found_paths:
                    exp_include_found_paths.remove(includeFound)
        self.assertEqual(len(exp_include_found_paths), 0)
