import unittest
from expressions import *
from ast import *


class Test_AstMethod(unittest.TestCase):    
    

    def test_MethodParsingReturns0(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            uint_32 const* Bar(int* a);
        };
        """).build_ast()  

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1]._identifier, 'Bar')
        self.assertEqual(tree[1]._parameters, 'int* a')
        self.assertEqual(tree[1]._returns, 'uint_32 const*')
        self.assertFalse(tree[1]._constness)


    def test_MethodParsingReturns1(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            A::B const* Bar(int* a);
        };
        """).build_ast()  

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1]._identifier, 'Bar')
        self.assertEqual(tree[1]._parameters, 'int* a')
        # tutaj mi zwraca A:: B const* -> musimy pomyslec nad metoda _parseAndFormatParams
        self.assertEqual(tree[1]._returns, 'A::B const*') 
        self.assertFalse(tree[1]._constness)


    def test_MethodParsingReturns2(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            private:
            G const* Bar(int* a);
        };
        """).build_ast()  

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1]._identifier, 'Bar')
        self.assertEqual(tree[1]._parameters, 'int* a')
        self.assertEqual(tree[1]._returns, 'G const*')
        self.assertFalse(tree[1]._constness)


    def test_MethodParsingReturns3(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            private:
            G::B const* Bar(int* a);
        };
        """).build_ast()  

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1]._identifier, 'Bar')
        self.assertEqual(tree[1]._parameters, 'int* a')
        # tutaj mi zwraca A=G:: B const* -> musimy pomyslec nad metoda _parseAndFormatParams
        self.assertEqual(tree[1]._returns, 'G::B const*')
        self.assertFalse(tree[1]._constness)


    def test_MethodParsingReturns4(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            Foo();
            int Bar(int* a);
        };
        """).build_ast()  

        self.assertTrue(isinstance(tree[2], MethodExpression))
        self.assertEqual(tree[2]._identifier, 'Bar')
        self.assertEqual(tree[2]._parameters, 'int* a')
        self.assertEqual(tree[2]._returns, 'int')
        self.assertFalse(tree[2]._constness)


    def test_MethodParsingReturns5(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            Foo(){}
            int Bar(int* a);
        };
        """).build_ast()  

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1]._identifier, 'Bar')
        self.assertEqual(tree[1]._parameters, 'int* a')
        self.assertEqual(tree[1]._returns, 'int')
        self.assertFalse(tree[1]._constness)


    def test_MethodParsingReturns6(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            Foo(){}
            int const* const Bar(int* a);
        };
        """).build_ast()  

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1]._identifier, 'Bar')
        self.assertEqual(tree[1]._parameters, 'int* a')
        self.assertEqual(tree[1]._returns, 'int const* const')
        self.assertFalse(tree[1]._constness)


    def test_MethodParsingReturns7(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            Foo(){}
            A::B const* const Bar(int* a);
        };
        """).build_ast()  

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1]._identifier, 'Bar')
        self.assertEqual(tree[1]._parameters, 'int* a')
        self.assertEqual(tree[1]._returns, 'A::B const* const')
        self.assertFalse(tree[1]._constness)


    def test_MethodParsingReturns8(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            Foo(){}
            A::B const& const Bar(int* a);
        };
        """).build_ast()  

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1]._identifier, 'Bar')
        self.assertEqual(tree[1]._parameters, 'int* a')
        self.assertEqual(tree[1]._returns, 'A::B const& const')
        self.assertFalse(tree[1]._constness)


    # Focus on parameters part


    def test_MethodParsingParameters0(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            void Bar();
        };
        """).build_ast() 

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1]._identifier, 'Bar')
        self.assertEqual(tree[1]._parameters, '')
        self.assertEqual(tree[1]._returns, 'void')
        self.assertFalse(tree[1]._constness)


    def test_MethodParsingParameters1(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            void Bar(int* a);
        };
        """).build_ast()  

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1]._identifier, 'Bar')
        self.assertEqual(tree[1]._parameters, 'int* a')
        self.assertEqual(tree[1]._returns, 'void')
        self.assertFalse(tree[1]._constness)


    def test_MethodParsingParameters2(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            void Bar(int* a, A::B const* value2);
        };
        """).build_ast()  

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1]._identifier, 'Bar')
        # tutaj tez jest A:: B
        self.assertEqual(tree[1]._parameters, 'int* a, A::B const* value2')
        self.assertEqual(tree[1]._returns, 'void')
        self.assertFalse(tree[1]._constness)


    def test_MethodParsingParameters3(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            void Bar(int* a, A::B const* value2);
        };
        """).build_ast()  

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1]._identifier, 'Bar')
        # tutaj tez jest A:: B
        self.assertEqual(tree[1]._parameters, 'int* a, A::B const* value2')
        self.assertEqual(tree[1]._returns, 'void')
        self.assertFalse(tree[1]._constness)


    def test_MethodParsingParameters4(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            void Bar(int * a);
        };
        """).build_ast()  

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1]._identifier, 'Bar')
        # i tez pytanie czy tutaj powinna byc wersja oryginalna czy nie ?
        # w sumie lepiej wyglada int* a niz int * a
        # do obgadania
        self.assertEqual(tree[1]._parameters, 'int* a')
        self.assertEqual(tree[1]._returns, 'void')
        self.assertFalse(tree[1]._constness)

    
    # Focus on constness part


    def test_MethodParsingConstness0(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            void Bar(int * a) const;
        };
        """).build_ast()  

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertTrue(tree[1]._constness)


    def test_MethodParsingConstness1(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            void Bar(int * a) const;
        };
        """).build_ast()  

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertTrue(tree[1]._constness)