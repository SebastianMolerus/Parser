from stateBase import State
from TreeBuilder.tok import TokenType
from TreeBuilder.expressions import OperatorExpression


class OperatorState(State):
    def __init__(self, token_stream, context):
        State.__init__(self, TokenType.operator_, token_stream, context)

    def is_valid(self,):
        return State.is_valid(self) and \
               self._context.get_current_scope() == TokenType.public_

    def handle(self):
        '''Used for parsing class operator.'''
        operator_id_str = ''
        self._forward()

        while self._current_kind() != TokenType.params_begin_:
            operator_id_str += self._token_stream.current_token.content
            self._forward()

        operator_return_tokens = self._get_method_return_type()
        del operator_return_tokens[-1]
        str_returns = self.convert_param_tokens_to_string(operator_return_tokens)

        operator_params_tokens = self.get_all_valid_next_tokens(not_valid_tokens=[TokenType.params_end_])
        str_params = self.convert_param_tokens_to_string(operator_params_tokens)

        while self._current_kind() != TokenType.params_end_:
            self._forward()

        self._forward()
        if self._current_kind() == TokenType.semicolon_:
            return OperatorExpression(operator_id_str, str_params, str_returns)
        else:
            while self._current_kind() != TokenType.closing_bracket_:
                self._forward()

        return None
