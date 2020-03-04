import pytest
from TreeBuilder.parsing import parse_namespace
from TreeBuilder.tok import TokenType
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream
from mock import Mock


def test_current_token_is_not_a_namespace():
    token_stream = Mock()
    token_stream.current_kind.return_value = TokenType.public_

    with pytest.raises(Exception):
        parse_namespace(token_stream)

    assert len(token_stream.mock_calls) == 1
    assert token_stream.current_kind.call_count == 1


def test_no_identifier_token_after_namespace():
    token_stream = Mock()
    token_stream.forward
    token_stream.current_kind.side_effect = [TokenType.namespace_, TokenType.closing_bracket_]

    with pytest.raises(Exception):
        parse_namespace(token_stream)

    assert len(token_stream.mock_calls) == 3
    assert token_stream.current_kind.call_count == 2
    assert token_stream.forward.call_count == 1


def test_namespace_identifier_from_token():
    tr = TokenReader(source_code='''
    namespace N {}
    ''')
    ts = TokenStream(tr)
    ts.forward()

    parsed_namespace = parse_namespace(ts)
    assert parsed_namespace.identifier == 'N'


def test_namespace_without_children():
    tr = TokenReader(source_code='''
    namespace N {}
    ''')
    ts = TokenStream(tr)
    ts.forward()

    parsed_namespace = parse_namespace(ts)
    assert len(parsed_namespace) == 0


def test_namespace_with_children():
    tr = TokenReader(source_code='''
    namespace N {
    class A{}
    }
    ''')
    ts = TokenStream(tr)
    ts.forward()

    parsed_namespace = parse_namespace(ts)
    assert len(parsed_namespace) == 1

