import unittest
import os
from IncludeParser.filesearcher import FileSearcher
from IncludeParser.ut_tests.create_enviroment_for_test import PROJECT_PATH
from IncludeParser.ut_tests.create_enviroment_for_test import HPP_FILE_LIST_INC
from IncludeParser.ut_tests.create_enviroment_for_test import EnvTestClass


ROOT_DIR_FOR_TEST = os.path.dirname(os.path.abspath(__file__))

class Test_FileSearcher(unittest.TestCase):

    def test_find_path_for_current_include(self):
        test_env_obj = EnvTestClass(ROOT_DIR_FOR_TEST)
        test_env_obj.create_env_for_test()

        include_file_searcher_obj = FileSearcher(ROOT_DIR_FOR_TEST + PROJECT_PATH)
        include_file_searcher_obj.find_file_path(HPP_FILE_LIST_INC)
        include_path_found_list = include_file_searcher_obj.get_found_file_list()

        for include_found_item in include_path_found_list:
            status = test_env_obj.is_file_include_path_exists(include_found_item)
            self.assertEqual(status, True)

        test_env_obj.remove_all()
    
    def test_no_includes_to_find(self):
        test_env_obj = EnvTestClass(ROOT_DIR_FOR_TEST)
        test_env_obj.create_env_for_test()

        includes_to_find = []
        include_file_searcher_obj = FileSearcher(ROOT_DIR_FOR_TEST + PROJECT_PATH)
        include_file_searcher_obj.find_file_path(includes_to_find)
        include_path_found = include_file_searcher_obj.get_found_file_list()
        self.assertEqual(len(include_path_found), 0)

        test_env_obj.remove_all()
    
    def test_random_includes_that_dont_exist(self):
        test_env_obj = EnvTestClass(ROOT_DIR_FOR_TEST)
        test_env_obj.create_env_for_test()

        includes_to_find = ['PanieJakieToBagno.hpp', 'WyszkolePanaWJedenKsiezyc.h', 'YYYYYTakJest.hpp']
        include_file_searcher_obj = FileSearcher(ROOT_DIR_FOR_TEST + PROJECT_PATH)
        include_file_searcher_obj.find_file_path(includes_to_find)
        include_path_found = include_file_searcher_obj.get_found_file_list()
        self.assertEqual(len(include_path_found), 0)

        test_env_obj.remove_all()
    
    def test_mix_includes_that_dont_exist_with_exist(self):
        test_env_obj = EnvTestClass(ROOT_DIR_FOR_TEST)
        test_env_obj.create_env_for_test()
        
        mix_list = HPP_FILE_LIST_INC[:]
        mix_list.append("WyszkolePanaWJedenKsiezyc.h")
        mix_list.append("YYYYYTakJest.hpp")
        include_file_searcher_obj = FileSearcher(ROOT_DIR_FOR_TEST + PROJECT_PATH)
        include_file_searcher_obj.find_file_path(mix_list)
        include_path_found_list = include_file_searcher_obj.get_found_file_list()

        for include_found_item in include_path_found_list:
            status = test_env_obj.is_file_include_path_exists(include_found_item)
            self.assertEqual(status, True)

        test_env_obj.remove_all()     
