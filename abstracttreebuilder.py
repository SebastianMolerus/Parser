from parsing import Parser
from parsing import Token
from nodes import namespaceNode
from nodes import classNode
from nodes import forwardedClassNode

class AbstractTreeBuilder:

    def __init__(self, parser):
        self.p = parser
        self.lifo = []
        self.lastNode = None
        self.currentToken = None


    @classmethod
    def FromTxt(cls, txt):
        p = Parser(Text=txt)
        return cls(p)

    @classmethod
    def FromFile(cls, file):
        p = Parser(fileName=file)
        return cls(p)

    def GetNextToken(self):

        if len(self.lifo) > 0:
            self.currentToken = self.lifo.pop(0)
        else:
            self.currentToken = self.p.GetToken()
        return self.currentToken

    def ReturnToken(self, token):
        self.lifo.insert(0, token)


    def GetNextNode(self):

        self.lastNode = None

        while self.GetNextToken() != Token.tok_eof:

            if self.currentToken == Token.tok_semicolon:
                return self.GetNextNode()

            if self.currentToken == Token.tok_closing_bracket:
                self.ReturnToken(self.currentToken)
                return None
            
            if self.currentToken == Token.tok_class:
                break
            if self.currentToken == Token.tok_namespace:
                break
            self.lastNode = self.TryGetMethod()
            if self.lastNode is not None:
                return self.lastNode

        if self.currentToken == Token.tok_namespace:
            self.lastNode = self.ParseNamespace()
        if self.currentToken == Token.tok_class:
            self.lastNode = self.ParseClass()


        return self.lastNode

    def TryGetMethod(self):

        token_buff = []
        while self.GetNextToken() != Token.tok_eof:

            if self.currentToken == Token.tok_semicolon:
                break

            token_buff.insert(0, [self.currentToken, self.p.identifier])

        for token,ident in token_buff:
            # we have params
            if token == Token.tok_params_begin:
                full_method = ""
                for token,ident in token_buff:
                    full_method+=ident

                print full_method

            

        
        for token, ident in token_buff:
            self.ReturnToken(token)
        return None


    def ParseNamespace(self):

        # we have "namespace" already
        
        # consume identifier
        if self.GetNextToken() != Token.tok_identifier:
            raise Exception("Identifier expected after namespace keyword")

        # we have identifier
        n = namespaceNode(self.p.identifier)

        # opening bracket consumed
        if self.GetNextToken() != Token.tok_opening_bracket:
            raise Exception("No opening brackets after namespace identifier")

        # currentToken == token.opening_brackets

        # empty namespace
        if self.GetNextToken() == Token.tok_closing_bracket:
            return n
     
        # we have something
        # check for eof
        if self.currentToken == Token.tok_eof:
            raise Exception("EOF before namespace closing bracket")

        # return something to stream
        self.ReturnToken(self.currentToken)

        # continue parsing, consume closing bracket
        while self.GetNextToken() != Token.tok_closing_bracket:
            self.ReturnToken(self.currentToken)
            n.addChild(self.GetNextNode())

        if None in n.childNodes:
            n.childNodes.remove(None)

        return n



    def ParseClass(self):
        # we have "class/struct" already
        
        # consume identifier
        if self.GetNextToken() != Token.tok_identifier:
            raise Exception("Identifier expected after class keyword")

        # we have identifier
        objectName = self.p.identifier

        # forwarded class
        if self.GetNextToken() == Token.tok_semicolon:
            return forwardedClassNode(objectName)

        # not forwarded class
        # move after opening bracket
        while self.currentToken != Token.tok_opening_bracket:
            self.GetNextToken()

        # currentToken == token.opening_brackets

        # empty class
        if self.GetNextToken() == Token.tok_closing_bracket:
            return classNode(objectName)

        # we have something
        # check for eof
        if self.currentToken == Token.tok_eof:
            raise Exception("EOF before class closing bracket")

        # return something to stream
        self.ReturnToken(self.currentToken)

        c = classNode(objectName)
        # continue parsing, consume closing brackets
        while self.GetNextToken() != Token.tok_closing_bracket:
            self.ReturnToken(self.currentToken)
            c.addChild(self.GetNextNode())

        if None in c.childNodes:
            c.childNodes.remove(None)

        return c

        