from statebase import State
from TreeBuilder.tok import TokenType
from TreeBuilder.expressions import DTorExpression


class DtorState(State):
    def __init__(self):
        State.__init__(self, TokenType.tilde_)

    def handle(self, token_stream, context):
        '''Used for parsing class dtor.'''
        if not self._is_proper_class_context(context):
            return None

        if not self._is_public_scope(context):
            return None

        d_tor_name = context.identifier

        while token_stream.current_token.kind != TokenType.params_end_:
            token_stream.next()

        token_stream.next()

        if token_stream.current_token.kind == TokenType.semicolon_:
            return DTorExpression(d_tor_name)
        else:
            while token_stream.current_token.kind != TokenType.closing_bracket_:
                token_stream.next()

        return None