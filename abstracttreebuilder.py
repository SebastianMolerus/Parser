from parsing import Parser
from parsing import Token
from nodes import namespaceNode

class AbstractTreeBuilder:

    def __init__(self, file):
        self.p = Parser(fileName=file)
        self.fifo = []

    def GetNextToken(self):

        if len(self.fifo) > 0:
            self.currentToken = self.fifo.pop(0)
        else:
            self.currentToken = self.p.GetToken()
        return self.currentToken

    def PushToken(self, token):
        self.fifo.insert(0, token)

    def GetNextNode(self):

        self.GetNextToken()
        if self.currentToken == Token.tok_namespace:
            return self.ParseNamespace()
        if self.currentToken == Token.tok_class:
            return self.ParseClass()


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
     
        # we have something not closing
        self.PushToken(self.currentToken)

        # while not closing bracket add more children
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

        # opening bracket consumed
        if self.GetNextToken() != Token.tok_opening_bracket:
            raise Exception("No opening brackets after namespace identifier")

            # TODO


a = AbstractTreeBuilder('a.txt')

node = a.GetNextNode()
node2 = a.GetNextNode()
node3 = a.GetNextNode()

print "end"