from TreeBuilder.Parsing.helpers import get_return_part, convert_param_tokens_to_string
from state_base import State
from TreeBuilder.tok import TokenType
from TreeBuilder.expressions import OperatorExpression


class OperatorState(State):
    def __init__(self):
        State.__init__(self, TokenType.operator_)

    def is_valid(self, token_stream, expression_context):
        return State.is_valid(self, token_stream, expression_context)\
               and \
               expression_context.get_current_scope() == TokenType.public_

    def handle(self, token_stream, expression_context):
        operator_id_str = ''
        token_stream.forward()

        while token_stream.current_kind() != TokenType.params_begin_:
            operator_id_str += token_stream.current_content()
            token_stream.forward()

        operator_return_tokens = get_return_part(token_stream)
        del operator_return_tokens[-1]
        return_pars_as_str = convert_param_tokens_to_string(operator_return_tokens)

        operator_params_tokens = token_stream.get_all_valid_forward_tokens(not_valid_tokens=[TokenType.params_end_])
        str_params = convert_param_tokens_to_string(operator_params_tokens)

        token_stream.move_forward_to_token_type(TokenType.params_end_)

        token_stream.forward()
        if token_stream.current_kind() == TokenType.semicolon_:
            return OperatorExpression(operator_id_str, str_params, return_pars_as_str)
        else:
            token_stream.move_forward_to_token_type(TokenType.closing_bracket_)
