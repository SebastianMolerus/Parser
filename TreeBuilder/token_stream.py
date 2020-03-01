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

    def get_all_valid_forward_tokens(self, not_valid_token_types):
        if not isinstance(not_valid_token_types, list):
            raise Exception("List expected.")

        if len(not_valid_token_types) == 0:
            raise Exception("No arguments given.")

        starting_position = self.current_index

        result = []

        while self.forward():
            if self.current_kind() in not_valid_token_types:
                break
            result.append(self.current_token)

        self.current_index = starting_position

        return result

    def move_forward_to_token_type(self, token_type):
        while self.current_kind() != token_type:
            assert (self.forward())

