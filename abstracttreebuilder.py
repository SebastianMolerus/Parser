from parsing import Parser
from parsing import Token
from element import element

class AbstractTreeBuilder:

    def __init__(self, file):
        self.p = Parser(fileName=file)

    def GetNextToken(self):
        self.currentToken = self.p.GetToken()
        return self.currentToken

    def ProcessNamespace(self, elem):

        if self.GetNextToken() != Token.tok_identifier:
            print "Expected identifier after namespace declaration."

        identifier_of_namespace = "namespace "
        identifier_of_namespace+=self.p.identifier

        if self.GetNextToken() != Token.tok_opening_bracket:
            print "Expected { after namespace identifier."

        if self.GetNextToken() != Token.tok_closing_bracket:

            # we are in some element already
            if elem:
                newElement = element(identifier_of_namespace)
                elem.addElement(newElement)
                self.Scanner(newElement)
            # this is opening namespace
            else:
                self.lastElement = element(identifier_of_namespace)
                self.Scanner(self.lastElement)

            if self.GetNextToken() != Token.tok_closing_bracket:
                print "Expected } after namespace end."

        else:
            if elem:
                elem.addElement(element(identifier_of_namespace))
            

    def ProcessClass(self, elem):

        if self.GetNextToken() != Token.tok_identifier:
            print "Expected identifier after class declaration."

        identifier_of_class = "class "
        identifier_of_class += self.p.identifier

        # forwarded class
        if self.GetNextToken() == Token.tok_semicolon:
            if elem:
                elem.addElement("forwaded "+ identifier_of_class)
                return
        
        # derived classes
        if self.currentToken == Token.tok_colon:
            while self.GetNextToken() != Token.tok_opening_bracket:
                pass
            self.GetNextToken() # eat opening brackets

        if self.GetNextToken() != Token.tok_closing_bracket:

            # we have a class body
            # we are in some element already
            if elem:
                newElement = element(identifier_of_class)
                elem.addElement(newElement)
                self.Scanner(newElement)
            # this is first class
            else:
                self.lastElement = element(identifier_of_class)
                self.Scanner(self.lastElement)

            if self.GetNextToken() != Token.tok_closing_bracket:
                print "Expected } after namespace end."


        else:
            # we dont have class body
            if elem:
                elem.addElement(element(identifier_of_class))
        


        

    def Scanner(self, elem = None):

        if self.currentToken==Token.tok_namespace:
            self.ProcessNamespace(elem)
        if self.currentToken==Token.tok_class:
            self.ProcessClass(elem)


    def DoWork(self):
        while True:
            self.GetNextToken()
            self.Scanner()
            e = self.lastElement
            print "Iteration"


a = AbstractTreeBuilder("a.txt")
a.DoWork()