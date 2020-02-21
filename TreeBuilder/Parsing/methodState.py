from stateBase import State
from TreeBuilder.tok import TokenType, Token
from TreeBuilder.expressions import MethodExpression


class MethodState(State):
    def __init__(self):
        State.__init__(self, TokenType.params_begin_)

    def is_valid(self, token_stream, expression_context):
        return State.is_valid(self, token_stream, expression_context)\
               and \
               (expression_context.get_current_scope() == TokenType.public_ \
                or
                expression_context.is_friend_inside()) \
               and \
               token_stream.get_token_content_from_left() != expression_context.identifier

    def handle(self, token_stream, expression_context):
        # At params begin
        method_name = token_stream.get_token_content_from_left()

        method_return_part_as_tokens = token_stream.getreturn_part()
        method_return_part_as_string = self.convert_param_tokens_to_string(method_return_part_as_tokens)

        method_parameters_as_tokens = token_stream.get_all_valid_forward_tokens(not_valid_tokens=
                                                                                [TokenType.params_end_])
        method_parameters_as_string = self.convert_param_tokens_to_string(method_parameters_as_tokens)

        token_stream.move_forward_till_params_end_token()

        after_method_parameters_tokens = \
            token_stream.get_all_valid_forward_tokens(not_valid_tokens=
                                                      [TokenType.semicolon_, TokenType.opening_bracket_])

        is_method_const = False
        if Token(TokenType.const_) in after_method_parameters_tokens:
            is_method_const = True

        if Token(TokenType.equal_) in after_method_parameters_tokens:
            return None

        while token_stream.forward():
            if token_stream.current_kind() == TokenType.semicolon_:
                return MethodExpression(method_name,
                                        method_parameters_as_string,
                                        method_return_part_as_string,
                                        is_method_const)

            elif token_stream.current_kind() == TokenType.opening_bracket_:
                token_stream.move_forward_till_closing_bracket_token()
                break

