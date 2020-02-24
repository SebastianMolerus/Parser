import unittest

from TreeBuilder.Parsing.class_parsing.class_children_provider import ClassChildrenProvider
from TreeBuilder.Parsing.parser_creator import ClassParserCreator
from TreeBuilder.tok import TokenType
from mock import Mock, MagicMock


class MockClassParserCreator(ClassParserCreator):
    mocked_parser = Mock()
    get_parser = Mock(return_value=mocked_parser)


class MockedChildrenProvider(ClassChildrenProvider, MockClassParserCreator):
    pass


class class_children_provider_suite(unittest.TestCase):
    token_stream = Mock(return_value=False)
    class_children_provider = MockedChildrenProvider(token_stream)
    state_parser = MockClassParserCreator.mocked_parser

    def tearDown(self):
        self.token_stream.reset_mock(side_effect=True, return_value=True)
        self.token_stream.forward.reset_mock(side_effect=True, return_value=True)
        self.token_stream.current_kind.reset_mock(side_effect=True, return_value=True)
        self.state_parser.reset_mock()

    def test_no_next_token(self):
        self.token_stream.forward.return_value = False

        self.class_children_provider.try_add_children_to_class(None)

        self.state_parser.process.assert_not_called()

    def test_friend_spotted(self):
        self.token_stream.forward.side_effect = [True, False]
        self.token_stream.current_kind.return_value = TokenType.friend_
        expression = MagicMock()

        self.class_children_provider.try_add_children_to_class(expression)

        expression.set_friend_inside.assert_called_once()

    def test_scope_setted(self):
        self.token_stream.forward.side_effect = [True, False]
        self.token_stream.current_kind.return_value = TokenType.public_
        expression = MagicMock()

        self.class_children_provider.try_add_children_to_class(expression)

        expression.set_scope.assert_called_once_with(TokenType.public_)


if __name__ == '__main__':
    unittest.main()
