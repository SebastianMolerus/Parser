import pytest
from TreeBuilder.tok import TokenType, Token
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream


def test_first_token():
    tr = TokenReader(source_code='''
    class A{}
    ''')

    ts = TokenStream(tr)

    assert ts.forward() is True
    assert ts.current_kind() == TokenType.class_


def test_no_tokens():
    tr = TokenReader(source_code="")

    ts = TokenStream(tr)

    assert ts.forward() is True
    assert ts.current_kind() == TokenType.eof_


def test_no_tokens_spamming_forward():
    tr = TokenReader(source_code="")

    ts = TokenStream(tr)
    assert ts.forward() is True
    assert ts.current_kind() == TokenType.eof_
    assert ts.forward() is False
    assert ts.forward() is False


def test_try_to_get_current_token_before_forward():
    tr = TokenReader(source_code="")

    ts = TokenStream(tr)

    with pytest.raises(Exception):
        ts.current_token


def test_try_to_get_current_kind_before_forward():
    tr = TokenReader(source_code="")

    ts = TokenStream(tr)

    with pytest.raises(Exception):
        ts.current_kind()


def test_try_to_get_current_content_before_forward():
    tr = TokenReader(source_code="")

    ts = TokenStream(tr)

    with pytest.raises(Exception):
        ts.current_content()


def test_backward_does_not_go_before_first_token():
    tr = TokenReader(source_code="A B C D")

    ts = TokenStream(tr)

    assert ts.forward() is True
    assert ts.current_content() == 'A'
    assert ts.forward() is True
    assert ts.current_content() == 'B'
    assert ts.forward() is True
    assert ts.current_content() == 'C'

    while ts.backward():
        pass

    assert ts.current_content() == 'A'


def test_backward_before_forward():
    tr = TokenReader(source_code="A B C D")

    ts = TokenStream(tr)

    assert ts.backward() is False
    assert ts.forward() is True
    assert ts.current_content() == 'A'


def test_token_from_left():
    tr = TokenReader(source_code="A operator C D")

    ts = TokenStream(tr)

    assert ts.forward()
    assert ts.forward()
    assert ts.forward()

    current_token = ts.current_token

    assert current_token.content == 'C'
    assert ts.left_token().content == 'operator'
    assert ts.left_token().kind == TokenType.operator_
    assert current_token is ts.current_token


def test_token_content_from_left_no_tokens():
    tr = TokenReader(source_code="")

    ts = TokenStream(tr)

    with pytest.raises(Exception):
        ts.left_token()


def test_token_kind_from_left_no_tokens():
    tr = TokenReader(source_code="")

    ts = TokenStream(tr)

    with pytest.raises(Exception):
        ts.left_token()


def test_token_kind_from_right():
    tr = TokenReader(source_code="A B C namespace")

    ts = TokenStream(tr)

    assert ts.forward()
    assert ts.forward()
    assert ts.forward()

    current_token = ts.current_token

    assert current_token.content == 'C'
    assert ts.right_token().kind == TokenType.namespace_
    assert current_token is ts.current_token


def test_moving_till_given_token():
    tr = TokenReader(source_code="A B C namespace class operator")

    ts = TokenStream(tr)
    ts.forward()

    ts.move_forward_to(TokenType.class_)

    assert ts.current_kind() == TokenType.class_


def test_moving_till_given_token_but_already_on_this_token():
    tr = TokenReader(source_code="A B C namespace class operator")

    ts = TokenStream(tr)
    ts.forward()

    ts.move_forward_to(TokenType.identifier_)

    assert ts.current_content() == 'A'


def test_getting_valid_tokens_no_stop_token_given():
    tr = TokenReader(source_code="A B C namespace class operator")

    ts = TokenStream(tr)
    ts.forward()

    with pytest.raises(Exception):
        tokens = ts.copy_forward()


def test_getting_valid_tokens():
    tr = TokenReader(source_code="A B C namespace class operator")

    ts = TokenStream(tr)
    ts.forward()

    assert ts.current_content() == 'A'

    tokens = ts.forward_copy_if(lambda steam:
                                steam.current_kind() != TokenType.class_ and steam.current_kind() != TokenType.operator_)

    assert len(tokens) == 4
    assert tokens[0] == Token(TokenType.identifier_, 'A')
    assert tokens[1] == Token(TokenType.identifier_, 'B')
    assert tokens[2] == Token(TokenType.identifier_, 'C')
    assert tokens[3] == Token(TokenType.namespace_)


def test_right_token():
    tr = TokenReader(source_code="(&*)const()int")

    ts = TokenStream(tr)
    ts.forward()

    assert ts.right_token().content == '&'
    assert ts.right_token(2).content == '*'
    assert ts.right_token(3).content == ')'
    assert ts.right_token(4).content == 'const'
    assert ts.right_token(5).content == '('
    assert ts.right_token(6).content == ')'
    assert ts.right_token(7).content == 'int'


def test_left_token():
    tr = TokenReader(source_code="int&*)const))(")

    ts = TokenStream(tr)
    ts.forward()
    ts.move_forward_to(token_type=TokenType.params_begin_)

    assert ts.left_token().content == ')'
    assert ts.left_token(2).content == ')'
    assert ts.left_token(3).content == 'const'
    assert ts.left_token(4).content == ')'
    assert ts.left_token(5).content == '*'
    assert ts.left_token(6).content == '&'
    assert ts.left_token(7).content == 'int'


def test_copy_forward_if():
    tr = TokenReader(source_code="bar foo foobar()")

    ts = TokenStream(tr)
    ts.forward()

    tokens = ts.forward_copy_if(lambda token_stream: token_stream.current_kind() == TokenType.identifier_)

    assert len(tokens) == 3
    assert tokens[0].content == 'bar'
    assert tokens[1].content == 'foo'
    assert tokens[2].content == 'foobar'



