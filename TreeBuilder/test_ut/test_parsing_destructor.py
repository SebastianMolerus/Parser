import pytest
from TreeBuilder.expressions import ClassExpression, NamespaceExpression, DTorExpression
from TreeBuilder.parsing import parse_destructor
from TreeBuilder.tok import TokenType
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream
from mock import Mock


def test_starting_not_from_tilde():
    token_stream = Mock()
    token_stream.current_kind.return_value = TokenType.identifier_

    with pytest.raises(Exception):
        parse_destructor(token_stream, None)

    assert len(token_stream.mock_calls) == 1
    assert token_stream.current_kind.call_count == 1


def test_context_is_not_a_class():
    token_stream = Mock()
    token_stream.current_kind.return_value = TokenType.tilde_

    with pytest.raises(Exception):
        parse_destructor(token_stream, NamespaceExpression("Foo"))

    assert len(token_stream.mock_calls) == 1
    assert token_stream.current_kind.call_count == 1


def test_private_destructor_is_invalid():
    token_stream = Mock()
    token_stream.current_kind.return_value = TokenType.tilde_
    class_expression = Mock(ClassExpression)
    class_expression.get_current_scope.return_value = TokenType.private_

    assert parse_destructor(token_stream, class_expression) is None


def test_protected_destructor_is_invalid():
    token_stream = Mock()
    token_stream.current_kind.return_value = TokenType.tilde_
    class_expression = Mock(ClassExpression)
    class_expression.get_current_scope.return_value = TokenType.protected_

    assert parse_destructor(token_stream, class_expression) is None


def test_identifier_is_passed_from_context():
    tr = TokenReader(source_code='''
        ~Foo();
    ''')
    ts = TokenStream(tr)
    ts.forward()
    class_expr = ClassExpression("Foo")
    class_expr.set_scope(TokenType.public_)

    parsed_dtor = parse_destructor(ts, class_expr)

    assert parsed_dtor.identifier == class_expr.identifier


def test_dtor_implemented_inline_is_not_valid():
    tr = TokenReader(source_code='''
        ~Foo() {}
    ''')
    ts = TokenStream(tr)
    ts.forward()
    class_expr = ClassExpression("Foo")
    class_expr.set_scope(TokenType.public_)

    assert parse_destructor(ts, class_expr) is None


def test_dtor_with_ending_semicolon_is_valid():
    tr = TokenReader(source_code='''
        ~Foo();
    ''')
    ts = TokenStream(tr)
    ts.forward()
    class_expr = ClassExpression("Foo")
    class_expr.set_scope(TokenType.public_)

    assert isinstance(parse_destructor(ts, class_expr), DTorExpression)


def test_ending_on_closing_bracket_with_implemented_inline():
    tr = TokenReader(source_code='''
        ~Foo() {}
    ''')
    ts = TokenStream(tr)
    ts.forward()
    class_expr = ClassExpression("Foo")
    class_expr.set_scope(TokenType.public_)

    parse_destructor(ts, class_expr)

    assert ts.current_kind() == TokenType.closing_bracket_
