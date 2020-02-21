import unittest
from TreeBuilder.nodes import Node


class Test_Node(unittest.TestCase):
    def test_Root(self):
        grand_father = Node()
        father = Node()
        child = Node()

        grand_father.attach(father)
        father.attach(child)

        self.assertEqual(child.get_root(), grand_father)
        self.assertEqual(father.get_root(), grand_father)
        self.assertEqual(grand_father.get_root(), grand_father)

    def test_Father(self):
        grand_father = Node()
        father = Node()
        child = Node()

        grand_father.attach(father)
        father.attach(child)

        self.assertEqual(child.get_father(), father)
        self.assertEqual(father.get_father(), grand_father)
        self.assertEqual(grand_father.get_father(), None)
