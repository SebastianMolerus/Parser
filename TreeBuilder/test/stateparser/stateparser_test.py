import unittest

from TreeBuilder.Parsing.stateBase import State
from TreeBuilder.Parsing.stateParser import StateParser
from mock import Mock


class Test_StateParser(unittest.TestCase):

    def test_process_token_with_no_valid_states(self):
        state_mock = Mock(State)
        state_mock.is_valid = Mock(return_value=False)
        state_mock.handle = Mock()
        s = StateParser()
        s.add_state(state_mock)

        s.process()

        state_mock.is_valid.assert_called_once()
        state_mock.handle.assert_not_called()

    def test_process_token_with_valid_state(self):
        state_mock = Mock(State)
        state_mock.is_valid = Mock(return_value=True)
        state_mock.handle = Mock()
        s = StateParser()
        s.add_state(state_mock)

        s.process()

        state_mock.is_valid.assert_called_once()
        state_mock.handle.assert_called_once()