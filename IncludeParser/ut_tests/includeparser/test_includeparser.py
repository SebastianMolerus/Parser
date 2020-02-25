import unittest
from IncludeParser.includeparser import IncludeParser

class Test_IncludeParser(unittest.TestCase):

    def test_parse_system_and_normal_includes(self):
        testStringToParse = ("#include <stdio.h>\n\n"
        "       #include\"hello.hpp\"")
        obj = IncludeParser()
        obj.parse_content(testStringToParse)

        self.assertEqual(len(obj.get_headers()), 1)
        self.assertEqual(len(obj.get_system_headers()), 1)
        self.assertEqual(obj.get_headers()[0], "hello.hpp")
        self.assertEqual(obj.get_system_headers()[0], "stdio.h")
    
    def test_no_includes(self):
        testStringToParse = (" Super Text o #include ")
        obj = IncludeParser()
        obj.parse_content(testStringToParse)

        self.assertEqual(len(obj.get_headers()), 0)
        self.assertEqual(len(obj.get_system_headers()), 0)
    
    def test_mixed_long_includes_with_normal(self):
        testStringToParse = ("#include \"Hello.hpp\"\n"
        "   #include \"Module/H.hpp\"\n"
        "#include \"Module\\timer.h\"\n\n\n"
        "#include <stdio.h>\n"
        "       #include<Module/timer.h>\n")
        obj = IncludeParser()
        obj.parse_content(testStringToParse)

        self.assertEqual(len(obj.get_headers()), 3)
        self.assertEqual(len(obj.get_system_headers()), 2)

        self.assertEqual(obj.get_headers()[0], "Hello.hpp")
        self.assertEqual(obj.get_headers()[1], "H.hpp")
        self.assertEqual(obj.get_headers()[2], "timer.h")
        self.assertEqual(obj.get_system_headers()[0], "stdio.h")
        self.assertEqual(obj.get_system_headers()[1], "Module/timer.h")
