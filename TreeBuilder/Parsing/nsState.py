from stateBase import State
from TreeBuilder.tok import TokenType
from TreeBuilder.expressions import NamespaceExpression
from stateBuilder import StateParserBuilder


class NamespaceState(State):
    def __init__(self, token_stream, context=None):
        State.__init__(self, TokenType.namespace_, token_stream, context)

    def handle(self):
        # we have "namespace" already
        # go next
        self._forward()

        # consume identifier
        if self._current_kind() != TokenType.identifier_:
            raise Exception("Identifier expected after namespace keyword")

        # we have identifier
        parsed_namespace = NamespaceExpression(self._current_content())

        self._forward()

        if self._current_kind() != TokenType.opening_bracket_:
            raise Exception("No opening brackets after namespace identifier")

        # currentToken == token.opening_brackets

        state_parser = StateParserBuilder(self._token_stream, parsed_namespace). \
            add_class_parsing(). \
            add_namespace_parsing(). \
            get_product()

        while self._forward():

            # we're done
            if self._current_kind() == TokenType.closing_bracket_:
                break

            expr = state_parser.process()
            if expr is None:
                continue
            parsed_namespace.attach(expr)

        return parsed_namespace
