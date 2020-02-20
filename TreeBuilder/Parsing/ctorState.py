from stateBase import State
from TreeBuilder.tok import TokenType
from TreeBuilder.expressions import CTorExpression
from TreeBuilder.expressions import ClassExpression


class CtorState(State):
    def __init__(self):
        State.__init__(self, TokenType.params_begin_)

    def is_valid(self, token_stream, expression_context):
        return State.is_valid(self, token_stream, expression_context)\
               and \
               self._is_ctor(token_stream, expression_context)\
               and \
               expression_context.get_current_scope() == TokenType.public_

    @staticmethod
    def _is_ctor(token_stream, expression_context):
        if not isinstance(expression_context, ClassExpression):
            return False
        if token_stream.get_token_content_from_left() != expression_context.identifier:
            return False
        return True

    def handle(self, token_stream, expression_context):
        constructor_identifier = expression_context.identifier

        constructorparameters_as_tokens = \
            token_stream.get_all_valid_forward_tokens(not_valid_tokens=[TokenType.params_end_])

        constructorparameters_as_string = self.convert_param_tokens_to_string(constructorparameters_as_tokens)

        token_stream.move_forward_till_params_end_token()

        token_stream.forward()
        if token_stream.current_kind() == TokenType.semicolon_:
            return CTorExpression(constructor_identifier, constructorparameters_as_string)
        else:
            token_stream.move_forward_till_closing_bracket_token()
