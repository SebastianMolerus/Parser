class StateParser:
    def __init__(self):
        self._current_state = None
        self._states = []

    def add_state(self, state):
        self._states.append(state)

    def process(self):
        self._current_state = None

        for s in self._states:
            if s.is_valid():
                self._current_state = s
                break

        if self._current_state is not None:
            return self._current_state.handle()

        return None
