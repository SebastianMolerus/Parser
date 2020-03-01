from abc import abstractmethod


class State:
    def __init__(self, kind):
        self._kind = kind

    def is_valid(self, token_stream, expression_context):
        return self._kind == token_stream.current_kind()

    @abstractmethod
    def handle(self, token_stream, expression_context):
        pass

