from TokenStream import TokenStream

from TokenReader import TokenType
from TokenReader import Token
from TokenReader import TokenReader

from Expressions import NamespaceExpression
from Expressions import ClassExpression
from Expressions import Expression

class AbstractTreeBuilder:
    def __init__(self, tokenStream):
        self.tokenStream = tokenStream


    def _try_parse_expression(self, context = None):

        CurrentToken = self.tokenStream.currentToken

        if CurrentToken.type == TokenType._namespace:
            return self._parse_namespace(context)

        if CurrentToken.type == TokenType._class:
            return self._parse_class(context)

        if CurrentToken.type == TokenType._params_begin:
            return self._parse_params(context)

        return None


    def build_ast(self):

        ASTTree = Expression("Root")

        while self.tokenStream.next():
            expr = self._try_parse_expression(ASTTree)
            if expr is not None:
                ASTTree.attach(expr)

        return ASTTree


    def _current_type(self):
        return self.tokenStream.currentToken.type


    def _current_content(self):
        return self.tokenStream.currentToken.content


    def _parse_namespace(self, context):

        # we have "namespace" already
        # go next
        self.tokenStream.next()

        # consume identifier
        if self._current_type() != TokenType._identifier:
            raise Exception("Identifier expected after namespace keyword")

        # we have identifier
        parsed_namespace  = NamespaceExpression(self._current_content())
        
        self.tokenStream.next()

        if self._current_type() != TokenType._opening_bracket:
            raise Exception("No opening brackets after namespace identifier")

        # currentToken == token.opening_brackets

        while self.tokenStream.next():

            # we're done
            if self._current_type() == TokenType._closing_bracket:
                break

            expr = self._try_parse_expression(parsed_namespace)
            if expr is None:
                continue
            print "Node {} added into {}.".format(expr._identifier ,parsed_namespace._identifier)
            parsed_namespace.attach(expr)

        return parsed_namespace


    def _parse_class(self, context):
        # we have class already
        # go next
        self.tokenStream.next()

        # consume identifier
        if self._current_type() != TokenType._identifier:
            raise Exception("Identifier expected after class keyword")

        # we have identifier
        parsedClass = ClassExpression(self._current_content())

        self.tokenStream.next()

        # we have something...

        # ...maybe forwarded class
        if self._current_type() == TokenType._semicolon:
            return None

        # ...move after opening bracket
        while self._current_type() != TokenType._opening_bracket:
            self.tokenStream.next()

        # currentToken == token.opening_brackets

        while self.tokenStream.next():

            # we're done
            if self._current_type() == TokenType._closing_bracket:
                break

            expr = self._try_parse_expression(parsedClass)
            if expr is None:
                continue
            print "Node {} added into {}.".format(expr._identifier ,parsedClass._identifier)
            parsedClass.attach(expr)

        return parsedClass


    def _parse_params(self, context):
        """Used for parsing methods, ctors etc..."""
        pass     