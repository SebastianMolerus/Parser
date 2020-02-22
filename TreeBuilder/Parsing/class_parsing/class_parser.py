from TreeBuilder.Parsing.class_parsing.class_children_provider import ClassChildrenProvider
from TreeBuilder.expressions import ClassExpression
from TreeBuilder.tok import TokenType


class ClassParser(ClassChildrenProvider):
    def __init__(self, token_stream, *args, **kwargs):
        self._token_stream = token_stream
        super(ClassParser, self).__init__(token_stream, *args, **kwargs)

    def parse_class(self):
        # At 'class'
        self._token_stream.forward()

        # At class 'identifier'
        parsed_class = ClassExpression(self._token_stream.current_content())

        self._token_stream.forward()

        # forwarded class
        if self._token_stream.current_kind() == TokenType.semicolon_:
            return None

        self._token_stream.move_forward_to_token_type(TokenType.opening_bracket_)

        super(ClassParser, self).try_add_children_to_class(parsed_class)

        return parsed_class
