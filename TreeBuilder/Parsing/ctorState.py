from stateBase import State
from TreeBuilder.tok import TokenType
from TreeBuilder.expressions import CTorExpression
from TreeBuilder.expressions import ClassExpression


class CtorState(State):
    def __init__(self, token_stream, context):
        State.__init__(self, TokenType.params_begin_, token_stream, context)

    def is_valid(self):
        return State.is_valid(self) and \
               self._is_ctor() and \
               self._context.get_current_scope() == TokenType.public_

    def _is_ctor(self):
        if not isinstance(self._context, ClassExpression):
            return False
        if self.get_token_content_from_left() != self._context.identifier:
            return False
        return True

    def handle(self):
        c_tor_name = self._context.identifier

        # at Params_begin
        ctor_params_tokens = self.get_all_valid_next_tokens(not_valid_tokens=[TokenType.params_end_])

        str_params = self.convert_param_tokens_to_string(ctor_params_tokens)

        while self._current_kind() != TokenType.params_end_:
            self._forward()
        # at Params_end

        self._forward()
        if self._current_kind() == TokenType.semicolon_:
            return CTorExpression(c_tor_name, str_params)
        else:
            while self._current_kind() != TokenType.closing_bracket_:
                self._forward()

        return None
