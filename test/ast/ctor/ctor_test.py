import unittest
from expressions import *
from ast import *

class Test_AstCtor(unittest.TestCase):


    def test_CtorSimple(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            A();
        };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertTrue(isinstance(tree[1], CTorExpression))
        self.assertEqual(tree[1]._identifier, 'A')


    def test_CtorImplementedMethodSameAsNamespace(self):
        tree = AbstractTreeBuilder(source_code="""
        namespace A{
            void A(){}
        }
        """).build_ast()

        self.assertEqual(len(tree),1)
        self.assertEqual(tree[0], NamespaceExpression('A'))


    def test_CtorNotImplementedMethodSameAsNamespace(self):
        tree = AbstractTreeBuilder(source_code="""
        namespace A{
            void A();
        };
        """).build_ast()

        self.assertFalse(isinstance(tree[1], MethodExpression))

        # Dziwne dlaczego to nie przechodzi ?!


    def test_CtorWithOneParameter(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{A(uint32_t& value1);};
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertEqual(tree[1], CTorExpression('A', 'uint32_t& value1')) 
 

    def test_CtorWithTwoParameters(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{A(uint32_t& value1, const uint32_t* value2);};
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertEqual(tree[1], CTorExpression('A', 'uint32_t& value1, const uint32_t* value2'))


    def test_TwoCtorsOneImplementedAnotherNot(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{A(){}A(int a);};
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertEqual(tree[1], CTorExpression('A', 'int a'))


    def test_TwoCtorsImplemented(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            A();
            A(int v);
            };
        """).build_ast()

        self.assertEqual(len(tree), 3)
        self.assertEqual(tree[0], ClassExpression('A'))

        self.assertEqual(tree[1], CTorExpression('A', ''))
        
        self.assertTrue(isinstance(tree[2], CTorExpression))
        self.assertEqual(tree[2].parameters, 'int v', "Parameters does not match.")
        self.assertEqual(tree[2]._identifier, 'A', 'Ctor identifier does not match.')


    def test_CtorWithNewlinedParameters(self):
        tree = AbstractTreeBuilder(source_code="""
        class MegaPrzydatnaKlasa{
            MegaPrzydatnaKlasa(int*& val1,
                               SomeOtherType const& val2);
            };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('MegaPrzydatnaKlasa'))
        self.assertEqual(tree[1]._identifier, 'MegaPrzydatnaKlasa')
        self.assertEqual(tree[1].parameters, 'int*& val1, SomeOtherType const& val2')
        self.assertTrue(isinstance(tree[1], CTorExpression))


    def test_CtorNoCtor(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            void Method();
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('Foo'))


    def test_CtorTwoCtorsOneWithGarbageInside(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            Foo()
            {
                Foo* ptr = new Foo();
                delete ptr;
            }

            Foo(int v);
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('Foo'))
        self.assertEqual(tree[1]._identifier, 'Foo')
        self.assertEqual(tree[1].parameters, 'int v')
        self.assertTrue(isinstance(tree[1], CTorExpression))