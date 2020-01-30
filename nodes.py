class Node:

    def __init__(self, father = None):
        self._father = father
        self._children = []
        self._flat_list = []


    def attach(self, node):
        node._father = self
        self._children.append(node)
        self._flat_list = self._get_flat_list(self._children)
    

    def get_father(self):
        return self._father


    def get_root(self):
        ancestor = self.get_father()
        root = None
        while ancestor:
            root = ancestor
            ancestor = ancestor.get_father()
        return root


    def _get_flat_list(self, l):
        '''Returns one flat list contains all elements to easy iterate.'''
        f = []

        for item in l:
            f.append(item)
            f.extend(self._get_flat_list(item._children))

        return f


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








