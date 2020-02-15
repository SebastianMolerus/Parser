from statebase import State
from TreeBuilder.tok import TokenType
from TreeBuilder.expressions import OperatorExpression


class OperatorState(State):
    def __init__(self):
        State.__init__(self, TokenType.operator_)

    def handle(self, token_stream, context):
        '''Used for parsing class operator.'''

        if not self._is_proper_class_context(context):
            return None

        if not self._is_public_scope(context):
            return None

        operator_id_str = ''
        token_stream.next()

        while token_stream.current_token.kind != TokenType.params_begin_:
            operator_id_str += token_stream.current_token.content
            token_stream.next()

        operator_return_tokens = self._get_method_return_type(token_stream)
        del operator_return_tokens[-1]
        str_returns = self._convert_param_tokens_to_string(operator_return_tokens)

        operator_params_tokens = State._get_all_valid_next_tokens(token_stream=token_stream, not_valid_tokens=[TokenType.params_end_])
        str_params = self._convert_param_tokens_to_string(operator_params_tokens)

        while token_stream.current_token.kind != TokenType.params_end_:
            token_stream.next()

        token_stream.next()
        if token_stream.current_token.kind == TokenType.semicolon_:
            return OperatorExpression(operator_id_str, str_params, str_returns)
        else:
            while token_stream.current_token.kind != TokenType.closing_bracket_:
                token_stream.next()
        return None