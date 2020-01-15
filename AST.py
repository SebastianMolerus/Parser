from TokenStream import TokenStream
from TokenReader import TokenType
from TokenReader import Token

class AST:
    def __init__(self, tokenStream):
        self.tokenStream = tokenStream

    def buildTree(self, context = None):

        while self.tokenStream.next():

            CurrentToken = self.tokenStream.current

            if CurrentToken.type == TokenType._eof:
                return CurrentToken

            if CurrentToken.type == TokenType._namespace:
                return self.ParseNamespace(context)

            if CurrentToken.type == TokenType._class:
                return self.ParseClass(context)

    def _currentContent(self):
        return self.tokenStream.currentToken.content

    def _currentType(self):
        return self.tokenStream.currentToken.type

# -----------------------------------------------------------------
# namespace parsing
    def ParseNamespace(self, context):

        # we have "namespace" already
        # go next
        self.tokenStream.next()

        # consume identifier
        if self._currentType() != TokenType._identifier:
            raise Exception("Identifier expected after namespace keyword")

        # we have identifier
        namespaceIdentifier = self._currentContent()

        self.tokenStream.next()

        # opening bracket consumed
        if self._currentType() != TokenType._opening_bracket:
            raise Exception("No opening brackets after namespace identifier")

        # currentToken == token.opening_brackets

        self.tokenStream.next()

        # we have something...

        # ...maybe empty namespace
        if self._currentType() == TokenType._closing_bracket:
            return namespaceIdentifier
  
        # ...maybe eof
        if self._currentType() == TokenType._eof:
            raise Exception("EOF before namespace closing bracket")

        # ...continue till closing bracket
        while self._currentType() != TokenType._closing_bracket:
            
            #parse more...

            self.tokenStream.next()

        # we have closing bracket
        return # TODO

# -----------------------------------------------------------------
# class parsing
    def ParseClass(self, context):
        # we have class already
        # go next
        self.tokenStream.next()

        # consume identifier
        if self._currentType() != TokenType._identifier:
            raise Exception("Identifier expected after class keyword")

        # we have identifier
        className = self._currentContent()

        self.tokenStream.next()

        # we have something...

        # ...maybe forwarded class
        if self._currentType() == TokenType._semicolon:
            pass # TODO


        # ...move after opening bracket
        while self._currentType() != TokenType._opening_bracket:
            self.tokenStream.next()

        # currentToken == token.opening_brackets

        self.tokenStream.next()

        # we have something...

        # ... maybe empty class
        if self._currentType() == TokenType._closing_bracket:
            pass # TODO

        # ... maybe eof
        if self._currentType() == TokenType._eof:
            raise Exception("EOF before class closing bracket")

        # ...continue till closing bracket
        while self._currentType() != TokenType._closing_bracket:

            #parse more...

            self.tokenStream.next()

        # we have closing bracket
        return # TODO

        