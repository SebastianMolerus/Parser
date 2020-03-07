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
        saved_position = self.current_index
        while how_far > 0:
            assert (self.forward())
            how_far -= 1
        tok = self.current_token
        self.current_index = saved_position
        return tok

    def left_token(self, how_far=1):
        saved_position = self.current_index
        while how_far > 0:
            assert (self.backward())
            how_far -= 1
        tok = self.current_token
        self.current_index = saved_position
        return tok

    def copy_forward(self, not_valid_token_types):
        result = []
        while self.forward():
            if self.current_kind() in not_valid_token_types:
                break
            result.append(self.current_token)
        return result

    def get_all_valid_forward_tokens_using_regexp(self, re_pattern):
        txt = ''
        res = []
        while self.forward():
            txt += self.current_content()
            res.append(self.current_token)
            x = re.search(re_pattern, txt)
            if x is not None:
                del res[-1]
                break

        return res

    def move_forward(self, token_type):
        while self.current_kind() != token_type:
            assert (self.forward())

    def copy_forward_if(self, predicate):
        copied = []
        while predicate(self.current_token) is True:
            copied.append(self.current_token)
            assert self.forward()
        return copied



