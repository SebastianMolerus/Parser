from token_ import TokenType
from token_ import Token
from preproc import Preproc


class TokenReader:
    """Class used for getting tokens from file or text. """

    def __init__(self, file = None, text = None, preproc = None):
        """ Initialize with file or text.

        Args:
            file:     path to file to read tokens from.

            text:     string to read tokens from.

        """
        self._characters = []

        if text and file:
            raise Exception("Defined two resources of data.")

        if text:
            for char in text: 
                self._characters.append(char)
        else:
            with open(file) as fileobj:
                for line in fileobj:  
                    for char in line: 
                        self._characters.append(char)

        self._characters.append('\n')
        self._characters.append(' ')
        self._characters.append('e')
        self._characters.append('0')
        self._characters.append('f') 
        self._characters.append('$')

        self._preproc = preproc or Preproc(self._characters)
        self._characters = self._preproc.Preprocess()


    def _try_build_alnum_identifier(self):

        if not self._identifier.isalnum():
            return

        while True:
            popped = self._characters.pop(0)
            # for us'_' is treated as alnum.
            if popped.isalnum() or popped == '_':
                self._identifier += popped
            else:
                self._characters.insert(0, popped)
                break


    def get_next_token(self):

        """Method used to get next token.
        
        Last returned Token type is _eof.
                 
        """

        self._identifier = ' '

        while self._identifier.isspace():
            self._identifier = self._characters.pop(0)

        self._try_build_alnum_identifier()

        if self._identifier == r"namespace":
            return Token(TokenType._namespace, 'namespace')

        if self._identifier == r"class":
            return Token(TokenType._class, 'class')

        if self._identifier == r"struct":
            return Token(TokenType._struct, 'struct')

        if self._identifier == r";":
            return Token(TokenType._semicolon, ';')

        if self._identifier == r":":
            return Token(TokenType._colon, ':')

        if self._identifier == r"{":
            return Token(TokenType._opening_bracket, '{')

        if self._identifier == r"}":
            return Token(TokenType._closing_bracket, '}')

        if self._identifier == r"(":
            return Token(TokenType._params_begin, '(')

        if self._identifier == r")":
            return Token(TokenType._params_end, ')')

        if self._identifier == r"public":
            return Token(TokenType._public, 'public')

        if self._identifier == r"private":
            return Token(TokenType._private, 'private')

        if self._identifier == r"protected":
            return Token(TokenType._protected, 'protected')

        if self._identifier == r",":
            return Token(TokenType._comma, ',')

        if self._identifier == r"*":
            return Token(TokenType._star, '*')
            
        if self._identifier == r"&":
            return Token(TokenType._ref, '&')

        if self._identifier == r"~":
            return Token(TokenType._tilde, '~')

        if self._identifier == r"const":
            return Token(TokenType._const, 'const')

        if self._identifier == r"=":
            return Token(TokenType._equal, '=')

        if self._identifier == r"typedef":
            return Token(TokenType._typedef, 'typedef')

        if self._identifier == r"typename":
            return Token(TokenType._typename, 'typename')

        if self._identifier == r"virtual":
            return Token(TokenType._virtual, 'virtual')

        if self._identifier == r"friend":
            return Token(TokenType._friend, 'friend')

        if self._identifier == r"template":
            return Token(TokenType._template, 'template')

        if self._identifier == r"operator":
            return Token(TokenType._operator, 'operator')

        if self._identifier == r"e0f":
            return Token(TokenType._eof)

        return Token(TokenType._identifier, self._identifier)