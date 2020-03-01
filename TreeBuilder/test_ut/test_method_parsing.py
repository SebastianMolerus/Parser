import pytest
from TreeBuilder.parsing import parse_method
from TreeBuilder.tok import TokenType
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream


def test_beginning_not_on_params_begin():
    tr = TokenReader(source_code='''
    foo(
    ''')
    ts = TokenStream(tr)
    ts.forward()

    with pytest.raises(Exception):
        parse_method(ts)


def test_token_from_left_is_not_identifier():
    tr = TokenReader(source_code='''
    void typedef();
    ''')
    ts = TokenStream(tr)
    ts.forward()
    ts.forward()
    ts.forward()

    assert ts.current_kind() == TokenType.params_begin_

    with pytest.raises(Exception):
        parse_method(ts)