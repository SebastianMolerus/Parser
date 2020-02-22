import unittest
from __builtin__ import help

from TreeBuilder.Parsing.class_parsing.class_children_provider import ClassChildrenProvider
from TreeBuilder.Parsing.parser_creator import ClassParserCreator
from TreeBuilder.tokenstream import TokenStream
from mock import Mock


class MockClassParserCreator(ClassParserCreator):
    mocked_parser = Mock()
    get_parser = Mock(return_value=mocked_parser)


class MockedChildrenProvider(ClassChildrenProvider, MockClassParserCreator):
    pass


class class_children_provider_suite(unittest.TestCase):
    token_stream = Mock(TokenStream)
    class_children_provider = MockedChildrenProvider(token_stream)
    state_parser = MockClassParserCreator.mocked_parser

    def tearDown(self):
        self.token_stream.reset_mock()
        self.state_parser.reset_mock()

    def test_no_next_token(self):
        self.token_stream.forward.return_value = False

        self.class_children_provider.try_add_children_to_class(None)

        self.state_parser.process.assert_not_called()


if __name__ == '__main__':
    help(MockedChildrenProvider)
    unittest.main()
