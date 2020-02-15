from stateParser import StateParser


class StateParserBuilder:
    def __init__(self, token_stream, context=None):
        self._sp = StateParser()
        self._token_stream = token_stream
        self._context = context

    def add_class_parsing(self):
        from clsState import ClassState
        self._sp.add_state(ClassState(self._token_stream, self._context))
        return self

    def add_namespace_parsing(self):
        from nsState import NamespaceState
        self._sp.add_state(NamespaceState(self._token_stream, self._context))
        return self

    def add_params_parsing(self):
        from paramState import ParamsState
        self._sp.add_state(ParamsState(self._token_stream, self._context))
        return self

    def add_operator_parsing(self):
        from opState import OperatorState
        self._sp.add_state(OperatorState(self._token_stream, self._context))
        return self

    def add_dtor_parsing(self):
        from dtorState import DtorState
        self._sp.add_state(DtorState(self._token_stream, self._context))
        return self

    def add_ctor_parsing(self):
        from ctorState import CtorState
        self._sp.add_state(CtorState(self._token_stream, self._context))
        return self

    def add_method_parsing(self):
        from methodState import MethodState
        self._sp.add_state(MethodState(self._token_stream, self._context))
        return self

    def get_product(self):
        return self._sp
