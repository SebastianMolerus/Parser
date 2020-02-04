import unittest
from expressions import *
from ast import *


class Test_AstNamespace(unittest.TestCase):


    def test_OneSimpleNamespace(self):
        tree = AbstractTreeBuilder(source_code=r"namespace N1{}").build_ast()

        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0], NamespaceExpression('N1'))


    def test_NamespaceWithNestedClass(self):
        tree = AbstractTreeBuilder(source_code=r"namespace N1{class C1{};};").build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], NamespaceExpression('N1'))
        self.assertEqual(tree[1], ClassExpression('C1'))
        self.assertEqual(tree[1].get_father(), tree[0])

       
    def test_NamespaceWithNestedNamespace(self):
        tree = AbstractTreeBuilder(source_code="""
        namespace N1{
            namespace N2{}
        }
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], NamespaceExpression('N1'))
        self.assertEqual(tree[1], NamespaceExpression('N2'))