import unittest
from includefilesearcher import IncludeFileSearcher

ROOT_DIR_FOR_TEST = 'test\Project_Bagno'

class Test_IncludeFileSearcher(unittest.TestCase):

    def test_findIncludePath(self):
        includesToFind = ['timer_sys.h', 'R_LogOut.hpp', 'ICSVFileReader.h']
        includeFileSearcherObj = IncludeFileSearcher(includesToFind, ROOT_DIR_FOR_TEST)
        includeFileSearcherObj.find_include_path()
        includePathFound = includeFileSearcherObj.get_include_found_list()

        expIncludeFoundPaths = [
            "test\\Project_Bagno\\Lugiks\\EngineR_LogOut.hpp",
            "test\\Project_Bagno\\Lugiks\\Engine\\Modules\\ICSVFileReader\\ICSVFileReader.h",
            "test\\Project_Bagno\\Lugiks\Engine\\Modules\SystemIncludes\\timer_sys.h"]

        self.assertEqual(len(includePathFound), len(expIncludeFoundPaths))
        for includeFound in includePathFound:
            for includeFound in expIncludeFoundPaths:
                if includeFound in expIncludeFoundPaths:
                    expIncludeFoundPaths.remove(includeFound)
        self.assertEqual(len(expIncludeFoundPaths), 0)
