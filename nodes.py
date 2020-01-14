class Node:
    def __init__(self):
        self._children = []

    def Attach(self, node):
        self._children.append(node)
