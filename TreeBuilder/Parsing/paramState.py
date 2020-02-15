from TreeBuilder.tok import TokenType
from stateBase import State
from stateBuilder import StateParserBuilder


class ParamsState(State):
    def __init__(self, token_stream, context):
        State.__init__(self, TokenType.params_begin_, token_stream, context)

    def handle(self):
        state_parser = StateParserBuilder(self._token_stream, self._context).\
            add_ctor_parsing().\
            add_method_parsing().\
            get_product()

        return state_parser.process()
