from token_reader import TokenType


class Expression:
    def __init__(self, identifier):
        self.identifier = identifier
        self.children = []
        self.father = None

    def print_all(self, indent=0):
        z = chr(192)        # \
        m = chr(196) * 3    # ---
        size_of_special_chars = len(z) + len(m)

        s = (indent - (indent * size_of_special_chars)) * ' ' + str(type(self)) + self.identifier
        for c in self.children:
            s += '\n'
            s += indent * ' '
            s += z
            s += m
            s += c.print_all(indent + size_of_special_chars)

        return s

    def __str__(self):
        return self.print_all()

    def add_child(self, child):
        child.father = self
        self.children.append(child)

    def __eq__(self, expr):
        return self.identifier == expr.identifier and isinstance(expr, type(self))

    def __len__(self):
        return len(self.__flat_list(self.children))

    def __getitem__(self, item):
        return self.__flat_list(self.children)[item]

    def __flat_list(self, orig_list):
        f = []
        for item in orig_list:
            f.append(item)
            f.extend(self.__flat_list(item.children))
        return f

    
class ClassExpression(Expression):
    def __init__(self, identifier):
        Expression.__init__(self, identifier)
        self._current_scope = TokenType.private_
        self._is_friend_inside = False

    def set_scope(self, scope_token):
        if scope_token == TokenType.public_ or \
           scope_token == TokenType.private_ or \
           scope_token == TokenType.protected_:
            self._current_scope = scope_token

    def set_friend_inside(self):
        self._is_friend_inside = True

    def is_friend_inside(self):
        return self._is_friend_inside

    def get_current_scope(self):
        return self._current_scope


class NamespaceExpression(Expression):
    def __init__(self, identifier):
        Expression.__init__(self, identifier)


class MethodExpression(Expression):
    def __init__(self, identifier, parameters, return_part, is_const):
        Expression.__init__(self, identifier)
        self.parameters = parameters
        self.return_part = return_part
        self.is_const = is_const


class CTorExpression(Expression):
    def __init__(self, identifier, parameters, implementation = None):
        Expression.__init__(self, identifier)
        self.parameters = parameters
        self.implementation = implementation

    def __eq__(self, expr):
        return Expression.__eq__(self, expr) and self.parameters == expr.parameters


class DTorExpression(Expression):
    def __init__(self, identifier):
        Expression.__init__(self, identifier)


class OperatorExpression(Expression):
    def __init__(self, identifier, parameters, return_part):
        Expression.__init__(self, identifier)
        self.parameters = parameters
        self.return_part = return_part


class FunctionExpression(Expression):
    def __init__(self, identifier, parameters, return_part):
        Expression.__init__(self, identifier)
        self.parameters = parameters
