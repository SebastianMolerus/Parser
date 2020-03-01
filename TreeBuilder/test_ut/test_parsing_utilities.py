import pytest
from TreeBuilder.parsing_utilities import get_return_part_as_tokens
from TreeBuilder.tok import TokenType
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream
from mock import Mock


def test_get_return_part_as_tokens_not_on_params_begin():
    token_stream = Mock()
    token_stream.current_kind.return_value = TokenType.params_end_

    with pytest.raises(Exception):
        get_return_part_as_tokens(token_stream)

    assert token_stream.current_kind.call_count == 1
    assert len(token_stream.mock_calls) == 1


def test_get_return_part_as_tokens_with_semicolon_as_stop():
    tr = TokenReader(source_code='''
    ;const A* Foo(
    ''')

    ts = TokenStream(tr)
    ts.forward()
    ts.move_forward_to_token_type(token_type=TokenType.params_begin_)

    return_tokens = get_return_part_as_tokens(ts)

    assert len(return_tokens) == 3
    assert return_tokens[0].content == 'const'
    assert return_tokens[0].kind == TokenType.const_

    assert return_tokens[1].content == 'A'
    assert return_tokens[1].kind == TokenType.identifier_

    assert return_tokens[2].content == '*'
    assert return_tokens[2].kind == TokenType.star_


def test_get_return_part_as_tokens_with_no_stop_token():
    tr = TokenReader(source_code='''
    Bar& const Foo(
    ''')

    ts = TokenStream(tr)
    ts.forward()
    ts.move_forward_to_token_type(token_type=TokenType.params_begin_)

    return_tokens = get_return_part_as_tokens(ts)

    assert len(return_tokens) == 3
    assert return_tokens[0].content == 'Bar'
    assert return_tokens[0].kind == TokenType.identifier_

    assert return_tokens[1].content == '&'
    assert return_tokens[1].kind == TokenType.ref_

    assert return_tokens[2].content == 'const'
    assert return_tokens[2].kind == TokenType.const_


def test_get_return_part_as_tokens_no_backward_tokens():
    token_stream = Mock()
    token_stream.current_kind.return_value = TokenType.params_begin_
    token_stream.backward.return_value = False

    with pytest.raises(Exception):
        get_return_part_as_tokens(token_stream)

    assert len(token_stream.mock_calls) == 2
    assert token_stream.current_kind.call_count == 1
    assert token_stream.backward.call_count == 1


def test_get_return_part_as_tokens_opening_bracket_as_end_barrier():
    token_stream = Mock()
    token_stream.current_kind.side_effect = [TokenType.params_begin_, TokenType.opening_bracket_]
    token_stream.backward.return_value = True

    assert len(get_return_part_as_tokens(token_stream)) == 0

    assert len(token_stream.mock_calls) == 4
    assert token_stream.current_kind.call_count == 2
    assert token_stream.backward.call_count == 2


def test_get_return_part_as_tokens_closing_bracket_as_end_barrier():
    token_stream = Mock()
    token_stream.current_kind.side_effect = [TokenType.params_begin_, TokenType.closing_bracket_]
    token_stream.backward.return_value = True

    assert len(get_return_part_as_tokens(token_stream)) == 0

    assert len(token_stream.mock_calls) == 4
    assert token_stream.current_kind.call_count == 2
    assert token_stream.backward.call_count == 2


def test_get_return_part_as_tokens_semicolon_as_end_barrier():
    token_stream = Mock()
    token_stream.current_kind.side_effect = [TokenType.params_begin_, TokenType.semicolon_]
    token_stream.backward.return_value = True

    assert len(get_return_part_as_tokens(token_stream)) == 0

    assert len(token_stream.mock_calls) == 4
    assert token_stream.current_kind.call_count == 2
    assert token_stream.backward.call_count == 2


def test_get_return_part_as_tokens_semicolon_as_end_barrier():
    token_stream = Mock()
    token_stream.current_kind.side_effect = [TokenType.params_begin_, TokenType.semicolon_]
    token_stream.backward.return_value = True

    assert len(get_return_part_as_tokens(token_stream)) == 0

    assert len(token_stream.mock_calls) == 4
    assert token_stream.current_kind.call_count == 2
    assert token_stream.backward.call_count == 2


def get_return_part_as_tokens_scope_token_is_end_barrier():
    tr = TokenReader(source_code='''
    public :void Foo(
    ''')

    ts = TokenStream(tr)
    ts.forward()
    ts.move_forward_to_token_type(token_type=TokenType.params_begin_)

    return_tokens = get_return_part_as_tokens(ts)

    assert len(return_tokens) == 1
    assert return_tokens[0].content == 'void'
    assert return_tokens[0].kind == TokenType.identifier_


def get_return_part_as_tokens_scope_namespace_is_part_of_return_part():
    tr = TokenReader(source_code='''
    A::B* const Foo(
    ''')

    ts = TokenStream(tr)
    ts.forward()
    ts.move_forward_to_token_type(token_type=TokenType.params_begin_)

    return_tokens = get_return_part_as_tokens(ts)

    assert len(return_tokens) == 6

    assert return_tokens[0].content == 'A'
    assert return_tokens[1].content == ':'
    assert return_tokens[2].content == ':'
    assert return_tokens[3].content == 'B'
    assert return_tokens[4].content == '*'
    assert return_tokens[5].content == 'const'

    assert return_tokens[0].kind == TokenType.identifier_
    assert return_tokens[1].kind == TokenType.colon_
    assert return_tokens[2].kind == TokenType.colon_
    assert return_tokens[3].kind == TokenType.identifier_
    assert return_tokens[4].kind == TokenType.star_
    assert return_tokens[5].kind == TokenType.const_


