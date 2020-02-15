from statebase import State
from TreeBuilder.tok import TokenType
from TreeBuilder.expressions import NamespaceExpression
from statebuilder import StateParserBuilder


class NamespaceState(State):
    def __init__(self):
        State.__init__(self, TokenType.namespace_)

    def handle(self, token_stream, context):
        # we have "namespace" already
        # go next
        token_stream.next()

        # consume identifier
        if token_stream.current_token.kind != TokenType.identifier_:
            raise Exception("Identifier expected after namespace keyword")

        # we have identifier
        parsed_namespace = NamespaceExpression(token_stream.current_token.content)

        token_stream.next()

        if token_stream.current_token.kind != TokenType.opening_bracket_:
            raise Exception("No opening brackets after namespace identifier")

        # currentToken == token.opening_brackets

        while token_stream.next():

            # we're done
            if token_stream.current_token.kind == TokenType.closing_bracket_:
                break

            state_parser = StateParserBuilder(token_stream).\
                add_class_parsing().\
                add_namespace_parsing().\
                get_product()

            expr = state_parser.process(parsed_namespace)
            if expr is None:
                continue
            parsed_namespace.attach(expr)

        return parsed_namespace