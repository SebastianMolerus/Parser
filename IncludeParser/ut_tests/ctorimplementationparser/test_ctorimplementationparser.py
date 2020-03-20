import unittest
from TreeBuilder.expressions import CTorExpression
from IncludeParser.ctorimplementationparser import CtorImplementationParser

class Test_CtorImplementationParser(unittest.TestCase):

    def _create_source_code_for_test(self, ctor_impl_str):
        start_test_str = ("#include <iostream>\n\n"
        "//------- START FILE -------\n"
        "namespace TestNs {\n\n"
        "TestClass::GetMemberA()\n"
        "{\n"
        "	return m_a;\n"
        "}\n\n"
        "TestClass::SetMemberA(int a) {m_a = a;}\n\n")

        end_test_str = ("\n\n"
        "// ---- END OF FILE ----\n"
        "Func(int a, int b)\n"
        "{\n"
        "	return a+b;\n"
        "}\n"
        "} //End of TestNS\n")

        source_file_str = start_test_str + ctor_impl_str + end_test_str
        return source_file_str

    def test_parse_one_line_ctor_implementation(self):
        ctor_expression_obj = CTorExpression(identifier="TestClass", parameters="int a")
        ctor_expression_obj.father = "TestClass"

        exp_ctor_impl_str = "TestClass::TestClass(int a) : m_a(a){ int *ptr = new int(5); }"
        test_code_str = self._create_source_code_for_test(exp_ctor_impl_str)

        sut = CtorImplementationParser(None, test_code_str)
        sut.fill_with_ctor_implementation(ctor_expression_obj)

        self.assertEqual(ctor_expression_obj.implementation.rstrip(), exp_ctor_impl_str.rstrip())
    
    def test_parse_multiline_ctor_implementation(self):
        ctor_expression_obj = CTorExpression(identifier="TestClass", parameters="int a, int b")
        ctor_expression_obj.father = "TestClass"

        exp_ctor_impl_str = ("TestClass::TestClass(int a, int b) \n"
        ": m_a(a), m_b(b)\n"
        "{\n"
        "	int *ptr = new int(50);\n"
        "	int *ptr2 = new int(50);\n"
        "}\n")

        test_code_str = self._create_source_code_for_test(exp_ctor_impl_str)

        sut = CtorImplementationParser(None, test_code_str)
        sut.fill_with_ctor_implementation(ctor_expression_obj)

        self.assertEqual(ctor_expression_obj.implementation.rstrip(), exp_ctor_impl_str.rstrip())
    
    def test_no_parse_default_ctor_implementation(self):
        ctor_expression_obj = CTorExpression(identifier="TestClass", parameters="")
        ctor_expression_obj.father = "TestClass"

        exp_ctor_impl_str = ("TestClass::TestClass() \n"
        "{\n"
        "	char *ptr = new char(5)\n"
        "}\n")

        test_code_str = self._create_source_code_for_test(exp_ctor_impl_str)
        sut = CtorImplementationParser(None, test_code_str)
        sut.fill_with_ctor_implementation(ctor_expression_obj)

        self.assertEqual(ctor_expression_obj.implementation, None)

