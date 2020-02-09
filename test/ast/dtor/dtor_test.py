import unittest
from expressions import *
from ast import *

class Test_AstDtor(unittest.TestCase):

    def test_PublicDtorNotImplemented(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            public:
            void ~A();
        };
        """).build_ast()

        self.assertEqual(len(tree),2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertEqual(tree[1], DTorExpression('A'))

    def test_PublicDtorImplemented(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            public:
            void ~A(){ 
                del ptr
            }
            private:
            int *ptr;
        };
        """).build_ast()

        self.assertEqual(len(tree),1)
        self.assertEqual(tree[0], ClassExpression('A'))

    def test_PrivateDtorNotImplemented(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            private:
            void ~A();
        };
        """).build_ast()

        self.assertEqual(len(tree),1)
        self.assertEqual(tree[0], ClassExpression('A'))

    def test_PublicDtorNotImplementedWithGarbageComments(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            //Public
            public:
            /* Destructor 
                void ~A();
            */
            void ~A(); //Destructor
        };
        """).build_ast()

        self.assertEqual(len(tree),2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertEqual(tree[1], DTorExpression('A'))

    def test_NoDtor(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            //Public
            public:
            /* Destructor 
                void ~A();
            */
        };
        """).build_ast()

        self.assertEqual(len(tree),1)
        self.assertEqual(tree[0], ClassExpression('A'))