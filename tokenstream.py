from token_ import TokenType


class TokenStream:
    def __init__(self, token_reader):
        self._cache = []

        while True:
            token = token_reader.get_next_token()
            self._cache.append(token)
            if token.kind == TokenType.eof_:
                break
            
        if len(self._cache) > 0:
            self._currentIndex = -1

    def next(self):
        if self._currentIndex < len(self._cache) - 1:
            self._currentIndex += 1
            return True
        return False

    def prev(self):
        if self._currentIndex > 0:
            self._currentIndex -= 1
            return True
        return False

    @property
    def current_token(self):
        return self._cache[self._currentIndex]








        

        



    


