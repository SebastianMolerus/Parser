import unittest

from AST import AbstractTreeBuilder

from TokenStream import TokenStream

from TokenReader import TokenReader
from TokenReader import TokenType

from Expressions import Expression
from Expressions import NamespaceExpression
from Expressions import ClassExpression

from Nodes import Node


# ------------------------------------------------------------
# ------------------- HELPER METHODS -------------------------


def _TokenReader_get_all_tokens(TokenReader):
    tokens = []
    while True:
        token = TokenReader.get_next_token()
        if token.type == TokenType._eof:
            break
        tokens.append(token)

    return tokens


# ------------------------------------------------------------
# --------------------- TESTS --------------------------------


class Test_TokenReader(unittest.TestCase):
    def test_get_next_tokenClassForwardDeclared(self):
        reader = TokenReader(text="class A;")
        token1 = reader.get_next_token()
        token2 = reader.get_next_token()
        token3 = reader.get_next_token()

        self.assertEqual(token1.type, TokenType._class)

        self.assertEqual(token2.type, TokenType._identifier)
        self.assertEqual(token2.content, "A")

        self.assertEqual(token3.type, TokenType._semicolon)
        self.assertEqual(token3.content, ";")


    def test_get_next_tokenCommented(self):
        reader = TokenReader(text="//class A;")
        token1 = reader.get_next_token()

        self.assertEqual(token1.type, TokenType._eof)


    def test_get_next_tokenClassDefinition(self):
        reader = TokenReader(text=""" //class A;
                                      class B{};     """)
        token1 = reader.get_next_token()
        token2 = reader.get_next_token()
        token3 = reader.get_next_token()
        token4 = reader.get_next_token()
        token5 = reader.get_next_token()

        self.assertEqual(token1.type, TokenType._class)

        self.assertEqual(token2.type, TokenType._identifier)
        self.assertEqual(token2.content, "B")

        self.assertEqual(token3.type, TokenType._opening_bracket)

        self.assertEqual(token4.type, TokenType._closing_bracket)

        self.assertEqual(token5.type, TokenType._semicolon)


    def test_get_next_tokenMethodDefinition1(self):
        reader = TokenReader(text=r"void Foo::Bar(uint32_t& ref, int * ptr) const;")
        tokens = _TokenReader_get_all_tokens(reader)

        self.assertEqual(len(tokens), 16)

        self.assertEqual(tokens[0].type, TokenType._identifier)
        self.assertEqual(tokens[0].content, "void")

        self.assertEqual(tokens[1].type, TokenType._identifier)
        self.assertEqual(tokens[1].content, "Foo")

        self.assertEqual(tokens[2].type, TokenType._colon)
        self.assertEqual(tokens[2].content, ":")

        self.assertEqual(tokens[3].type, TokenType._colon)
        self.assertEqual(tokens[3].content, ":")

        self.assertEqual(tokens[4].type, TokenType._identifier)
        self.assertEqual(tokens[4].content, "Bar")

        self.assertEqual(tokens[5].type, TokenType._params_begin)
        self.assertEqual(tokens[5].content, "(")

        self.assertEqual(tokens[6].type, TokenType._identifier)
        self.assertEqual(tokens[6].content, "uint32_t")

        self.assertEqual(tokens[7].type, TokenType._ref)
        self.assertEqual(tokens[7].content, "&")

        self.assertEqual(tokens[8].type, TokenType._identifier)
        self.assertEqual(tokens[8].content, "ref")

        self.assertEqual(tokens[9].type, TokenType._comma)
        self.assertEqual(tokens[9].content, ",")

        self.assertEqual(tokens[10].type, TokenType._identifier)
        self.assertEqual(tokens[10].content, "int")

        self.assertEqual(tokens[11].type, TokenType._star)
        self.assertEqual(tokens[11].content, "*")

        self.assertEqual(tokens[12].type, TokenType._identifier)
        self.assertEqual(tokens[12].content, "ptr")

        self.assertEqual(tokens[13].type, TokenType._params_end)
        self.assertEqual(tokens[13].content, ")")

        self.assertEqual(tokens[14].type, TokenType._const)
        self.assertEqual(tokens[14].content, "const")

        self.assertEqual(tokens[15].type, TokenType._semicolon)
        self.assertEqual(tokens[15].content, ";")


    def test_get_next_tokenEoF(self):
        reader = TokenReader(text=r"//void Foo::Bar(uint32_t& ref, int * ptr) const;")
        token = reader.get_next_token()

        self.assertEqual(token.type, TokenType._eof)
        self.assertEqual(token.content, "")

    def test_GetTokenInvalidComment(self):
        reader = TokenReader(text=r"/void Foo::Bar(uint32_t& ref, int * ptr) const;")
        with self.assertRaises(Exception):
            reader.get_next_token()

    def test_GetTokenPreprocIgnored(self):
        reader = TokenReader(text="""#ifndef HEADER_HPP
                                     #define HEADER_HPP""")

        token = reader.get_next_token()

        self.assertEqual(token.type, TokenType._eof)
        self.assertEqual(token.content, "")

    def test_GetTokenInsideClass1(self):
        reader = TokenReader(text="""class Foo : private Bar{   
                                     public:                    
                                     private:                   
                                     protected:                 
                                     };""")

        tokens = _TokenReader_get_all_tokens(reader)

        self.assertEqual(len(tokens), 14)

        self.assertEqual(tokens[0].type, TokenType._class)
        self.assertEqual(tokens[0].content, "class")

        self.assertEqual(tokens[1].type, TokenType._identifier)
        self.assertEqual(tokens[1].content, "Foo")

        self.assertEqual(tokens[2].type, TokenType._colon)
        self.assertEqual(tokens[2].content, ":")

        self.assertEqual(tokens[3].type, TokenType._private)
        self.assertEqual(tokens[3].content, "private")

        self.assertEqual(tokens[4].type, TokenType._identifier)
        self.assertEqual(tokens[4].content, "Bar")

        self.assertEqual(tokens[5].type, TokenType._opening_bracket)
        self.assertEqual(tokens[5].content, "{")

        self.assertEqual(tokens[6].type, TokenType._public)
        self.assertEqual(tokens[6].content, "public")

        self.assertEqual(tokens[7].type, TokenType._colon)
        self.assertEqual(tokens[7].content, ":")

        self.assertEqual(tokens[8].type, TokenType._private)
        self.assertEqual(tokens[8].content, "private")

        self.assertEqual(tokens[9].type, TokenType._colon)
        self.assertEqual(tokens[9].content, ":")

        self.assertEqual(tokens[10].type, TokenType._protected)
        self.assertEqual(tokens[10].content, "protected")

        self.assertEqual(tokens[11].type, TokenType._colon)
        self.assertEqual(tokens[11].content, ":")
        
        self.assertEqual(tokens[12].type, TokenType._closing_bracket)
        self.assertEqual(tokens[12].content, "}")
        
        self.assertEqual(tokens[13].type, TokenType._semicolon)
        self.assertEqual(tokens[13].content, ";")


class Test_AbstractTreeBuilder(unittest.TestCase):

    def test_OneSimpleNamespace(self):
        reader = TokenReader(text=r"namespace N1{}")
        s = TokenStream(reader)
        a = AbstractTreeBuilder(s)

        tree = a.build_ast()

        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0], NamespaceExpression('N1'))


    def test_NamespaceWithNestedClass(self):
        reader = TokenReader(text=r"namespace N1{class C1{};};")
        s = TokenStream(reader)
        a = AbstractTreeBuilder(s)

        tree = a.build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], NamespaceExpression('N1'))
        self.assertEqual(tree[1], ClassExpression('C1'))
        self.assertEqual(tree[1].get_father(), tree[0])

       
    def test_NamespaceWithNestedNamespace(self):
        reader = TokenReader(text="""
        namespace N1{
            namespace N2{}
        }
        """)

        s = TokenStream(reader)
        a = AbstractTreeBuilder(s)

        tree = a.build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], NamespaceExpression('N1'))
        self.assertEqual(tree[1], NamespaceExpression('N2'))
    

class Test_Node(unittest.TestCase):

    def test_Root(self):
        grandFather = Node()
        father = Node()
        child = Node()

        grandFather.attach(father)
        father.attach(child)

        self.assertEqual(child.get_root(), grandFather)
        self.assertEqual(father.get_root(), grandFather)
        self.assertEqual(grandFather.get_root(), None)

    
    def test_Father(self):
        grandFather = Node()
        father = Node()
        child = Node()

        grandFather.attach(father)
        father.attach(child)

        self.assertEqual(child.get_father(), father)
        self.assertEqual(father.get_father(), grandFather)
        self.assertEqual(grandFather.get_father(), None)



def main():
    unittest.main()