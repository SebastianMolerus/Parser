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
            self._current_index = -1

    def forward(self):
        if self._current_index < len(self._cache) - 1:
            self._current_index += 1
            return True
        return False

    def backward(self):
        if self._current_index > 0:
            self._current_index -= 1
            return True
        return False

    @property
    def current_token(self):
        return self._cache[self._current_index]

    def current_kind(self):
        return self.current_token.kind

    def current_content(self):
        return self.current_token.content

    def get_token_content_from_left(self):
        assert (self.backward())
        identifier = self.current_content()
        self.forward()
        return identifier

    def get_token_kind_from_right(self):
        assert (self.forward())
        kind = self.current_kind()
        self.backward()
        return kind

    def get_token_kind_from_left(self):
        assert (self.backward())
        kind = self.current_kind()
        self.forward()
        return kind

    def get_all_valid_forward_tokens(self, not_valid_tokens):
        if not_valid_tokens is None:
            raise Exception("No arguments given.")

        starting_position = self._current_index

        result = []

        while self.forward():
            if self.current_kind() in not_valid_tokens:
                break
            result.append(self.current_token)

        self._current_index = starting_position

        return result

    def getreturn_part(self):
        assert (self.current_kind() == TokenType.params_begin_)

        stop_parsing_tokens = [TokenType.opening_bracket_,
                               TokenType.closing_bracket_,
                               TokenType.semicolon_]

        starting_position = self._current_index

        assert (self.backward())
        result = []

        while self.backward():
            if self.current_kind() in stop_parsing_tokens:
                break

            if self.current_kind() == TokenType.colon_ and \
                    self.get_token_kind_from_right() != TokenType.colon_ and \
                    self.get_token_kind_from_left() != TokenType.colon_:
                break

            if self.current_kind() != TokenType.virtual_:
                result.append(self.current_token)

        self._current_index = starting_position

        result.reverse()

        return result

    def move_forward_till_closing_bracket_token(self):
        while self.current_kind() != TokenType.closing_bracket_:
            assert (self.forward())

    def move_forward_till_params_end_token(self):
        while self.current_kind() != TokenType.params_end_:
            assert (self.forward())

