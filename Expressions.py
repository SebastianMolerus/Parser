from Nodes import Node

class Expression(object, Node):
    def __init__(self, identifier):
        self._identifier = identifier
        Node.__init__(self)


    def _print_all(self, indent = 0):

        z = chr(192)        # \
        m = chr(196) * 3    # ---
        size_of_special_chars = len(z) + len(m)

        s =  (indent - (indent* size_of_special_chars)) * ' ' + self._identifier
        for c in self._children:
            s += '\n'
            s += indent * ' '
            s += z
            s += m
            s += c._print_all(indent + size_of_special_chars)
        
        return s


    def __str__(self):
        return self._print_all()
    

class ClassExpression(Expression):
    def __init__(self, identifier):
        Expression.__init__(self, identifier)


class NamespaceExpression(Expression):
    def __init__(self, identifier):
        Expression.__init__(self, identifier)


class MethodExpression(Expression):
    def __init__(self, identifier, parameters, returns, const = False):
        Expression.__init__(identifier)


