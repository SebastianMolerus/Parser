
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
    tok_params_end      =   10    # )

class CharStream:
    def __init__(self):
        self.buffer = []

    def append(self, char):
        self.buffer.append(char)
    
    def pop(self):
        if self.isEmpty():
            raise Exception("EOF")
        self.lastChar = self.buffer.pop(0)
        return self.lastChar

    def isEmpty(self):
        return len(self.buffer) == 0

    def push(self, char):
        self.buffer.insert(0, char)


class Parser:
    def __init__(self, fileName):
        self.cs = CharStream()
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
        while self.cs.lastChar.isalpha():
            if self.cs.pop().isalpha():
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

        
        if identifier == "namespace":
            return Token.tok_namespace
        if identifier == "class":
            return Token.tok_class
        if identifier == "struct":
            return Token.tok_struct
        if identifier == ";":
            return Token.tok_semicolon
        if identifier == ":":
            return Token.tok_colon
        if identifier == r"{":
            return Token.tok_opening_bracket
        if identifier == r"}":
            return Token.tok_closing_bracket
        if identifier == r"(":
            return Token.tok_params_begin
        if identifier == r")":
            return Token.tok_params_end

        return Token.tok_identifier



        





try:
    p = Parser('a.txt')
    while True:
        tok = p.GetToken()
except Exception as ex:
    print ex.message
print "End"