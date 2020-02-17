import unittest
from filesearcher import FileSearcher

ROOT_DIR_FOR_TEST = 'test\Project_Bagno'


class Test_FileSearcher(unittest.TestCase):

    def test_findIncludePath(self):
        includes_to_find = ['timer_sys.h', 'R_LogOut.hpp', 'ICSVFileReader.h']
        include_file_searcher_obj = FileSearcher(ROOT_DIR_FOR_TEST)
        include_file_searcher_obj.find_file_path(includes_to_find)
        include_path_found = include_file_searcher_obj.get_found_file_list()

        exp_include_found_paths = [
            "test\\Project_Bagno\\Lugiks\\EngineR_LogOut.hpp",
            "test\\Project_Bagno\\Lugiks\\Engine\\Modules\\ICSVFileReader\\ICSVFileReader.h",
            "test\\Project_Bagno\\Lugiks\Engine\\Modules\SystemIncludes\\timer_sys.h"]

        self.assertEqual(len(include_path_found), len(exp_include_found_paths))
        for includeFound in include_path_found:
            for includeFound in exp_include_found_paths:
                if includeFound in exp_include_found_paths:
                    exp_include_found_paths.remove(includeFound)
        self.assertEqual(len(exp_include_found_paths), 0)
