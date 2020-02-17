import unittest
from includeparser import IncludeParser

class Test_IncludeParser(unittest.TestCase):

    def test_parseSystemAndNormalInclude(self):
        testStringToParse = ("#include <stdio.h>\n\n"
        "//#include\n"
        "       #include\"hello.hpp\"")
        obj = IncludeParser(testStringToParse)

        self.assertEqual(len(obj.get_headers), 1)
        self.assertEqual(len(obj.get_system_headers()), 1)
        self.assertEqual(obj.get_headers[0], "hello.hpp")
        self.assertEqual(obj.get_system_headers()[0], "stdio.h")
    
    def test_noIncludes(self):
        testStringToParse = ("//#include\n")
        obj = IncludeParser(testStringToParse)

        self.assertEqual(len(obj.get_headers), 0)
        self.assertEqual(len(obj.get_system_headers()), 0)
    