from token_stream import TokenStream
from parsing import Parser
from token_expr import TokExpr

class TokenStreamRestoWrapper:
    def __init__(self, TokenStream):
        self._consumedTokens = []
        self._wrappee = TokenStream

    def next(self):
        res = self._wrappee.next()
        self._consumedTokens.append(self._wrappee.currentTok)
        return res
    
    def restore(self, count = -1):
        rev = reversed(self._consumedTokens)
        for i, tok in enumerate(rev):
            self._wrappee.returnTok(tok)
            self._consumedTokens.remove(tok)
            if count > 0 and count == i:
                break

    @property
    def currentTok(self):
        return self._wrappee.currentTok
