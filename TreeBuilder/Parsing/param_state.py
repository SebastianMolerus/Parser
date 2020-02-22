from TreeBuilder.tok import TokenType
from stateBase import State
from stateBuilder import StateParserBuilder


class ParamsState(State):
    def __init__(self):
        State.__init__(self, TokenType.params_begin_)

    def handle(self, token_stream, expression_context):
        state_parser = StateParserBuilder(token_stream). \
            add_method_parsing(). \
            add_ctor_parsing().\
            get_product()

        return state_parser.process(expression_context)
