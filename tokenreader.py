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
            return Token(TokenType.namespace_, 'namespace')

        if self._identifier == r"class":
            return Token(TokenType.class_, 'class')

        if self._identifier == r"struct":
            return Token(TokenType.struct_, 'struct')

        if self._identifier == r";":
            return Token(TokenType.semicolon_, ';')

        if self._identifier == r":":
            return Token(TokenType.colon_, ':')

        if self._identifier == r"{":
            return Token(TokenType.opening_bracket_, '{')

        if self._identifier == r"}":
            return Token(TokenType.closing_bracket_, '}')

        if self._identifier == r"(":
            return Token(TokenType.params_begin_, '(')

        if self._identifier == r")":
            return Token(TokenType.params_end_, ')')

        if self._identifier == r"public":
            return Token(TokenType.public_, 'public')

        if self._identifier == r"private":
            return Token(TokenType.private_, 'private')

        if self._identifier == r"protected":
            return Token(TokenType.protected_, 'protected')

        if self._identifier == r",":
            return Token(TokenType.comma_, ',')

        if self._identifier == r"*":
            return Token(TokenType.star_, '*')
            
        if self._identifier == r"&":
            return Token(TokenType.ref_, '&')

        if self._identifier == r"~":
            return Token(TokenType.tilde_, '~')

        if self._identifier == r"const":
            return Token(TokenType.const_, 'const')

        if self._identifier == r"=":
            return Token(TokenType.equal_, '=')

        if self._identifier == r"typedef":
            return Token(TokenType.typedef_, 'typedef')

        if self._identifier == r"typename":
            return Token(TokenType.typename_, 'typename')

        if self._identifier == r"virtual":
            return Token(TokenType.virtual_, 'virtual')

        if self._identifier == r"friend":
            return Token(TokenType.friend_, 'friend')

        if self._identifier == r"template":
            return Token(TokenType.template_, 'template')

        if self._identifier == r"operator":
            return Token(TokenType.operator_, 'operator')

        if self._identifier == r"e0f":
            return Token(TokenType.eof_)

        return Token(TokenType.identifier_, self._identifier)