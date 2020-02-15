from statebase import State
from TreeBuilder.tok import TokenType
from statebuilder import StateParserBuilder
from TreeBuilder.expressions import ClassExpression


class ClassState(State):
    def __init__(self):
        State.__init__(self, TokenType.class_)

    def handle(self, token_stream, context):
        # we have class already
        # go next
        token_stream.next()

        # consume identifier
        if token_stream.current_token.kind != TokenType.identifier_:
            raise Exception("Identifier expected after class keyword")

        # we have identifier
        parsed_class = ClassExpression(token_stream.current_token.content)

        token_stream.next()

        # we have something...

        # ...maybe forwarded class
        if token_stream.current_token.kind == TokenType.semicolon_:
            return None

        # ...move after opening bracket
        while token_stream.current_token.kind != TokenType.opening_bracket_:
            token_stream.next()

        # currentToken == token.opening_brackets

        while token_stream.next():

            # friend inside class
            if token_stream.current_token.kind == TokenType.friend_:
                parsed_class._friend_inside_spotted()

            # take care of public, prot, private
            parsed_class._set_scope_from_scope_token(token_stream.current_token.kind)

            # we're done
            if token_stream.current_token.kind == TokenType.closing_bracket_:
                break

            state_parser = StateParserBuilder(token_stream).\
                add_class_parsing().\
                add_dtor_parsing().\
                add_operator_parsing().\
                add_params_parsing().\
                get_product()

            expr = state_parser.process(parsed_class)
            if expr is None:
                continue
            parsed_class.attach(expr)

        return parsed_class