from state_base import State
from TreeBuilder.tok import TokenType
from TreeBuilder.expressions import DTorExpression


class DtorState(State):
    def __init__(self):
        State.__init__(self, TokenType.tilde_)

    def is_valid(self, token_stream, expression_context):
        return State.is_valid(self, token_stream, expression_context)\
               and \
               expression_context.get_current_scope() == TokenType.public_

    def handle(self, token_stream, expression_context):
        destructor_identifier = expression_context.identifier

        token_stream.move_forward_to_token_type(TokenType.params_end_)

        token_stream.forward()

        if token_stream.current_kind() == TokenType.semicolon_:
            return DTorExpression(destructor_identifier)
        else:
            token_stream.move_forward_to_token_type(TokenType.closing_bracket_)
