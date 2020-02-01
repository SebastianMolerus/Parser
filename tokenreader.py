import enum


class TokenType(enum.Enum): 
    _identifier      =   1,
    _namespace       =   2,
    _class           =   3,
    _struct          =   4,
    _semicolon       =   5,     # ;
    _colon           =   6,     # :
    _opening_bracket =   7,     # {
    _closing_bracket =   8,     # }
    _params_begin    =   9,     # (
    _params_end      =   10,    # )
    _public          =   11,
    _private         =   12,
    _protected       =   13,
    _comma           =   14,    # ,
    _eof             =   15,
    _ref             =   16,    # &,
    _star            =   17,    # *
    _preproc         =   18,    # #
    _tilde           =   19,    # ~
    _const           =   20,
    _equal           =   21


class CharStream:
    def __init__(self):
        self.buffer = []
        self.lastChar = ''

    def append(self, char):
        self.buffer.append(char)
    
    def pop(self):
        if self.is_empty():
            raise Exception("Pop on empty CharStream")
        self.lastChar = self.buffer.pop(0)
        return self.lastChar

    def is_empty(self):
        return len(self.buffer) == 0

    def push(self, char):
        self.buffer.insert(0, char)

    def is_alnum(self):
        """For our purposes _ is treated as alphanumerical for uint_32
           ':' for Foo::Bar"""
        return (self.lastChar.isalnum() or \
                self.lastChar == '_')


class Token:
    def __init__(self, type, content = ""):
        self._type = type
        self._content = content

    @property
    def type(self):
        '''Returns token type eq: TokenType._eof, TokenType._identifier'''
        return self._type

    @property
    def content(self):
        return self._content


class TokenReader:
    """Class used for getting tokens from file or text. """

    def __init__(self, fileName = None, text = None):
        """ Initialize with fileName or text, not both.

        Args:
            fileName: path to file to read tokens from.

            text:     cpp code to read tokens from.

        """
        self.CharStream = CharStream()

        if text and fileName:
            raise Exception("Defined two resources of data.")

        if text:
            for char in text: 
                self.CharStream.append(char)
            self.CharStream.append('\n')
            self.CharStream.append(' ')
            self.CharStream.append('e')
            self.CharStream.append('0')
            self.CharStream.append('f') 
            self.CharStream.append('$')
            return
 
        with open(fileName) as fileobj:
            for line in fileobj:  
                for char in line: 
                    self.CharStream.append(char)
            self.CharStream.append('\n')
            self.CharStream.append(' ')
            self.CharStream.append('e')
            self.CharStream.append('0')
            self.CharStream.append('f')
            self.CharStream.append('$')


    def get_next_token(self):
        """Method used to get next token.
        
        returns: Token with corresponding type and content.
                 Last returned Token type is _eof.
                 
        """

        self.identifier = ' '

        # always take one token, continue if it is a space
        while self.identifier.isspace():
            self.identifier = self.CharStream.pop()

        # process alnums 
        while self.CharStream.is_alnum():
            self.CharStream.pop()
            if self.CharStream.is_alnum():
                self.identifier+=self.CharStream.lastChar
            else:
                self.CharStream.push(self.CharStream.lastChar)

        #ignore comments
        if self.CharStream.lastChar == '/':
            if self.CharStream.pop() == '/':
                while self.CharStream.pop() != '\n':
                    pass
                return self.get_next_token()
            else:
                raise Exception("Expected / after /.")

        #ignore preproc directives, friends
        if self.CharStream.lastChar == '#' or self.identifier == 'friend':
            while self.CharStream.pop() != '\n':
                pass
            return self.get_next_token()
    
        if self.identifier == r"namespace":
            return Token(TokenType._namespace, "namespace")
        if self.identifier == r"class":
            return Token(TokenType._class, "class")
        if self.identifier == r"struct":
            return Token(TokenType._struct, "struct")
        if self.identifier == r";":
            return Token(TokenType._semicolon, ";")
        if self.identifier == r":":
            return Token(TokenType._colon, ":")
        if self.identifier == r"{":
            return Token(TokenType._opening_bracket, "{")
        if self.identifier == r"}":
            return Token(TokenType._closing_bracket, "}")
        if self.identifier == r"(":
            return Token(TokenType._params_begin, "(")
        if self.identifier == r")":
            return Token(TokenType._params_end, ")")
        if self.identifier == r"public":
            return Token(TokenType._public, "public")
        if self.identifier == r"private":
            return Token(TokenType._private, "private")
        if self.identifier == r"protected":
            return Token(TokenType._protected, "protected")
        if self.identifier == r",":
            return Token(TokenType._comma, ",")
        if self.identifier == r"*":
            return Token(TokenType._star, "*")
        if self.identifier == r"&":
            return Token(TokenType._ref, "&")
        if self.identifier == r"~":
            return Token(TokenType._tilde, "~")
        if self.identifier == r"const":
            return Token(TokenType._const, "const")
        if self.identifier == r"=":
            return Token(TokenType._equal, "=")

        if self.identifier == r"e0f":
            return Token(TokenType._eof)

        return Token(TokenType._identifier, self.identifier)