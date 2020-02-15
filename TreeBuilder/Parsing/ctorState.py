from statebase import State
from TreeBuilder.tok import TokenType
from TreeBuilder.expressions import CTorExpression


class CtorState(State):
    def __init__(self):
        State.__init__(self, TokenType.params_begin_)

    def handle(self, token_stream, context):
        '''Used for parsing class ctor.'''
        if not self._is_proper_class_context(context):
            return None

        if not self._is_public_scope(context):
            return None

        c_tor_name = context.identifier
        str_params = ''

        if self._get_identifier_from_left(token_stream) != context.identifier:
            return None

        # at Params_begin
        ctor_params_tokens = State._get_all_valid_next_tokens(token_stream=token_stream, not_valid_tokens=[TokenType.params_end_])

        str_params = self._convert_param_tokens_to_string(ctor_params_tokens)

        while token_stream.current_token.kind != TokenType.params_end_:
            token_stream.next()
        # at Params_end

        token_stream.next()
        if token_stream.current_token.kind == TokenType.semicolon_:
            return CTorExpression(c_tor_name, str_params)
        else:
            while token_stream.current_token.kind != TokenType.closing_bracket_:
                token_stream.next()
        return None