from parsing import Parser
from parsing import Token

import tokenstream

import nodes


class AbstractTreeBuilder:

    def __init__(self, token_stream):
        self._stream = token_stream

    def GetNextNode(self):

        while self._stream.next():
            pass  

    def TryParseSomething(self, ContextNode = None):
    
        #    |
        #   i();
        stream = self._stream
        stream.save()

        # go backward for identifier
        stream.prev()
        #   |
        #   i();

        identifier = stream.current.content

        stream.next()
        #    |
        #   i();

        if ContextNode:
            # method in class

            # Ctor


        else:
            # function
       

        return None


       


    def ParseNamespace(self):

        # we have "namespace" already
        
        # consume identifier
        if self._GetExpression().token() != Token.tok_identifier:
            raise Exception("Identifier expected after namespace keyword")

        # we have identifier
        n = namespaceNode(self._currentExpression.identifier())

        # opening bracket consumed
        if self._GetExpression().token() != Token.tok_opening_bracket:
            raise Exception("No opening brackets after namespace identifier")

        # currentToken == token.opening_brackets

        # empty namespace
        if self._GetExpression().token() == Token.tok_closing_bracket:
            return n
     
        # we have something
        # check for eof
        if self._currentExpression.token() == Token.tok_eof:
            raise Exception("EOF before namespace closing bracket")

        # return something to stream
        self._ReturnExpr(self._currentExpression)

        # continue parsing, consume closing bracket
        while self._GetExpression().token() != Token.tok_closing_bracket:
            self._ReturnExpr(self._currentExpression)
            n.addChild(self.GetNextNode())

        if None in n.childNodes:
            n.childNodes.remove(None)

        return n

    def ParseClass(self):
        # we have "class/struct" already
        
        # consume identifier
        if self._GetExpression().token() != Token.tok_identifier:
            raise Exception("Identifier expected after class keyword")

        # we have identifier
        objectName = self._currentExpression.identifier()

        # forwarded class
        if self._GetExpression().token() == Token.tok_semicolon:
            return forwardedClassNode(objectName)

        # not forwarded class
        # move after opening bracket
        while self._currentExpression.token() != Token.tok_opening_bracket:
            self._GetExpression()

        # currentToken == token.opening_brackets

        # empty class
        if self._GetExpression().token() == Token.tok_closing_bracket:
            if self._GetExpression().token() != Token.tok_semicolon:
                raise Exception("Expecting ; after class ending bracket") # consume ;
            return classNode(objectName)

        # we have something
        # check for eof
        if self._currentExpression.token() == Token.tok_eof:
            raise Exception("EOF before class closing bracket")

        # return something to stream
        self._ReturnExpr(self._currentExpression)

        c = classNode(objectName)
        # continue parsing, consume closing brackets
        while self._GetExpression().token() != Token.tok_closing_bracket:
            self._ReturnExpr(self._currentExpression)
            c.addChild(self.GetNextNode())

        if self._GetExpression().token() != Token.tok_semicolon:
                raise Exception("Expecting ; after class ending bracket") # consume ;

        if None in c.childNodes:
            c.childNodes.remove(None)

        return c

        