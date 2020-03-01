import pytest
from TreeBuilder.parsing import parse_method
from TreeBuilder.tok import TokenType
from mock import Mock


def test_beginning_not_on_params_begin():
    token_stream = Mock()
    token_stream.return_value.current_kind.return_value == TokenType.params_end_

    with pytest.raises(Exception):
        parse_method(token_stream)

    assert len(token_stream.mock_calls) == 1


def test_token_from_left_is_not_identifier():
    token_stream = Mock()
    token_stream.current_kind.return_value = TokenType.params_begin_
    token_stream.get_token_kind_from_left.return_value = TokenType.typedef_

    with pytest.raises(Exception):
        parse_method(token_stream)

    assert len(token_stream.mock_calls) == 2
