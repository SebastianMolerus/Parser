from stateParser import StateParser


class StateParserBuilder:
    def __init__(self, token_stream, context=None):
        self._sp = StateParser(token_stream, context)
        self._context = context

    def add_class_parsing(self):
        from clsState import ClassState
        self._sp.add_state(ClassState())
        return self

    def add_namespace_parsing(self):
        from nsState import NamespaceState
        self._sp.add_state(NamespaceState())
        return self

    def add_params_parsing(self):
        from paramState import ParamsState
        self._sp.add_state(ParamsState())
        return self

    def add_operator_parsing(self):
        from opState import OperatorState
        self._sp.add_state(OperatorState())
        return self

    def add_dtor_parsing(self):
        from dtorState import DtorState
        self._sp.add_state(DtorState())
        return self

    def add_ctor_parsing(self):
        from ctorState import CtorState
        self._sp.add_state(CtorState())
        return self

    def add_method_parsing(self):
        from methodState import MethodState
        self._sp.add_state(MethodState())
        return self

    def get_product(self):
        return self._sp
