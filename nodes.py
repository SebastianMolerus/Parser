
class Node:
    def __init__(self, name):
        self.name = name
        self.childNodes = []

    def addChild(self, node):
        self.childNodes.append(node)
        print "Object: %s -> has new node %s" % (self.name, node.name)


class classNode(Node):
    def __init__(self, name):
        Node.__init__(self, name)
        print "Class node (%s) created." % (self.name) 

class namespaceNode(Node):
    def __init__(self, name):
        Node.__init__(self, name)
        print "Namespace node (%s) created." % (self.name) 

