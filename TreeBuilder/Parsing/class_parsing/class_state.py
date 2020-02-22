from TreeBuilder.Parsing.class_parsing.class_parser import ClassParser
from TreeBuilder.Parsing.stateBase import State
from TreeBuilder.tok import TokenType


class ClassState(State):
    def __init__(self):
        State.__init__(self, TokenType.class_)

    def handle(self, token_stream, expression_context):
        class_parser = ClassParser(token_stream)
        return class_parser.parse_class()


