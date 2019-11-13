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
        self._savedIndex = -1

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

    def seek(self, count):

        if count > 0:
            if self._currentIndex + count >= len(self._cache):
                return self._cache[-1]

        elif count < 0:
            if self._currentIndex + count < 0:
                return self._cache[0]

        return self._cache[self._currentIndex + count]
            

    def save(self):
        self._savedIndex = self._currentIndex

    def load(self):
        self._currentIndex = self._savedIndex

    @property
    def current(self):
        return self._cache[self._currentIndex]








        

        



    


