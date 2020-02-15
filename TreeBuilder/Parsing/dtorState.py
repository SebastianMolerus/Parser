from stateBase import State
from TreeBuilder.tok import TokenType
from TreeBuilder.expressions import DTorExpression


class DtorState(State):
    def __init__(self, token_stream, context):
        State.__init__(self, TokenType.tilde_, token_stream, context)

    def is_valid(self):
        return State.is_valid(self) and \
               self._context.get_current_scope() == TokenType.public_

    def handle(self):
        d_tor_name = self._context.identifier

        while self._current_kind() != TokenType.params_end_:
            self._forward()

        self._forward()

        if self._current_kind() == TokenType.semicolon_:
            return DTorExpression(d_tor_name)
        else:
            while self._current_kind() != TokenType.closing_bracket_:
                self._forward()

        return None
