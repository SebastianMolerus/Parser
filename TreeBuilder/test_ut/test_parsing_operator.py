import pytest
from TreeBuilder.expressions import ClassExpression, OperatorExpression
from TreeBuilder.parsing import parse_operator
from TreeBuilder.tok import TokenType
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream
from mock import Mock


def test_starting_from_operator_token():
    token_stream = Mock()
    token_stream.current_kind.return_value = TokenType.params_begin_

    with pytest.raises(Exception):
        parse_operator(token_stream, None)

    assert len(token_stream.mock_calls) == 1
    assert token_stream.current_kind.call_count == 1


def test_operator_not_in_public_context():
    token_stream = Mock()
    token_stream.current_kind.return_value = TokenType.operator_
    expression_context = Mock()
    expression_context.get_current_scope.return_value = TokenType.private_

    assert parse_operator(token_stream, expression_context) is None


@pytest.mark.parametrize(argnames="operator_mark",
                         argvalues=['++', '--', '+=', '+', '-', '<<', '>>', '=', '[]', '->', '()', '*', '~', '<',
                                    '||', '->*', ',', '^=', '-='],)
def test_operator_identifier(operator_mark):
    tr = TokenReader(source_code='''
        operator{}();
        '''.format(operator_mark))
    ts = TokenStream(tr)
    ts.forward()
    ts.move_forward_to(token_type=TokenType.operator_)

    expr = ClassExpression("X")
    expr.set_scope(TokenType.public_)

    parsed_operator = parse_operator(ts, expr)

    assert isinstance(parsed_operator, OperatorExpression)
    assert parsed_operator.identifier == 'operator{}'.format(operator_mark)


@pytest.mark.parametrize(argnames="operator_mark",
                         argvalues=['++', '--', '+=', '+', '-', '<<', '>>', '=', '[]', '->', '()', '*', '~', '<',
                                    '||', '->*', ',', '^=', '-='],)
def test_operator_return_part(operator_mark):
    tr = TokenReader(source_code='''
        T& operator{}();
        '''.format(operator_mark))
    ts = TokenStream(tr)
    ts.forward()
    ts.move_forward_to(token_type=TokenType.operator_)

    expr = ClassExpression("X")
    expr.set_scope(TokenType.public_)

    parsed_operator = parse_operator(ts, expr)

    assert parsed_operator.return_part == 'T&'
