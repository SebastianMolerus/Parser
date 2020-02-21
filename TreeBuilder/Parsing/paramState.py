from TreeBuilder.tok import TokenType
from stateBase import State
from stateBuilder import StateParserBuilder


class ParamsState(State):
    def __init__(self):
        State.__init__(self, TokenType.params_begin_)

    def handle(self, token_stream, expression_context, state_parser=None):
        _state_parser = state_parser or StateParserBuilder(token_stream, expression_context). \
            add_method_parsing(). \
            add_ctor_parsing().\
            get_product()

        return _state_parser.process()
