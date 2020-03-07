import pytest
from TreeBuilder.expressions import ClassExpression, NamespaceExpression
from TreeBuilder.parsing import parse_constructor
from TreeBuilder.tok import TokenType
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream
from mock import Mock


def get_prepared_token_stream(source_code):
    tr = TokenReader(source_code=source_code)
    ts = TokenStream(tr)
    ts.forward()
    ts.move_forward(TokenType.params_begin_)
    return ts


def test_current_token_is_not_params_begin():
    token_stream = Mock()
    token_stream.current_kind.return_value = TokenType.params_end_

    with pytest.raises(Exception):
        parse_constructor(token_stream, None)

    token_stream.current_kind.assert_called_once()
    assert len(token_stream.mock_calls) == 1


def test_none_context():
    token_stream = Mock()
    token_stream.current_kind.return_value = TokenType.params_begin_

    with pytest.raises(Exception):
        parse_constructor(token_stream, None)

    token_stream.current_kind.assert_called_once()
    assert len(token_stream.mock_calls) == 1


def test_not_valid_context():
    token_stream = Mock()
    token_stream.current_kind.return_value = TokenType.params_begin_

    with pytest.raises(Exception):
        parse_constructor(token_stream, NamespaceExpression("Foo"))

    token_stream.current_kind.assert_called_once()
    assert len(token_stream.mock_calls) == 1


def test_ctor_identifier_from_class_identifier():
    token_stream = get_prepared_token_stream(source_code="Foo();")
    class_expression = ClassExpression("Foo")
    parsed_ctor = parse_constructor(token_stream, class_expression)

    assert parsed_ctor.identifier == class_expression.identifier


def test_parameters_are_passed_to_ctor():
    token_stream = get_prepared_token_stream(source_code="Foo(Foo const& other);")
    parsed_ctor = parse_constructor(token_stream, ClassExpression("Foo"))

    assert parsed_ctor.parameters == 'Foo const& other'


def test_ctor_implemented_in_line_is_not_valid():
    token_stream = get_prepared_token_stream(source_code="Foo(){}")
    assert parse_constructor(token_stream, ClassExpression("Foo")) is None
