from stateBase import State
from TreeBuilder.tok import TokenType
from TreeBuilder.expressions import NamespaceExpression
from stateBuilder import StateParserBuilder


class NamespaceState(State):
    def __init__(self):
        State.__init__(self, TokenType.namespace_)

    def handle(self, token_stream, expression_context, state_parser=None):
        # At namespace
        token_stream.forward()

        # At namespace identifier
        parsed_namespace = NamespaceExpression(token_stream.current_content())

        # At opening bracket
        token_stream.forward()

        _state_parser = state_parser or StateParserBuilder(token_stream). \
            add_class_parsing(). \
            add_namespace_parsing(). \
            get_product()

        self._try_parse_children_for_parsed_namespace(_state_parser, parsed_namespace, token_stream)

        return parsed_namespace

    @staticmethod
    def _try_parse_children_for_parsed_namespace(_state_parser, parsed_namespace, token_stream):
        while token_stream.forward():
            if token_stream.current_kind() == TokenType.closing_bracket_:
                break

            expr = _state_parser.process(parsed_namespace)
            if expr is None:
                continue
            parsed_namespace.attach(expr)

        return parsed_namespace
