from stateBase import State
from TreeBuilder.tok import TokenType
from TreeBuilder.expressions import MethodExpression


class MethodState(State):
    def __init__(self, token_stream, context):
        State.__init__(self, TokenType.params_begin_, token_stream, context)

    def is_valid(self):
        return State.is_valid(self) and \
               (self._context.get_current_scope() == TokenType.public_ or
                self._context.is_friend_inside())

    def handle(self):
        method_identifier = self.get_token_content_from_left()

        # at Return_Params_begin

        method_return_tokens = self._get_method_return_type()
        str_returns = self.convert_param_tokens_to_string(method_return_tokens)

        # at Return_Params_end

        # at Params_begin

        method_params_tokens = self.get_all_valid_next_tokens(not_valid_tokens=[TokenType.params_end_])
        str_params = self.convert_param_tokens_to_string(method_params_tokens)

        while self._current_kind() != TokenType.params_end_:
            self._forward()

        # at Params_end

        after_parameters_tokens = \
            self.get_all_valid_next_tokens(not_valid_tokens=
                                           [TokenType.semicolon_, TokenType.opening_bracket_])

        is_method_const = False
        for token in after_parameters_tokens:
            if token.kind == TokenType.const_:
                is_method_const = True

            # pure virtual
            if token.kind == TokenType.equal_:
                return None

        while self._forward():
            if self._current_kind() == TokenType.semicolon_ or \
                    self._current_kind() == TokenType.opening_bracket_:
                break

        if self._current_kind() == TokenType.semicolon_:
            return MethodExpression(method_identifier,
                                    str_params,
                                    str_returns,
                                    is_method_const)

        else:
            while self._current_kind() != TokenType.closing_bracket_:
                self._forward()

        return None
