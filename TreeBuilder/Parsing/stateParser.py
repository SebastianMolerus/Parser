class StateParser:
    def __init__(self, token_stream, expression_context=None):
        self._current_state = None
        self._states = []
        self._token_stream = token_stream
        self._expression_context = expression_context

    def add_state(self, state):
        self._states.append(state)

    def process(self):
        self._current_state = None

        for s in self._states:
            if s.is_valid(self._token_stream, self._expression_context):
                self._current_state = s
                break

        if self._current_state is not None:
            return self._current_state.handle(self._token_stream, self._expression_context)

        return None
