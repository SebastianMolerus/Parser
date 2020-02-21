from stateBase import State
from TreeBuilder.tok import TokenType
from stateBuilder import StateParserBuilder
from TreeBuilder.expressions import ClassExpression


class ClassState(State):
    def __init__(self):
        State.__init__(self, TokenType.class_)

    def handle(self, token_stream, expression_context, state_parser=None):
        # At class
        token_stream.forward()

        # At class identifier
        parsed_class = ClassExpression(token_stream.current_content())

        # After class identifier
        token_stream.forward()

        # forwarded class
        if token_stream.current_kind() == TokenType.semicolon_:
            return None

        while token_stream.current_kind() != TokenType.opening_bracket_:
            token_stream.forward()

        _state_parser = state_parser or StateParserBuilder(token_stream, parsed_class). \
            add_class_parsing(). \
            add_dtor_parsing(). \
            add_operator_parsing(). \
            add_params_parsing(). \
            get_product()

        self._try_parse_children_for_parsed_class(_state_parser, parsed_class, token_stream)

        return parsed_class

    @staticmethod
    def _try_parse_children_for_parsed_class(_state_parser, parsed_class, token_stream):
        while token_stream.forward():

            if token_stream.current_kind() == TokenType.friend_:
                parsed_class.set_friend_inside()

            parsed_class.set_scope(token_stream.current_kind())

            if token_stream.current_kind() == TokenType.closing_bracket_:
                break

            expr = _state_parser.process()
            if expr is None:
                continue
            parsed_class.attach(expr)
