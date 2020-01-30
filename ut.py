import unittest

from AST import AbstractTreeBuilder

from tokenstream import TokenStream

from TokenReader import TokenReader
from TokenReader import TokenType

from Expressions import *

from nodes import Node


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

    def test_GetDesctructorInsideClass(self):
        reader = TokenReader(text="""class Foo {
                                     ~Foo();
                                };""")
        tokens = _TokenReader_get_all_tokens(reader)
        self.assertEqual(tokens[0].type, TokenType._class)
        self.assertEqual(tokens[0].content, "class")

        self.assertEqual(tokens[1].type, TokenType._identifier)
        self.assertEqual(tokens[1].content, "Foo")

        self.assertEqual(tokens[2].type, TokenType._opening_bracket)
        self.assertEqual(tokens[2].content, "{")

        self.assertEqual(tokens[3].type, TokenType._tilde)
        self.assertEqual(tokens[3].content, "~")

        self.assertEqual(tokens[4].type, TokenType._identifier)
        self.assertEqual(tokens[4].content, "Foo")

        self.assertEqual(tokens[5].type, TokenType._params_begin)
        self.assertEqual(tokens[5].content, "(")

        self.assertEqual(tokens[6].type, TokenType._params_end)
        self.assertEqual(tokens[6].content, ")")

        self.assertEqual(tokens[7].type, TokenType._semicolon)
        self.assertEqual(tokens[7].content, ";")

        self.assertEqual(tokens[8].type, TokenType._closing_bracket)
        self.assertEqual(tokens[8].content, "}")

        self.assertEqual(tokens[9].type, TokenType._semicolon)
        self.assertEqual(tokens[9].content, ";")


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


    def test_CtorSimple(self):
        reader = TokenReader(text="""
        class A{
            A();
        };
        """)

        s = TokenStream(reader)
        a = AbstractTreeBuilder(s)

        tree = a.build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertTrue(isinstance(tree[1], CTorExpression))
        self.assertEqual(tree[1]._identifier, 'A')

        # wedlug mnie identifikator kontruktora nie powinien byc A() tylko A
        # patrz test_TwoCtorsOneImplementedAnotherNot


    def test_CtorImplementedMethodSameAsNamespace(self):
        reader = TokenReader(text="""
        namespace A{
            void A(){}
        }
        """)

        s = TokenStream(reader)
        a = AbstractTreeBuilder(s)

        tree = a.build_ast()

        self.assertEqual(len(tree),1)
        self.assertEqual(tree[0], NamespaceExpression('A'))


    def test_CtorNotImplementedMethodSameAsNamespace(self):
        reader = TokenReader(text="""
        namespace A{
            void A();
        };
        """)

        s = TokenStream(reader)
        a = AbstractTreeBuilder(s)

        tree = a.build_ast()

        self.assertFalse(isinstance(tree[1], CTorExpression))

        # mozna skompilowac taka sama nazwe metody jak klasa
        # trzeba zabezpieczyc to czy context konstruktora to faktycznie klasa


    def test_CtorWithOneParameter(self):
        reader = TokenReader(text="""
        class A{A(uint32_t& value1);};
        """)

        s = TokenStream(reader)
        a = AbstractTreeBuilder(s)

        tree = a.build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertEqual(tree[1], CTorExpression('A', 'uint32_t& value1')) 
        # zakladam ze parametry zapisujemy w formie oryginalnej bez dodatkowych spacji
        # do obgadania

    
    def test_CtorWithTwoParameters(self):
        reader = TokenReader(text="""
        class A{A(uint32_t& value1, const uint32_t* value2);};
        """)

        s = TokenStream(reader)
        a = AbstractTreeBuilder(s)

        tree = a.build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertEqual(tree[1], CTorExpression('A', 'uint32_t& value1, const uint32_t* value2'))
        # zakladam ze parametry zapisujemy w formie oryginalnej bez dodatkowych spacji
        # do obgadania ( swiadome kopiuj wklej z testu wyzej )


    def test_TwoCtorsOneImplementedAnotherNot(self):
        reader = TokenReader(text="""
        class A{A(){}A(int a);};
        """)

        s = TokenStream(reader)
        a = AbstractTreeBuilder(s)

        tree = a.build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertEqual(tree[1], CTorExpression('A', 'int a'))

        # tutaj kolejny argument zeby identifikator by A a nie A()
        # poniewaz tutaj wczytalo ze konstruktor z jednym parametrem
        # A(int a) ma identyfikator A()
        # jezeli chcemy indetyfikator w formie A(...) to po co nam parametry


    def test_TwoCtorsImplemented(self):
        reader = TokenReader(text="""
        class A{
            A();
            A(int v);
            };
        """)

        s = TokenStream(reader)
        a = AbstractTreeBuilder(s)

        tree = a.build_ast()

        self.assertEqual(len(tree), 3)
        self.assertEqual(tree[0], ClassExpression('A'))

        self.assertEqual(tree[1], CTorExpression('A', ''))
        
        self.assertTrue(isinstance(tree[2], CTorExpression))
        self.assertEqual(tree[2].parameters, 'int v', "Parameters does not match.")
        self.assertEqual(tree[2]._identifier, 'A', 'Ctor identifier does not match.')


    def test_CtorWithNewlinedParameters(self):
        reader = TokenReader(text="""
        class MegaPrzydatnaKlasa{
            MegaPrzydatnaKlasa(int*& val1,
                               SomeOtherType const& val2);
            };
        """)

        s = TokenStream(reader)
        a = AbstractTreeBuilder(s)

        tree = a.build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('MegaPrzydatnaKlasa'))
        self.assertEqual(tree[1]._identifier, 'MegaPrzydatnaKlasa')
        self.assertEqual(tree[1].parameters, 'int*& val1, SomeOtherType const& val2')
        self.assertTrue(isinstance(tree[1], CTorExpression))


    def test_CtorNoCtor(self):
        reader = TokenReader(text="""
        class Foo{
            void Method();
        """)

        s = TokenStream(reader)
        a = AbstractTreeBuilder(s)

        tree = a.build_ast()

        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0], ClassExpression('Foo'))


    def test_CtorTwoCtorsOneWithGarbageInside(self):
        reader = TokenReader(text="""
        class Foo{
            Foo()
            {
                Foo* ptr = new Foo();
                delete ptr;
            }

            Foo(int v);
        """)

        s = TokenStream(reader)
        a = AbstractTreeBuilder(s)

        tree = a.build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('Foo'))
        self.assertEqual(tree[1]._identifier, 'Foo')
        self.assertEqual(tree[1].parameters, 'int v')
        self.assertTrue(isinstance(tree[1], CTorExpression))


    def test_DtorSimpleNotImplemented(self):
        reader = TokenReader(text="""
        class A{
            void ~A();
        };
        """)

        s = TokenStream(reader)
        a = AbstractTreeBuilder(s)

        tree = a.build_ast()

        self.assertEqual(len(tree),2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertEqual(tree[1], DTorExpression('A'))

        # wedlug mnie identyfikator destruktora tez powinien byc A nie ~A()
        # do obgadania


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