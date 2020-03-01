import unittest

from TreeBuilder.atb import AbstractTreeBuilder
from TreeBuilder.expressions import CTorExpression, Expression
from TreeBuilder.expressions import ClassExpression
from TreeBuilder.expressions import NamespaceExpression
from TreeBuilder.tok import TokenType
from TreeBuilder.token_stream import TokenStream
from mock import Mock


class Test_Ctor(unittest.TestCase):


    def test_CtorSimple(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            public:
            A();
        };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertTrue(isinstance(tree[1], CTorExpression))
        self.assertEqual(tree[1].identifier, 'A')

    def test_OnePrivateCtorSimple(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            A();
        };
        """).build_ast()

        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0], ClassExpression('A'))

    def test_TwoCtorsSimplePrivateAndPublic(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            A(A &);
            public:
            A();
        };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertTrue(isinstance(tree[1], CTorExpression))
        self.assertEqual(tree[1].identifier, 'A')

    def test_CtorImplementedMethodSameAsNamespace(self):
        tree = AbstractTreeBuilder(source_code="""
        namespace A{
            void A(){}
        }
        """).build_ast()

        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0], NamespaceExpression('A'))

    def test_CtorWithOneParameter(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{public: A(uint32_t& value1);};
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertEqual(tree[1], CTorExpression('A', 'uint32_t& value1'))

    def test_CtorWithTwoParameters(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{public:A(uint32_t& value1, const uint32_t* value2);};
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertEqual(tree[1], CTorExpression('A', 'uint32_t& value1, const uint32_t* value2'))

    def test_TwoCtorsOneImplementedAnotherNot(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{public:A(){}A(int a);};
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertEqual(tree[1], CTorExpression('A', 'int a'))

    def test_TwoCtorsImplemented(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            public:
            A();
            A(int v);
            };
        """).build_ast()

        self.assertEqual(len(tree), 3)
        self.assertEqual(tree[0], ClassExpression('A'))

        self.assertEqual(tree[1], CTorExpression('A', ''))

        self.assertTrue(isinstance(tree[2], CTorExpression))
        self.assertEqual(tree[2].parameters, 'int v', "Parameters does not match.")
        self.assertEqual(tree[2].identifier, 'A', 'Ctor identifier does not match.')

    def test_CtorWithNewlinedParameters(self):
        tree = AbstractTreeBuilder(source_code="""
        class M{
            public:
            M(int*& val1,
                               SomeOtherType const& val2);
            };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('M'))
        self.assertEqual(tree[1].identifier, 'M')
        self.assertEqual(tree[1].parameters, 'int*& val1, SomeOtherType const& val2')
        self.assertTrue(isinstance(tree[1], CTorExpression))

    def test_CtorNoCtor(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            void Method();
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('Foo'))

    def test_CtorTwoCtorsOneWithGarbageInside(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            Foo()
            {
                Foo* ptr = new Foo();
                delete ptr;
            }

            Foo(int v);
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('Foo'))
        self.assertEqual(tree[1].identifier, 'Foo')
        self.assertEqual(tree[1].parameters, 'int v')
        self.assertTrue(isinstance(tree[1], CTorExpression))

    def test_TwoCopyCtorsPrivateAndPublic(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            private
            A(const A&);
            public:
            A(const A&);
        };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertTrue(isinstance(tree[1], CTorExpression))
        self.assertEqual(tree[1].identifier, 'A')
        self.assertEqual(tree[1].parameters, 'const A&')

    def test_TwoCopyCtorsPrivateAndImplementedPublic(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            private:
            A(const A&);
            public:
            A(const A&) {
                a = A.a;
            }
            private:
            int a;
        };
        """).build_ast()

        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0], ClassExpression('A'))
