from TreeBuilder.Parsing.helpers import convert_param_tokens_to_string
from state_base import State
from TreeBuilder.tok import TokenType
from TreeBuilder.expressions import CTorExpression
from TreeBuilder.expressions import ClassExpression


class CtorState(State):
    def __init__(self):
        State.__init__(self, TokenType.params_begin_)

    def is_valid(self, token_stream, expression_context):
        return State.is_valid(self, token_stream, expression_context)\
               and \
               isinstance(expression_context, ClassExpression)\
               and \
               expression_context.get_current_scope() == TokenType.public_\
               and \
               token_stream.get_token_content_from_left() == expression_context.identifier

    def handle(self, token_stream, expression_context):
        constructor_identifier = expression_context.identifier

        constructor_parameters_as_tokens = \
            token_stream.get_all_valid_forward_tokens(not_valid_tokens=[TokenType.params_end_])

        constructor_parameters_as_string = convert_param_tokens_to_string(constructor_parameters_as_tokens)

        token_stream.move_forward_to_token_type(TokenType.params_end_)

        token_stream.forward()
        if token_stream.current_kind() == TokenType.semicolon_:
            return CTorExpression(constructor_identifier, constructor_parameters_as_string)
        else:
            token_stream.move_forward_to_token_type(TokenType.closing_bracket_)
