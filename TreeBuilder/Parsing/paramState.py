from TreeBuilder.tok import TokenType
from TreeBuilder.expressions import ClassExpression
from statebase import State
from ctorState import CtorState
from methodState import MethodState


class ParamsState(State):
    def __init__(self):
        State.__init__(self, TokenType.params_begin_)

    def _is_ctor(self, token_stream, context):
        if not isinstance(context, ClassExpression):
            return False
        if self._get_identifier_from_left(token_stream) != context.identifier:
            return False
        return True

    def handle(self, token_stream, context):
        if self._is_ctor(token_stream, context):
            return CtorState().handle(token_stream, context)
        else:
            return MethodState().handle(token_stream, context)