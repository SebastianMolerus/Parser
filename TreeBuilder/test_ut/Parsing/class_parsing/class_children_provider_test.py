import unittest

from TreeBuilder.Parsing.class_parsing.class_children_provider import ClassChildrenProvider
from TreeBuilder.Parsing.parser_factory import ClassParserFactory
from TreeBuilder.tok import TokenType
from mock import Mock


class ClassParserFactory(ClassParserFactory):
    get_parser = Mock(name="MockClassParserCreator")


class MockedChildrenProvider(ClassChildrenProvider, ClassParserFactory):
    pass


class class_children_provider_suite(unittest.TestCase):

    def setUp(self):
        ClassParserFactory.get_parser.return_value.reset_mock(return_value=True, side_effect=True)

    # def test_no_next_token(self):
    #     self.token_stream.forward = Mock(return_value=False)
    #     self.class_children_provider.try_add_children_to_class(None)
    #
    #     self.state_parser.process.assert_not_called()
    #
    # def test_friend_spotted(self):
    #     self.token_stream.forward.side_effect = [True, False]
    #     self.token_stream.current_kind.return_value = TokenType.friend_
    #     expression = MagicMock()
    #
    #     self.class_children_provider.try_add_children_to_class(expression)
    #
    #     expression.set_friend_inside.assert_called_once()
    #
    # def test_scope_setted(self):
    #     self.token_stream.forward.side_effect = [True, False]
    #     self.token_stream.current_kind.return_value = TokenType.public_
    #     expression = MagicMock()
    #
    #     self.class_children_provider.try_add_children_to_class(expression)
    #
    #     expression.set_scope.assert_called_once_with(TokenType.public_)
    #

    def test_end_of_parsing(self):
        token_stream = Mock()
        token_stream.forward.return_value = True
        token_stream.current_kind.return_value = TokenType.closing_bracket_
        state_parser = ClassParserFactory.get_parser.return_value
        class_children_provider = MockedChildrenProvider(token_stream)

        expression = Mock()

        class_children_provider.try_add_children_to_class(expression)
        state_parser.process.assert_not_called()
        expression.attach.assert_not_called()

    def test_expr_is_none_after_processing(self):
        token_stream = Mock()
        token_stream.forward.side_effect = [True, False]
        state_parser = ClassParserFactory.get_parser.return_value
        state_parser.process.return_value = None
        class_children_provider = MockedChildrenProvider(token_stream)
        expression = Mock()

        class_children_provider.try_add_children_to_class(expression)

        state_parser.process.assert_called_with(expression)
        expression.attach.assert_not_called()


if __name__ == '__main__':
    unittest.main()
