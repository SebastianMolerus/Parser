import unittest
from parsing import Parser
from parsing import Token
from abstracttreebuilder import AbstractTreeBuilder

class Test_ATB(unittest.TestCase):

    def GetAllNodes(self, builder):
        n = []
        while builder.GetNextNode():
            n.append(builder._lastNode)
        return n

    def test_ClassInsindeNamespace(self):
        a = AbstractTreeBuilder.FromTxt(r"namespace Z{class A{};}")
        n = self.GetAllNodes(a)
        self.assertTrue(len(n) == 1)
        self.assertTrue(n[0].name == "Z")
        self.assertTrue(n[0].childNodes[0].name == "A")

    def test_ClassWithoutEndingbracket(self):
        a = AbstractTreeBuilder.FromTxt(r"namespace Z{class A{}}")     
        with self.assertRaises(Exception) as ex:
            n = self.GetAllNodes(a)

    def test_SimplyMethod(self):
        a = AbstractTreeBuilder.FromTxt(r"void foo();")     
        n = self.GetAllNodes(a)
        self.assertTrue(len(n) == 1)
        self.assertTrue(n[0].name == 'foo')

class Test_Parser(unittest.TestCase):

    def GetAllTokens(self, txt):
        p = Parser(Text=txt)
        tokens = []
        while True:
            t = p.GetToken()
            if t == Token.tok_eof:
                break
            tokens.append([t, p.identifier])

        return tokens

    def test_CommentedNsAndClass(self):

        p = Parser(Text="//namespace A\n\
                         class b{}")

        tok1 = p.GetToken()
        self.assertTrue(tok1 == Token.tok_class)
        self.assertTrue(p.identifier == 'class')

        tok2 = p.GetToken()
        self.assertTrue(tok2 == Token.tok_identifier)
        self.assertTrue(p.identifier == 'b')

    def test_CheckingEof(self):
        
        p = Parser(Text="namespace A")
                         
        tok = p.GetToken()
        tok = p.GetToken()
        self.assertTrue(p.identifier == 'A')

    def test_ClassCombinations(self):
        
        code =  "class forwarded;\n"
        code += "class child : public father{\n"
        code += "}\n"
                     
        tokens = self.GetAllTokens(code)

        self.assertTrue(tokens[0] == [Token.tok_class, 'class'])
        self.assertTrue(tokens[1] == [Token.tok_identifier, 'forwarded'])
        self.assertTrue(tokens[2] == [Token.tok_semicolon, ';'])
        self.assertTrue(tokens[3] == [Token.tok_class, 'class'])
        self.assertTrue(tokens[4] == [Token.tok_identifier, 'child'])
        self.assertTrue(tokens[5] == [Token.tok_colon, ':'])
        self.assertTrue(tokens[6] == [Token.tok_public, 'public'])
        self.assertTrue(tokens[7] == [Token.tok_identifier, 'father'])
        self.assertTrue(tokens[8] == [Token.tok_opening_bracket, '{'])
        self.assertTrue(tokens[9] == [Token.tok_closing_bracket, '}'])

    def test_underscoreInIdentifier(self):
        code = "uint32_t"

        p = Parser(Text=code)

        t = p.GetToken()
        self.assertTrue(t == Token.tok_identifier)
        self.assertTrue('uint32_t' == p.identifier)
        self.assertTrue(Token.tok_eof == p.GetToken())

    def test_methodWithTwoParams(self):

        code = "void someMethod(uint32_t& someRef, uint8_t* ptr) const;"

        tokens = self.GetAllTokens(code)

        self.assertTrue(tokens[0] == [Token.tok_identifier, 'void'])
        self.assertTrue(tokens[1] == [Token.tok_identifier, 'someMethod'])
        self.assertTrue(tokens[2] == [Token.tok_params_begin, '('])
        self.assertTrue(tokens[3] == [Token.tok_identifier, 'uint32_t'])
        self.assertTrue(tokens[4] == [Token.tok_ref, '&'])
        self.assertTrue(tokens[5] == [Token.tok_identifier, 'someRef'])
        self.assertTrue(tokens[6] == [Token.tok_comma, ','])
        self.assertTrue(tokens[7] == [Token.tok_identifier, 'uint8_t'])
        self.assertTrue(tokens[8] == [Token.tok_star, '*'])
        self.assertTrue(tokens[9] == [Token.tok_identifier, 'ptr'])
        self.assertTrue(tokens[10] == [Token.tok_params_end, ')'])
        self.assertTrue(tokens[11] == [Token.tok_identifier, 'const'])
        self.assertTrue(tokens[12] == [Token.tok_semicolon, ';'])

    def test_notValidCommentedCode(self):

        code = " / some bad comment;"

        with self.assertRaises(Exception) as ex:
            t = self.GetAllTokens(code)

    def test_ValidCommentedCode(self):

        code = " // class A{}\n"
        code += "    class B\n "

        t = self.GetAllTokens(code)

        self.assertTrue(len(t) == 2)
        self.assertTrue(t[1] == [Token.tok_identifier, 'B'])
 
    def test_IgnorePreprocessorDirectives(self):

        code =  "#define something class A{}\n"
        code += "#endif"
        code += "#ifndef struct B{}"

        t = self.GetAllTokens(code)

        self.assertTrue(len(t) == 0)

    def test_IgnoreLongComments(self):
        code =  "/// @file ble.hpp\n"
        t = self.GetAllTokens(code)
        self.assertTrue(len(t) == 0)

    def test_ignoreInclude(self):
        code = "#include <stdint.h>"
        t = self.GetAllTokens(code)
        self.assertTrue(len(t) == 0)

    def test_ignoreFriends(self):
        code = "friend class NamespaceA::NamespaceB::someClass"
        t = self.GetAllTokens(code)
        self.assertTrue(len(t) == 0)


def main():
    unittest.main()