import unittest

from parsing import Parser
from parsing import Token

from tokenstream import TokenStream

from abstracttreebuilder import AbstractTreeBuilder

class Test_TokenStream(unittest.TestCase):
    def test_Initialize(self):
        p = Parser(Text="namespace A; class B;")                 
        t = TokenStream(p)
        self.assertTrue(len(t._cache) == 6)

    def test_CurrentTokenAssignedToFirstElement(self):
        p = Parser(Text="namespace A; class B;")        
        t = TokenStream(p)
        self.assertTrue(t.current.content == 'namespace')

    def test_IterateForwardAndBackward(self):
        p = Parser(Text="namespace A;")        
        t = TokenStream(p)

        while t.next():
            pass

        self.assertTrue(t.current.content == ';')

        while t.prev():
            pass

        self.assertTrue(t.current.content == 'namespace')

    def test_Seeking(self):
        p = Parser(Text="namespace A class B struct D")        
        t = TokenStream(p)

        t.next()
        t.next()
        self.assertTrue(t.current.content == 'class')
        self.assertTrue(t.seek(0).content == 'class')

        self.assertTrue(t.seek(-1).content == 'A')
        self.assertTrue(t.seek(-2).content == 'namespace')
        self.assertTrue(t.seek(-3).content == 'namespace')
        self.assertTrue(t.seek(-9).content == 'namespace')

        self.assertTrue(t.seek(1).content == "B")
        self.assertTrue(t.seek(2).content == "struct")
        self.assertTrue(t.seek(3).content == "D")
        self.assertTrue(t.seek(4).content == "D")
        self.assertTrue(t.seek(10000).content == "D")

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

    def test_ColonsAsIdentifiers(self):
        p = Parser(Text="A::b")
        p.GetToken()
        self.assertEqual(p.identifier, 'A::b')

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

        code = "void someMethod(uint32_t & someRef, uint8_t * ptr) const;"

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
        self.assertTrue(tokens[11] == [Token.tok_const, 'const'])
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

class ContextStub:
    def __init__(self, name):
        self.name = name

class Test_ATB(unittest.TestCase):

    def _set_token_stream_on_inputs_begin(self, token_stream):
        while token_stream.next() and token_stream.current.type != Token.tok_params_begin:
            pass

    def test_Parse_Expression_CtorSuccess(self):
        p = Parser(Text="A();")               
        t = TokenStream(p)
        self._set_token_stream_on_inputs_begin(t)
        c = ContextStub("A")
        a = AbstractTreeBuilder(t)

        CtorExp = a.Parse_Expression(c)

        self.assertEqual(CtorExp.name, "A")
        self.assertEqual(CtorExp.params, "")
        self.assertEqual(t.current.content, r";")
  
    def test_Parse_Expression_ParseCtorImplementedInline(self):
        p = Parser(Text=r"A(){};")               
        t = TokenStream(p)
        self._set_token_stream_on_inputs_begin(t)
        c = ContextStub("A")
        a = AbstractTreeBuilder(t)

        self.assertIsNone(a.Parse_Expression(c))
        self.assertTrue(t.current.content == r"{")

    def test_Parse_Expression_ParseCtorWithDifferentContext(self):
        p = Parser(Text=r");A(){}")               
        t = TokenStream(p)
        self._set_token_stream_on_inputs_begin(t)
        c = ContextStub("B")
        a = AbstractTreeBuilder(t)

        self.assertIsNone(a.Parse_Expression(c))
        self.assertTrue(t.current.content == r"{")

    def test_Parse_Expression_CopyCtorSuccess(self):
        p = Parser(Text=r"class A{A(A const& other);")               
        t = TokenStream(p)
        self._set_token_stream_on_inputs_begin(t)
        c = ContextStub("A")
        a = AbstractTreeBuilder(t)
        CopyCtorExp = a.Parse_Expression(c)

        self.assertEqual(CopyCtorExp.name, "A")
        self.assertEqual(CopyCtorExp.params, "A const & other")
        self.assertEqual(t.current.content, r";")

    def test_Parse_Expression_CopyCtorImplementedInline(self):
        p = Parser(Text=r"const;A(A const& other){}")               
        t = TokenStream(p)
        self._set_token_stream_on_inputs_begin(t)
        c = ContextStub("A")
        a = AbstractTreeBuilder(t)

        self.assertIsNone(a.Parse_Expression(c))
        self.assertEqual(t.current.content, r"{")

    def test_Parse_Expression_AssignOperatorSuccess(self):
        p = Parser(Text=r"A& operator=(A const& other);")               
        t = TokenStream(p)
        self._set_token_stream_on_inputs_begin(t)
        c = ContextStub("A")
        a = AbstractTreeBuilder(t)
        op = a.Parse_Expression(c)

        self.assertEqual(op.params, "A const & other")
        self.assertEqual(op.returns,  "A&")
        self.assertEqual(t.current.content, r";")

    def test_Parse_Expression_AssignOperatorImplementedInline(self):
        p = Parser(Text=r"A& operator=(A const& other){")               
        t = TokenStream(p)
        self._set_token_stream_on_inputs_begin(t)
        c = ContextStub("A")
        a = AbstractTreeBuilder(t)

        self.assertIsNone(a.Parse_Expression(c))
        self.assertEqual(t.current.content, r"{")

    def test_Parse_Expression_EasiestMethodToParse(self):
        p = Parser(Text=r"{void m();")               
        t = TokenStream(p)
        self._set_token_stream_on_inputs_begin(t)
        c = ContextStub("A")
        a = AbstractTreeBuilder(t)
        m = a.Parse_Expression(c)

        self.assertEqual(m.name, "m")
        self.assertEqual(m.params, "")
        self.assertEqual(t.current.content, r";")

def main():
    unittest.main()