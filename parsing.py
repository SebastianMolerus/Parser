
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
    tok_public          =   11,
    tok_private         =   12,
    tok_protected       =   13,
    tok_comma           =   14,    # ,
    tok_eof             =   15,
    tok_ref             =   16,    # &,
    tok_star            =   17,     # *
    tok_preproc         =   18,     # #
    tok_tilde           =   19     # ~

class CharStream:
    def __init__(self):
        self.buffer = []

    def append(self, char):
        self.buffer.append(char)
    
    def pop(self):
        if self.isEmpty():
            raise Exception("Pop on empty CharStream")
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
            self.cs.append('\n')
            self.cs.append(' ')
            self.cs.append('e')
            self.cs.append('0')
            self.cs.append('f')
            self.cs.append('$')
            return
 
        with open(fileName) as fileobj:
            for line in fileobj:  
                for ch in line: 
                    self.cs.append(ch)
            self.cs.append('\n')
            self.cs.append(' ')
            self.cs.append('e')
            self.cs.append('0')
            self.cs.append('f')
            self.cs.append('$')


    def GetToken(self):

        #spaces
        self.identifier = ' '
        while self.identifier.isspace():
            self.identifier = self.cs.pop()

        #process alnums
        while self.cs.lastChar.isalnum() or self.cs.lastChar == r'_':
            if self.cs.pop().isalnum() or self.cs.lastChar == r'_':
                self.identifier+=self.cs.lastChar
            else:
                self.cs.push(self.cs.lastChar)

        #ignore comments
        if self.cs.lastChar == '/':
            if self.cs.pop() == '/':
                while self.cs.pop() != '\n':
                    pass
                return self.GetToken()
            else:
                raise Exception("Expected / after /.")

        #ignore preproc directives, friends
        if self.cs.lastChar == '#' or self.identifier == 'friend':
            while self.cs.pop() != '\n':
                pass
            return self.GetToken()
    
        if self.identifier == r"namespace":
            return Token.tok_namespace
        if self.identifier == r"class":
            return Token.tok_class
        if self.identifier == r"struct":
            return Token.tok_struct
        if self.identifier == r";":
            return Token.tok_semicolon
        if self.identifier == r":":
            return Token.tok_colon
        if self.identifier == r"{":
            return Token.tok_opening_bracket
        if self.identifier == r"}":
            return Token.tok_closing_bracket
        if self.identifier == r"(":
            return Token.tok_params_begin
        if self.identifier == r")":
            return Token.tok_params_end
        if self.identifier == r"public":
            return Token.tok_public
        if self.identifier == r"private":
            return Token.tok_private
        if self.identifier == r"protected":
            return Token.tok_protected
        if self.identifier == r",":
            return Token.tok_comma
        if self.identifier == r"*":
            return Token.tok_star
        if self.identifier == r"&":
            return Token.tok_ref
        if self.identifier == r"~":
            return Token.tok_tilde

        if self.identifier == r"e0f":
            return Token.tok_eof

        return Token.tok_identifier