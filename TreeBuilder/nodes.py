class Node:
    def __init__(self, father=None):
        self._father = father
        self.children = []
        self.flat_list = []

    def attach(self, node):
        node._father = self
        self.children.append(node)
        self.flat_list = self.get_flat_list(self.children)

    def get_father(self):
        return self._father

    def get_root(self):
        ancestor = self.get_father()
        root = self
        while ancestor:
            root = ancestor
            ancestor = ancestor.get_father()
        return root

    def get_flat_list(self, orig_list):
        f = []

        for item in orig_list:
            f.append(item)
            f.extend(self.get_flat_list(item.children))

        return f

    def __iter__(self):
        return NodeIter(self.flat_list)

    def __len__(self):
        return len(self.flat_list)

    def __getitem__(self, key):
        return self.flat_list[key]


class NodeIter:

    def __init__(self, node_list):
        self._node_list = node_list
        self._currIndex = -1

    def __iter__(self):
        return self

    def __next__(self):
        self._currIndex += 1
        if self._currIndex == len(self._node_list):
            raise StopIteration
        return self._node_list[self._currIndex]

    # something for python 2.x
    next = __next__
