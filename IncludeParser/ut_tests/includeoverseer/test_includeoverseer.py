import unittest
import os
from IncludeParser.includeoverseer import IncludeOverseer
from IncludeParser.ut_tests.create_enviroment_for_test import PROJECT_PATH
from IncludeParser.ut_tests.create_enviroment_for_test import MODULE_NAME_HPP
from IncludeParser.ut_tests.create_enviroment_for_test import MODULE_FOR_TEST
from IncludeParser.ut_tests.create_enviroment_for_test import MODULE_NAME_CPP
from IncludeParser.ut_tests.create_enviroment_for_test import EnvTestClass

ROOT_DIR_FOR_TEST = os.path.dirname(os.path.abspath(__file__))

class Test_IncludeOverseer(unittest.TestCase):

    def test_all_header_path_from_file(self):
        test_env_obj = EnvTestClass(ROOT_DIR_FOR_TEST)
        test_env_obj.create_env_for_test()
        
        test_object = IncludeOverseer(ROOT_DIR_FOR_TEST + MODULE_FOR_TEST + MODULE_NAME_HPP, ROOT_DIR_FOR_TEST + PROJECT_PATH)
        test_object.parse_all()
        include_path_found_list = test_object.get_headers_for_stub()
        for include_found_item in include_path_found_list:
            status = test_env_obj.is_file_include_path_exists(include_found_item)
            self.assertEqual(status, True)
        
        test_env_obj.remove_all()

        


