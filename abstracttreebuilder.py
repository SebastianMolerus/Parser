from parsing import Parser
from parsing import Token
from nodes import namespaceNode
from nodes import classNode
from nodes import forwardedClassNode
from nodes import functionNode

class AbstractTreeBuilder:

    def __init__(self, parser):
        self._p = parser
        self._tokenBuffer = []
        self._currentToken = None
        self._lastNode = None

    @classmethod
    def FromTxt(cls, txt):
        _p = Parser(Text=txt)
        return cls(_p)

    @classmethod
    def FromFile(cls, file):
        _p = Parser(fileName=file)
        return cls(_p)

    def _GetNextToken(self):

        if len(self._tokenBuffer) > 0:
            self._currentToken = self._tokenBuffer.pop(0)
        else:
            self._currentToken = self._p.GetToken()
        return self._currentToken

    def _ReturnToken(self, token):
        self._tokenBuffer.insert(0, token)


    def GetNextNode(self):

        while self._GetNextToken() != Token.tok_eof:      

            if self._currentToken == Token.tok_class:
                self._lastNode =  self.ParseClass()
                return self._lastNode
            if self._currentToken == Token.tok_namespace:
                self._lastNode = self.ParseNamespace()
                return self._lastNode

            self._lastNode = self.TryParseFunction()
            if self._lastNode is not None:
                return self._lastNode

        return None


    def TryParseFunction(self):
        pass

    def ParseNamespace(self):

        # we have "namespace" already
        
        # consume identifier
        if self._GetNextToken() != Token.tok_identifier:
            raise Exception("Identifier expected after namespace keyword")

        # we have identifier
        n = namespaceNode(self._p.identifier)

        # opening bracket consumed
        if self._GetNextToken() != Token.tok_opening_bracket:
            raise Exception("No opening brackets after namespace identifier")

        # currentToken == token.opening_brackets

        # empty namespace
        if self._GetNextToken() == Token.tok_closing_bracket:
            return n
     
        # we have something
        # check for eof
        if self._currentToken == Token.tok_eof:
            raise Exception("EOF before namespace closing bracket")

        # return something to stream
        self._ReturnToken(self._currentToken)

        # continue parsing, consume closing bracket
        while self._GetNextToken() != Token.tok_closing_bracket:
            self._ReturnToken(self._currentToken)
            n.addChild(self.GetNextNode())

        if None in n.childNodes:
            n.childNodes.remove(None)

        return n

    def ParseClass(self):
        # we have "class/struct" already
        
        # consume identifier
        if self._GetNextToken() != Token.tok_identifier:
            raise Exception("Identifier expected after class keyword")

        # we have identifier
        objectName = self._p.identifier

        # forwarded class
        if self._GetNextToken() == Token.tok_semicolon:
            return forwardedClassNode(objectName)

        # not forwarded class
        # move after opening bracket
        while self._currentToken != Token.tok_opening_bracket:
            self._GetNextToken()

        # currentToken == token.opening_brackets

        # empty class
        if self._GetNextToken() == Token.tok_closing_bracket:
            if self._GetNextToken() != Token.tok_semicolon:
                raise Exception("Expecting ; after class ending bracket") # consume ;
            return classNode(objectName)

        # we have something
        # check for eof
        if self._currentToken == Token.tok_eof:
            raise Exception("EOF before class closing bracket")

        # return something to stream
        self._ReturnToken(self._currentToken)

        c = classNode(objectName)
        # continue parsing, consume closing brackets
        while self._GetNextToken() != Token.tok_closing_bracket:
            self._ReturnToken(self._currentToken)
            c.addChild(self.GetNextNode())

        if self._GetNextToken() != Token.tok_semicolon:
                raise Exception("Expecting ; after class ending bracket") # consume ;

        if None in c.childNodes:
            c.childNodes.remove(None)

        return c

        