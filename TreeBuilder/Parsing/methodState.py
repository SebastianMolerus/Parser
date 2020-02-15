from statebase import State
from TreeBuilder.tok import TokenType
from TreeBuilder.expressions import MethodExpression


class MethodState(State):
    def __init__(self):
        State.__init__(self, TokenType.params_begin_)

    def handle(self, token_stream, context):
        '''Used for parsing class methods.

                starting at params_begin token.

                '''

        if not self._is_proper_class_context(context):
            return None
        if not self._is_public_scope(context):
            return None

        assert (token_stream.current_token.kind == TokenType.params_begin_)

        if not context.is_friend_inside() and \
                (
                        context.get_current_scope() == TokenType.protected_ or context.get_current_scope() == TokenType.private_):
            return None

        method_identifier = self._get_identifier_from_left(token_stream)

        if method_identifier == context.identifier:
            return None

        # at Return_Params_begin

        method_return_tokens = self._get_method_return_type(token_stream)
        str_returns = self._convert_param_tokens_to_string(method_return_tokens)

        # at Return_Params_end

        # at Params_begin

        method_params_tokens = self._get_all_valid_next_tokens(token_stream=token_stream, not_valid_tokens=[TokenType.params_end_])
        str_params = self._convert_param_tokens_to_string(method_params_tokens)

        while token_stream.current_token.kind != TokenType.params_end_:
            token_stream.next()

        # at Params_end

        after_parameters_tokens = \
            self._get_all_valid_next_tokens(token_stream=token_stream, not_valid_tokens=
                                                [TokenType.semicolon_, TokenType.opening_bracket_])

        method_constness = False
        for token in after_parameters_tokens:
            if token.kind == TokenType.const_:
                method_constness = True

            # pure virtual
            if token.kind == TokenType.equal_:
                return None

        while token_stream.next():
            if token_stream.current_token.kind == TokenType.semicolon_ or \
                    token_stream.current_token.kind == TokenType.opening_bracket_:
                break

        if token_stream.current_token.kind == TokenType.semicolon_:
            return MethodExpression(method_identifier,
                                    str_params,
                                    str_returns,
                                    method_constness)

        else:
            while token_stream.current_token.kind != TokenType.closing_bracket_:
                token_stream.next()

        return None