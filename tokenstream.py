from TokenReader import Token
from TokenReader import TokenReader
from TokenReader import TokenType

class TokenStream:
    def __init__(self, parser):
        self._cache = []
        self._currentIndex = 0

        # get all tokens till EOF
        while True:
            token = parser.GetToken()
            if token.type == TokenType.tok_eof:
                break
            self._cache.append(token)

        if len(self._cache) > 0:
            self._currentTok = self._cache[0]
            self._currentIndex = 0

    def __iter__(self):
        return self

    # move to next token if there is one
    def next(self, amount):
        if self._currentIndex < len(self._cache) - 1:
            self._currentIndex+=1
            return True
        return False

    # move to previous token
    def prev(self):
        if self._currentIndex > 0:
            self._currentIndex-=1
            return True
        return False

    # get current Token
    @property
    def currentToken(self):
        return self._cache[self._currentIndex]








        

        



    


