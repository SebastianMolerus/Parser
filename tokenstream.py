from TokenReader import Token
from TokenReader import TokenReader
from TokenReader import TokenType

class TokenStream:
    def __init__(self, token_reader):
        self._cache = []

        while True:
            token = token_reader.get_next_token()
            self._cache.append(token)
            if token.type == TokenType._eof:
                break
            
        if len(self._cache) > 0:
            self._currentIndex = -1


    def next(self):
        if self._currentIndex < len(self._cache) - 1:
            self._currentIndex+=1
            return True
        return False


    def prev(self):
        if self._currentIndex > 0:
            self._currentIndex-=1
            return True
        return False

 
    @property
    def currentToken(self):
        return self._cache[self._currentIndex]








        

        



    


