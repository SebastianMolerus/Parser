import unittest

from TreeBuilder.Parsing.class_parsing.class_children_provider import ClassChildrenProvider
from TreeBuilder.Parsing.class_parsing.class_parser import ClassParser
from TreeBuilder.expressions import ClassExpression, Expression
from TreeBuilder.tok import TokenType
from TreeBuilder.tokenstream import TokenStream
from mock import Mock


class ClassChildrenProviderMock(ClassChildrenProvider):
    try_add_children_to_class = Mock()

    @staticmethod
    def try_add_children_to_class_side_effect(*args, **kwargs):
        assert (len(args) == 1)
        args[0].attach(Expression('Expr'))


class MockedClassParser(ClassParser, ClassChildrenProviderMock):
    pass


class class_parser_suite(unittest.TestCase):
    token_stream = Mock(TokenStream)
    class_parser = MockedClassParser(token_stream)

    def tearDown(self):
        self.token_stream.reset_mock()
        self.class_parser.try_add_children_to_class.reset_mock()
        self.class_parser.try_add_children_to_class.side_effect = None

    def test_class_without_children(self):
        class_identifier = 'Foo'
        self.token_stream.current_content.return_value = class_identifier

        parsed = self.class_parser.parse_class()

        self.assertIsNotNone(parsed)
        self.class_parser.\
            try_add_children_to_class.assert_called_once_with(ClassExpression(class_identifier))
        self.assertEqual(self.token_stream.forward.call_count, 2)
        self.assertEqual(len(parsed), 0)

    def test_class_with_children(self):
        class_identifier = 'Bar'
        self.token_stream.current_content.return_value = class_identifier
        self.class_parser.try_add_children_to_class.side_effect =\
            self.class_parser.try_add_children_to_class_side_effect

        parsed = self.class_parser.parse_class()

        self.class_parser.\
            try_add_children_to_class.assert_called_once_with(ClassExpression(class_identifier))
        self.assertEqual(self.token_stream.forward.call_count, 2)
        self.assertEqual(len(parsed), 1)

    def test_forwarded_class(self):
        self.token_stream.current_kind.return_value = TokenType.semicolon_

        parsed = self.class_parser.parse_class()

        self.assertIsNone(parsed)
        self.class_parser.try_add_children_to_class.assert_not_called()


if __name__ == '__main__':
    unittest.main()
