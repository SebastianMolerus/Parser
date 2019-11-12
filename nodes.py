
class Node:
    def __init__(self, name):
        self._name = name
        self._childNodes = []

    def addChild(self, node):
        self._childNodes.append(node)
        print "Object: %s -> has new node %s" % (self._name, node._name)

    @property
    def name(self):
        return self._name

class classNode(Node):
    def __init__(self, name):
        Node.__init__(self, name)
        print "Class node (%s) created." % (self._name) 

class namespaceNode(Node):
    def __init__(self, name):
        Node.__init__(self, name)
        print "Namespace node (%s) created." % (self._name) 
    
class functionNode(Node):
    def __init__(self, function_name, returns = "", params=""):
        Node.__init__(self, function_name)
        self._returns = returns
        self._params = params
        print "Method node (%s) created." % (self._name) 

    @property
    def params(self):
        return self._params
    
    @params.setter
    def params(self, params):
        self._params = params
        print "Method %s with params : (%s)" % (self._name, self._params)

    @property
    def returns(self):
        return self._returns

    @returns.setter
    def returns(self, returns):
        self._returns = returns
        print "Method %s returns %s" % (self._name, self._returns)

class ctorNode(Node):
    def __init__(self, name, initParams):
        Node.__init__(self, name)
        self._initParams = initParams
        print "Ctor node (%s) created." % (self._name)

class CopyConstructorNode(ctorNode):
    def __init__(self, name, initParams, returns):
        ctorNode.__init__(self, name, initParams)
        self._returns = returns
        print "CopyCtor node (%s) created." % (self._name)

