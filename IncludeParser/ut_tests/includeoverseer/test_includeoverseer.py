import unittest
from IncludeParser.includeoverseer import IncludeOverseer
from SystemModules.RepoPath.repopath import RepoPath


ROOT_DIR_FOR_TEST = RepoPath.get_repository_path()


class Test_IncludeOverseer(unittest.TestCase):

    def test_all_header_path_from_file(self):
        o = IncludeOverseer(ROOT_DIR_FOR_TEST + "\\Lugiks\\Engine\\Modules\\ModuleTest\\ModuleTest.hpp")
        exp_include_found_paths = [
            ROOT_DIR_FOR_TEST + "\\Lugiks\\Defs.hpp",
            ROOT_DIR_FOR_TEST + "\\Lugiks\\Engine\\R_LogOut.hpp",
            ROOT_DIR_FOR_TEST + "\\Lugiks\\Engine\\Modules\\CSV_Reader\\csv_reader.h",
            ROOT_DIR_FOR_TEST + "\\Lugiks\\Engine\\Modules\\SystemIncludes\\timer_sys1.hpp",
            ROOT_DIR_FOR_TEST + "\\Lugiks\\Engine\\Modules\\ICSVFileReader\\ICSVFileReader.h"]
        
        o.parse_all()
        include_path_found = o.get_headers_for_stub()

        self.assertEqual(len(include_path_found), len(exp_include_found_paths))
        for includeFound in include_path_found:
            for includeFound in exp_include_found_paths:
                if includeFound in exp_include_found_paths:
                    exp_include_found_paths.remove(includeFound)
        self.assertEqual(len(exp_include_found_paths), 0)



