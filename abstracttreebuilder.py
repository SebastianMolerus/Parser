from parsing import Parser
from parsing import Token

class AbstractTreeBuilder:

    def ProcessNamespace(self):

        if self.p.GetToken() != Token.tok_identifier:
            print "Expected identifier after namespace declaration."

        namespace_identifier = self.p.identifier

        if self.p.GetToken() != Token.tok_opening_bracket:
            print "Expected { after namespace identifier."

        self.Scanner()

        if self.p.GetToken() != Token.tok_closing_bracket:
            print "Expected } after namespace end."



    def Initialize(self, file):
        self.p = Parser(fileName=file)


    def Scanner(self, token):

        if token==Token.tok_namespace:
            ProcessNamespace()


    def MainWork(self):
        while True:
            Scanner(self, self.p.GetToken())