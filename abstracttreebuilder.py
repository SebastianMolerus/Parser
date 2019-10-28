from parsing import Parser
from parsing import Token
from nodes import namespaceNode
from nodes import classNode

class AbstractTreeBuilder:

    def __init__(self, file):
        self.p = Parser(fileName=file)
        self.lifo = []
        self.lastNode = None

    def GetNextToken(self):

        if len(self.lifo) > 0:
            self.currentToken = self.lifo.pop(0)
        else:
            self.currentToken = self.p.GetToken()
        return self.currentToken

    def PushToken(self, token):
        self.lifo.insert(0, token)

    def GetNextNode(self):

        if self.GetNextToken() == Token.tok_eof:
            return None

        if self.currentToken == Token.tok_namespace:
            self.lastNode = self.ParseNamespace()
        if self.currentToken == Token.tok_class:
            self.lastNode = self.ParseClass()
        if self.currentToken == Token.tok_struct:
            self.lastNode = self.ParseClass()

        return self.lastNode

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
        self.PushToken(self.currentToken)

        # continue parsing, consume closing bracket
        while self.GetNextToken() != Token.tok_closing_bracket:
            self.PushToken(self.currentToken)
            n.addChild(self.GetNextNode())

        return n



    def ParseClass(self):
        # we have "class" already
        
        # consume identifier
        if self.GetNextToken() != Token.tok_identifier:
            raise Exception("Identifier expected after class keyword")

        # we have identifier
        c = classNode(self.p.identifier)

        

        


a = AbstractTreeBuilder('a.txt')

nodes = []

while a.GetNextNode():
    nodes.append(a.lastNode)

print "end"