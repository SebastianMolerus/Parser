import pytest
from TreeBuilder.expressions import MethodExpression
from TreeBuilder.parsing import parse_method
from TreeBuilder.tok import TokenType
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream
from mock import Mock


def test_token_from_left_is_not_identifier():
    token_stream = Mock()
    token_stream.current_kind.return_value = TokenType.params_begin_
    token_stream.left_token.return_value = TokenType.typedef_

    with pytest.raises(Exception):
        parse_method(token_stream)

    assert len(token_stream.mock_calls) == 2
    assert token_stream.current_kind.call_count == 1
    assert token_stream.left_token.call_count == 1


def test_const_is_part_of_method():
    tr = TokenReader(source_code='''
       void bar() const;
       ''')
    ts = TokenStream(tr)
    ts.forward()
    ts.move_forward(token_type=TokenType.params_begin_)

    parsed_method = parse_method(ts)

    assert isinstance(parsed_method, MethodExpression)
    assert parsed_method.identifier == 'bar'
    assert parsed_method.is_const


def test_virtual_in_return_part_not_part_of_method():
    tr = TokenReader(source_code='''
       virtual void Foo();
       ''')
    ts = TokenStream(tr)
    ts.forward()
    ts.move_forward(token_type=TokenType.params_begin_)

    parsed_method = parse_method(ts)

    assert isinstance(parsed_method, MethodExpression)
    assert parsed_method.identifier == 'Foo'
    assert parsed_method.return_part == 'void'


def test_pure_virtual_is_not_valid():
    tr = TokenReader(source_code='''
      virtual void Foo() = 0;
       ''')
    ts = TokenStream(tr)
    ts.forward()
    ts.move_forward(token_type=TokenType.params_begin_)

    assert parse_method(ts) is None


def test_implemented_method_is_not_valid():
    tr = TokenReader(source_code='''
       void Foo(){
       }
       ''')
    ts = TokenStream(tr)
    ts.forward()
    ts.move_forward(token_type=TokenType.params_begin_)

    assert parse_method(ts) is None


def test_checking_method_expr_fields():
    tr = TokenReader(source_code='''
       void Foo(int a) const;
       ''')
    ts = TokenStream(tr)
    ts.forward()
    ts.move_forward(token_type=TokenType.params_begin_)

    parsed_method = parse_method(ts)

    assert isinstance(parsed_method, MethodExpression)
    assert parsed_method.identifier == 'Foo'
    assert parsed_method.return_part == 'void'
    assert parsed_method.parameters == 'int a'
    assert parsed_method.is_const


