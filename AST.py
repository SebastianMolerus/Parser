from tokenstream import TokenStream

from TokenReader import TokenType
from TokenReader import Token
from TokenReader import TokenReader

from Expressions import NamespaceExpression
from Expressions import ClassExpression
from Expressions import CTorExpression
from Expressions import DTorExpression
from Expressions import Expression

class AbstractTreeBuilder:
    def __init__(self, tokenStream):
        self.tokenStream = tokenStream


    def _try_parse_expression(self, context = None):
        '''Main dispatch method for all expresions.
        
        Every method called from here should return 
        
        Expression if parsed succesfull

        or None
        
        '''

        CurrentToken = self.tokenStream.currentToken

        if CurrentToken.type == TokenType._namespace:
            return self._parse_namespace(context)

        if CurrentToken.type == TokenType._class:
            return self._parse_class(context)

        if CurrentToken.type == TokenType._params_begin:
            return self._parse_params(context)

        if CurrentToken.type == TokenType._tilde:
            return self._parse_dtor(context)

        return None


    def build_ast(self):

        ASTTree = Expression("Root")

        while self.tokenStream.next():
            expr = self._try_parse_expression(ASTTree)
            if expr is not None:
                ASTTree.attach(expr)

        return ASTTree


    def _current_type(self):
        '''Returns current token type eq: TokenType._eof, TokenType._identifier'''
        return self.tokenStream.currentToken.type


    def _current_content(self):
        '''Returns current token content eq: Foo, uint32_t'''
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
            
            # take care of public, prot, private
            parsedClass._set_scope_from_scope_token(self._current_type())

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
        """Used as dispatch method for parsing
        
        everything from TokenType._params_begin
        
        """

        parsedExpr = None

        parsedExpr = self._parse_ctor(context) 
        if parsedExpr:
            return parsedExpr

        parsedExpr = self._parse_method(context) 
        if parsedExpr:
            return parsedExpr
            

    def _parse_ctor(self, context):
        cTorName = context._identifier + "()"
        strParams = ''

        if self._giveMethodName() != context._identifier:
            return None

        if self._current_type() != TokenType._params_begin:
            return None # nie osiagalny kod chyba ze ktos spierdzieli giveMethodName

        self.tokenStream.next()

        while self._current_type() != TokenType._params_end:
            if (self._current_type() == TokenType._ref) or (self._current_type() == TokenType._star):
                pass
            else:
                strParams += ' '
            strParams += self._current_content()
            self.tokenStream.next()
        self.tokenStream.next()

        if self._current_type() == TokenType._semicolon:
            parsedCtor = CTorExpression(cTorName, strParams)
            return parsedCtor
        else:
            while self._current_type() != TokenType._closing_bracket:
                self.tokenStream.next()

        return None


    def _parse_dtor(self, context):
        dTorName = "~" + context._identifier + "()"

        if self._current_type() != TokenType._tilde: 
            return None # Nigdy tu nie wejdziemy

        self.tokenStream.next()
        self.tokenStream.next()

        if self._current_type() != TokenType._params_begin:
            return None # Wedlug mnie tutaj Exception bo jak mamy ~ a tutaj nie bedzie params_begin to bedzie problem
        
        while self._current_type() != TokenType._params_end:
            self.tokenStream.next() # chyba nie ma destruktora z parametrami

        self.tokenStream.next()

        if self._current_type() == TokenType._semicolon:
            parsedDtor = DTorExpression(dTorName)
            return parsedDtor
        else:
            while self._current_type() != TokenType._closing_bracket:
                self.tokenStream.next()

        return None

            
    def _parse_method(self, context):
        pass

    # ja bym pomyslal nad inna nazwa poniewaz to jest dobre do uzycia w wielu miejscach
    # a nie zawsze zwraca Method Name
    # moze np. get identifier from left albo cos takiego ?
    def _giveMethodName(self):
        methodName = ''
        if self._current_type() == TokenType._params_begin:
            self.tokenStream.prev()
            methodName += self._current_content()
            self.tokenStream.next()
        return methodName
