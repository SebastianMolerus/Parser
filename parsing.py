
import enum

class Token(enum.Enum): 
    tok_identifier      =   1,
    tok_namespace       =   2,
    tok_class           =   3,
    tok_struct          =   4,
    tok_semicolon       =   5,    # ;
    tok_colon           =   6,    # :
    tok_opening_bracket =   7,    # {
    tok_closing_bracket =   8,    # }
    tok_params_begin    =   9,    # (
    tok_params_end      =   10,   # )
    tok_underscore      =   11,   # _
    tok_public          =   12,
    tok_private         =   13,
    tok_protected       =   14,
    tok_comma           =   15    # ,

class CharStream:
    def __init__(self):
        self.buffer = []

    def append(self, char):
        self.buffer.append(char)
    
    def pop(self):
        if self.isEmpty():
            raise Exception("Popped empty CharStream")
        self.lastChar = self.buffer.pop(0)
        return self.lastChar

    def isEmpty(self):
        return len(self.buffer) == 0

    def push(self, char):
        self.buffer.insert(0, char)


class Parser:
    def __init__(self, fileName = None, Text = None):
        self.cs = CharStream()

        if Text and fileName:
            raise Exception("Defined two resources of data")

        if Text:
            for i, v in enumerate(Text): 
                self.cs.append(v)
            return
 
        with open(fileName) as fileobj:
            for line in fileobj:  
                for ch in line: 
                    self.cs.append(ch)

    def GetToken(self):

        #spaces
        identifier = ' '
        while identifier.isspace():
            identifier = self.cs.pop()

        #process letters
        while self.cs.lastChar.isalnum():
            if self.cs.pop().isalnum():
                identifier+=self.cs.lastChar
            else:
                self.cs.push(self.cs.lastChar)

        #process comments
        if self.cs.lastChar == '/':
            if self.cs.pop() == '/':
                while self.cs.pop() != '\n':
                    pass
                return self.GetToken()
            else:
                raise Exception("Expected / after /.")

        
        if identifier == r"namespace":
            return Token.tok_namespace
        if identifier == r"class":
            return Token.tok_class
        if identifier == r"struct":
            return Token.tok_struct
        if identifier == r";":
            return Token.tok_semicolon
        if identifier == r":":
            return Token.tok_colon
        if identifier == r"{":
            return Token.tok_opening_bracket
        if identifier == r"}":
            return Token.tok_closing_bracket
        if identifier == r"(":
            return Token.tok_params_begin
        if identifier == r")":
            return Token.tok_params_end
        if identifier == r"_":
            return Token.tok_underscore
        if identifier == r"public":
            return Token.tok_public
        if identifier == r"private":
            return Token.tok_private
        if identifier == r"protected":
            return Token.tok_protected
        if identifier == r",":
            return Token.tok_comma

        return Token.tok_identifier