from parsing import Parser
from parsing import Token
import copy

class TokExpr:
    def __init__(self, tokType, content):
        self._type = tokType
        self._content = content

    @property
    def type(self):
        return self._type
    
    @property
    def content(self):
        return self._content

class TokenStream:
    def __init__(self, parser):
        self._cache = []
        self._currentIndex = None

        while True:
            t = parser.GetToken()
            if t == Token.tok_eof:
                break
            c = parser.identifier
            self._cache.append(TokExpr(t, c))

        if len(self._cache) > 0:
            self._currentTok = self._cache[0]
            self._currentIndex = 0

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
    def current(self):
        return self._cache[self._currentIndex]








        

        



    


