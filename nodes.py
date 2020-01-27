class Node:
    def __init__(self, father = None):
        self._children = []
        self._father = father

    def Attach(self, node):
        self._children.append(node)
        node._father = self

    def GetFather(self):
        return self._father

    def GetRoot(self):
        ancestor = self.GetFather()
        root = None
        while ancestor:
            root = ancestor
            ancestor = ancestor.GetFather()
        return root
