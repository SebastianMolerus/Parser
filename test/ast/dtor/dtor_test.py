import unittest
from expressions import *
from ast import *

class Test_AstDtor(unittest.TestCase):


    def test_DtorSimpleNotImplemented(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            void ~A();
        };
        """).build_ast()

        self.assertEqual(len(tree),2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertEqual(tree[1], DTorExpression('A'))