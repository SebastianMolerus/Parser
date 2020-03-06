import os
import errno
import shutil

PROJECT_PATH = "\\Env_Test_Path\\Project_Bagno\\"

INCLUDES_PATH = PROJECT_PATH + "Inc\\"
INCLUDES_PATH_2 = PROJECT_PATH + "Inc_2\\"
INCLUDES_PATH_ALL = PROJECT_PATH + "Inc_All\\"

MODULE_FOR_TEST = PROJECT_PATH + "MODULE_TEST\\MODULE_1\\"
MODULE_NAME_HPP = "module_1.hpp"
MODULE_NAME_CPP = "module_1.cpp"

ENV_TEST_PATH = [PROJECT_PATH, INCLUDES_PATH, INCLUDES_PATH_2, INCLUDES_PATH_ALL, MODULE_FOR_TEST]


HPP_FILE_LIST_INC = ["Inc_header_1.hpp", "Inc_header_2.hpp", "Inc_header_3.hpp", "Inc_header_4.hpp", "Inc_header_5.hpp"]
H_FILE_LIST_INC = ["Inc_header_1.h", "Inc_header_2.h", "Inc_header_3.h", "Inc_header_4.h", "Inc_header_5.h"]

HPP_FILE_LIST_INC_2 = ["Inc2_header_1.hpp", "Inc2_header_2.hpp", "Inc2_header_3.hpp", "Inc2_header_4.hpp", "Inc2_header_5.hpp"]
H_FILE_LIST_INC_2 = ["Inc2_header_1.h", "Inc2_header_2.h", "Inc2_header_3.h", "Inc2_header_4.h", "Inc2_header_5.h"]

SYS_HEADER_LIST = ["#include <iostream>", "#include <stdio.h>", "#include <string>", "#include <algorithm>", "#include <vector>"]


HEADER_ALL_FILE_LIST_1 = ["Inc_header_hpp_all.hpp"]
HEADER_ALL_FILE_LIST_2 = ["Inc2_header_hpp_all.hpp"]
HEADER_ALL_FILE_LIST_3 = ["Inc_header_h_all.hpp"]
HEADER_ALL_FILE_LIST_4 = ["Inc2_header_h_all.hpp"]


NUMBER_OF_HEADER_FILES = len(HPP_FILE_LIST_INC) + len(H_FILE_LIST_INC) + len(HPP_FILE_LIST_INC_2) + len(H_FILE_LIST_INC_2) + len(HEADER_ALL_FILE_LIST_1) + len(HEADER_ALL_FILE_LIST_2) + len(HEADER_ALL_FILE_LIST_3) + len(HEADER_ALL_FILE_LIST_4)

class EnvTestClass:
    def __init__(self, test_path):
        if test_path:
            self._exp_header_path_list = []
            self._test_path = test_path
        else:
            raise Exception("Testing PATH missing")
    
    def create_env_for_test(self):
        self._create_env_folders()
        self._create_empty_header_files(self._test_path + INCLUDES_PATH, HPP_FILE_LIST_INC)
        self._create_empty_header_files(self._test_path + INCLUDES_PATH, H_FILE_LIST_INC)
        self._create_empty_header_files(self._test_path + INCLUDES_PATH_2, HPP_FILE_LIST_INC_2)
        self._create_empty_header_files(self._test_path + INCLUDES_PATH_2, H_FILE_LIST_INC_2)
        self._create_filled_headers_for_test(self._test_path + INCLUDES_PATH_ALL, HEADER_ALL_FILE_LIST_1, HPP_FILE_LIST_INC)
        self._create_filled_headers_for_test(self._test_path + INCLUDES_PATH_ALL, HEADER_ALL_FILE_LIST_2, HPP_FILE_LIST_INC_2)
        self._create_filled_headers_for_test(self._test_path + INCLUDES_PATH_ALL, HEADER_ALL_FILE_LIST_3, H_FILE_LIST_INC)
        self._create_filled_headers_for_test(self._test_path + INCLUDES_PATH_ALL, HEADER_ALL_FILE_LIST_4, H_FILE_LIST_INC_2)
        self._create_module_1_for_test()
    
    def get_exp_header_test_path_list(self):
        return self._exp_header_path_list

    def remove_all(self):
        shutil.rmtree(self._test_path  + "\\Env_Test_Path\\")
    
    def is_file_include_path_exists(self, include_path_item):
        if include_path_item in self._exp_header_path_list:
            return True
        else:
            return False

    def _create_env_folders(self):
        dir_path_str = ""
        for dir_path in ENV_TEST_PATH:
            dir_path_str = self._test_path + dir_path
            if not os.path.exists(dir_path_str):
                os.makedirs(dir_path_str)
    
    def _create_empty_header_files(self, path, file_list):
        path_str = ""
        for list_item in file_list:
            path_str = path + list_item
            f = open(path_str, "w")
            f.close()
            self._exp_header_path_list.append(path_str)
    
    def _create_filled_headers_for_test(self, path, header_all_list, include_to_write_list):
        path_str = ""
        for list_item in header_all_list:
            path_str = path + list_item
            f = open(path_str, "w")
            for include_to_write in include_to_write_list:
                f.write("#include " + "\"" + include_to_write + "\"\n")
            for sys_include in SYS_HEADER_LIST:
                f.write(sys_include + "\n")
            f.close()
            self._exp_header_path_list.append(path_str)
    
    def _create_module_1_for_test(self):
        header_path_str = self._test_path + MODULE_FOR_TEST + MODULE_NAME_HPP
        source_path_str = self._test_path + MODULE_FOR_TEST + MODULE_NAME_CPP

        f = open(header_path_str, "w")
        for header_item in HEADER_ALL_FILE_LIST_1:
            f.write("#include " + "\"" + header_item + "\"\n")

        for header_item in HEADER_ALL_FILE_LIST_2:
            f.write("#include " + "\"" + header_item + "\"\n")
        
        f.write("\n#define TIME 1\n#define HELLO\nclass Test\n{\n Test();\n};")
        f.close()

        f = open(source_path_str, "w")
        f.write("#include \"module_1.hpp\"\n\n//---------------------\n\n")

        for header_item in HEADER_ALL_FILE_LIST_3:
            f.write("#include           " + "\"" + header_item + "\"\n\n\n\n\n")

        for header_item in HEADER_ALL_FILE_LIST_4:
            f.write("#include " + "\"" + header_item + "\"\n")
        f.close()
