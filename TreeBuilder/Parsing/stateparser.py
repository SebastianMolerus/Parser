class StateParser:
    def __init__(self, token_stream):
        self._current_state = None
        self._states = []
        self._token_stream = token_stream

    def add_state(self, state):
        self._states.append(state)

    def process(self, context=None):
        self._current_state = None

        for s in self._states:
            if s.is_successful_compared(self._token_stream.current_token.kind):
                self._current_state = s
                break

        if self._current_state is not None:
            return self._current_state.handle(self._token_stream, context)

        return None




