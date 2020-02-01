class Node:

    def __init__(self, father = None):
        self._father = father
        self._children = []
        self._flat_list = []
        self._flat_list.append(self)


    def attach(self, node):
        node._father = self
        self._children.append(node)
        self.get_root()._flat_list.append(node)
    

    def get_father(self):
        return self._father


    def get_root(self):
        ancestor = self.get_father()
        root = self
        while ancestor:
            root = ancestor
            ancestor = ancestor.get_father()
        return root


    def __iter__(self):
        return NodeIter(self._flat_list)

    
    def __len__(self):
        return len(self._flat_list)


    def __getitem__(self, key):
        return self._flat_list[key]

        
class NodeIter:
    
    def __init__(self, node_list):
        self._node_list = node_list
        self._currIndex = -1

    
    def __iter__(self):
        return self


    def __next__(self):
        self._currIndex+=1
        if self._currIndex == len(self._node_list):
            raise StopIteration
        return self._node_list[self._currIndex]

    # something for python 2.x
    next = __next__








