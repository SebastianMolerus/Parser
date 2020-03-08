import re

from tok import TokenType


class TokenStream:
    def __init__(self, token_reader):
        self._cache = []

        while True:
            token = token_reader.get_next_token()
            self._cache.append(token)
            if token.kind == TokenType.eof_:
                break

        if len(self._cache) > 0:
            self.current_index = -1

    def forward(self):
        if self.current_index < len(self._cache) - 1:
            self.current_index += 1
            return True
        return False

    def backward(self):
        if self.current_index > 0:
            self.current_index -= 1
            return True
        return False

    @property
    def current_token(self):
        if self.current_index == -1:
            raise Exception("Current Token not setted. Use Forward first.")
        return self._cache[self.current_index]

    def current_kind(self):
        return self.current_token.kind

    def current_content(self):
        return self.current_token.content

    def right_token(self, how_far=1):
        return self._cache[self.current_index + how_far]

    def left_token(self, how_far=1):
        return self._cache[self.current_index - how_far]

    def move_forward_to(self, token_type):
        while self.current_kind() != token_type:
            assert (self.forward())

    def forward_copy_if(self, predicate):
        copied = []
        while predicate(self) is True:
            copied.append(self.current_token)
            assert self.forward()
        return copied


