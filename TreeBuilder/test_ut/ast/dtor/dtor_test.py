import unittest
from TreeBuilder.expressions import ClassExpression
from TreeBuilder.expressions import DTorExpression
from TreeBuilder.parsing import build_ast
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream


class Test_AstDtor(unittest.TestCase):

    def test_PublicDtorNotImplemented(self):
        tr = TokenReader(source_code="""
        class A{
            public:
            void ~A();
        };
        """)

        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree),2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertEqual(tree[1], DTorExpression('A'))

    def test_PublicDtorImplemented(self):
        tr = TokenReader(source_code="""
        class A{
            public:
            void ~A(){ 
                del ptr
            }
            private:
            int *ptr;
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree),1)
        self.assertEqual(tree[0], ClassExpression('A'))

    def test_PrivateDtorNotImplemented(self):
        tr = TokenReader(source_code="""
        class A{
            private:
            void ~A();
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0], ClassExpression('A'))

    def test_PublicDtorNotImplementedWithGarbageComments(self):
        tr = TokenReader(source_code="""
        class A{
            //Public
            public:
            /* Destructor 
                void ~A();
            */
            void ~A(); //Destructor
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree),2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertEqual(tree[1], DTorExpression('A'))

    def test_NoDtor(self):
        tr = TokenReader(source_code="""
        class A{
            //Public
            public:
            /* Destructor 
                void ~A();
            */
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0], ClassExpression('A'))
