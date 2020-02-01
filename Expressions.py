from nodes import Node
from tokenreader import TokenType


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


    def __eq__(self, expr):
        return self._identifier == expr._identifier and isinstance(expr, type(self))

    
class ClassExpression(Expression):
    def __init__(self, identifier):
        Expression.__init__(self, identifier)
        self._currentScope = TokenType._private


    def _set_scope_from_scope_token(self, scope_token):
        '''Sets current scope only if given token is about scope.'''
        if scope_token == TokenType._public or \
           scope_token == TokenType._private or \
           scope_token == TokenType._protected:
            self._currentScope = scope_token


class NamespaceExpression(Expression):
    def __init__(self, identifier):
        Expression.__init__(self, identifier)


class MethodExpression(Expression):
    def __init__(self, identifier, parameters, returns, constness):
        Expression.__init__(self, identifier)
        self._parameters = parameters
        self._returns = returns
        self._constness = constness


class CTorExpression(Expression):
    def __init__(self, identifier, parameters):
        Expression.__init__(self, identifier)
        self.parameters = parameters


    def __eq__(self, expr):
        return Expression.__eq__(self, expr) and self.parameters == expr.parameters


class DTorExpression(Expression):
    def __init__(self, identifier):
        Expression.__init__(self, identifier)
