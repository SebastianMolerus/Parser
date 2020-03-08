import unittest
from TreeBuilder.expressions import NamespaceExpression
from TreeBuilder.expressions import ClassExpression
from TreeBuilder.parsing import build_ast
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream


class Test_AstNamespace(unittest.TestCase):

    def test_OneSimpleNamespace(self):
        tr = TokenReader(source_code=r"namespace N1{}")
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0], NamespaceExpression('N1'))

    def test_NamespaceWithNestedClass(self):
        tr = TokenReader(source_code=r"namespace N1{class C1{};};")
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], NamespaceExpression('N1'))
        self.assertEqual(tree[1], ClassExpression('C1'))
        self.assertEqual(tree[1].get_father(), tree[0])

    def test_NamespaceWithNestedNamespace(self):
        tr = TokenReader(source_code="""
        namespace N1{
            namespace N2{}
        }
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], NamespaceExpression('N1'))
        self.assertEqual(tree[1], NamespaceExpression('N2'))
