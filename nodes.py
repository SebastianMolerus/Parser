
class Node:
    def __init__(self, name):
        self.name = name
        self.childNodes = []

    def addChild(self, node):
        self.childNodes.append(node)

    def getChildren(self):
        return self.childNodes

class classNode(Node):
    pass

class forwardedClassNode(Node):
    pass

class namespaceNode(Node):
    pass
    
class functionNode(Node):
    pass
    
