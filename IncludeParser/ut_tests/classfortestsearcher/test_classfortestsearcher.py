import unittest
from IncludeParser.classfortestsearcher import ClassForTestSearcher
from SystemModules.RepoPath.repopath import RepoPath


ROOT_DIR_FOR_TEST = RepoPath.get_repository_path()


class Test_ClassForTestSearcher(unittest.TestCase):

    def test_find_class_path(self):
        class_for_test_obj = ClassForTestSearcher("ModuleTest")
        classHeaderFoundPath = class_for_test_obj.get_class_header_file_localization()
        classSourceFoundPath = class_for_test_obj.get_class_source_file_localization()
        self.assertEqual(len(classHeaderFoundPath), 1)
        self.assertEqual(len(classSourceFoundPath), 1)

        self.assertEqual(classHeaderFoundPath[0], ROOT_DIR_FOR_TEST + "\\Lugiks\\Engine\\Modules\\ModuleTest\\ModuleTest.hpp")
        self.assertEqual(classSourceFoundPath[0], ROOT_DIR_FOR_TEST + "\\Lugiks\\Engine\\Modules\\ModuleTest\\ModuleTest.cpp")     
