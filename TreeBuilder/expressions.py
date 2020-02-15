from nodes import Node
from tokrdr import TokenType


class Expression(object, Node):
    def __init__(self, identifier):
        self.identifier = identifier
        Node.__init__(self)

    def _print_all(self, indent = 0):

        z = chr(192)        # \
        m = chr(196) * 3    # ---
        size_of_special_chars = len(z) + len(m)

        s = (indent - (indent * size_of_special_chars)) * ' ' + str(type(self)) + self.identifier
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
        return self.identifier == expr.identifier and isinstance(expr, type(self))

    
class ClassExpression(Expression):
    def __init__(self, identifier):
        Expression.__init__(self, identifier)
        self._currentScope = TokenType.private_
        self._isFriendInside = False

    def _set_scope_from_scope_token(self, scope_token):
        '''Sets current scope only if given token is about scope.'''
        if scope_token == TokenType.public_ or \
           scope_token == TokenType.private_ or \
           scope_token == TokenType.protected_:
            self._currentScope = scope_token

    def _friend_inside_spotted(self):
        self._isFriendInside = True

    def is_friend_inside(self):
        return self._isFriendInside

    def get_current_scope(self):
        return self._currentScope


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
        self._parameters = parameters

    def __eq__(self, expr):
        return Expression.__eq__(self, expr) and self._parameters == expr._parameters


class DTorExpression(Expression):
    def __init__(self, identifier):
        Expression.__init__(self, identifier)


class OperatorExpression(Expression):
    def __init__(self, identifier, parameters, returns):
        Expression.__init__(self, identifier)
        self._parameters = parameters
        self._returns = returns
