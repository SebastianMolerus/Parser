import unittest

from TreeBuilder.Parsing.state_base import State
from TreeBuilder.Parsing.state_parser import StateParser
from TreeBuilder.token_stream import TokenStream
from mock import Mock


class Test_StateParser(unittest.TestCase):

    def test_process_token_with_no_valid_states(self):
        state_mock = Mock(State)
        state_mock.is_valid = Mock(return_value=False)
        state_mock.handle = Mock()
        token_stream_mock = Mock(TokenStream)
        s = StateParser(token_stream_mock)
        s.add_state(state_mock)

        s.process()

        state_mock.is_valid.assert_called_once_with(token_stream_mock, None)
        state_mock.handle.assert_not_called()

    def test_process_token_with_valid_state(self):
        state_mock = Mock(State)
        state_mock.is_valid = Mock(return_value=True)
        state_mock.handle = Mock()
        token_stream_mock = Mock(TokenStream)
        s = StateParser(token_stream_mock)
        s.add_state(state_mock)

        s.process()

        state_mock.is_valid.assert_called_once_with(token_stream_mock, None)
        state_mock.handle.assert_called_once_with(token_stream_mock, None)

    def test_process_token_with_two_valid_state(self):
        state_mock = Mock(State)
        state_mock.is_valid = Mock(return_value=True)
        state_mock.handle = Mock()
        token_stream_mock = Mock(TokenStream)
        s = StateParser(token_stream_mock)
        s.add_state(state_mock)
        s.add_state(state_mock)

        with self.assertRaises(Exception) as exception:
            s.process()

        state_mock.handle.assert_not_called()




