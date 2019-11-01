
class Node:
    def __init__(self, name):
        self.name = name
        self.childNodes = []

    def addChild(self, node):
        self.childNodes.append(node)

class classNode(Node):
    pass

class forwardedClassNode(Node):
    pass

class namespaceNode(Node):
    pass
    
class methodNode(Node):
    pass
    
