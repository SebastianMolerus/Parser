from TreeBuilder.Parsing.parser_factory import ClassParserFactory
from TreeBuilder.tok import TokenType


class ClassChildrenProvider(ClassParserFactory):
    def __init__(self, token_stream, *args, **kwargs):
        super(ClassChildrenProvider, self).__init__(*args, **kwargs)
        self._state_parser = super(ClassChildrenProvider, self).get_parser(token_stream)
        self._token_stream = token_stream

    def try_add_children_to_class(self, parsed_class_context):
        while self._token_stream.forward():

            if self._token_stream.current_kind() == TokenType.friend_:
                parsed_class_context.set_friend_inside()

            parsed_class_context.set_scope(self._token_stream.current_kind())

            if self._token_stream.current_kind() == TokenType.closing_bracket_:
                break

            expr = self._state_parser.process(parsed_class_context)
            if expr is None:
                continue
            parsed_class_context.attach(expr)
