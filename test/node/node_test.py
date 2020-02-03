import unittest

from nodes import *

class Test_Node(unittest.TestCase):


    def test_Root(self):
        grandFather = Node()
        father = Node()
        child = Node()

        grandFather.attach(father)
        father.attach(child)

        self.assertEqual(child.get_root(), grandFather)
        self.assertEqual(father.get_root(), grandFather)
        self.assertEqual(grandFather.get_root(), grandFather)

    
    def test_Father(self):
        grandFather = Node()
        father = Node()
        child = Node()

        grandFather.attach(father)
        father.attach(child)

        self.assertEqual(child.get_father(), father)
        self.assertEqual(father.get_father(), grandFather)
        self.assertEqual(grandFather.get_father(), None)