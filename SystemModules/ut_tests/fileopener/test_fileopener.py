import unittest
from SystemModules.FileOpener.fileopener import FileOpener
from SystemModules.RepoPath.repopath import RepoPath


ROOT_DIR_FOR_TEST = RepoPath.get_repository_path()


class Test_FileOpener(unittest.TestCase):

    def test_open_file_that_not_exists(self):
        test_obj = FileOpener()
        code_str = test_obj.read_all_from_file(ROOT_DIR_FOR_TEST + "\\XXXXYYYYYZZZZZ\\XXXXXXXXXXXXXX.hpp")
        self.assertEqual(code_str,"")
