import pytest
from TreeBuilder.parsing_utilities import get_return_part_as_tokens
from TreeBuilder.tok import TokenType
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream
from mock import Mock


class TestGetReturnParsAsTokensSuite:
    def __init__(self):
        pass

    def test_not_on_params_begin(self):
        token_stream = Mock()
        token_stream.current_kind.return_value = TokenType.params_end_

        with pytest.raises(Exception):
            get_return_part_as_tokens(token_stream)

        assert token_stream.current_kind.call_count == 1
        assert len(token_stream.mock_calls) == 1

    def test_with_semicolon_as_stop(self):
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

    def test_with_no_stop_token(self):
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

    def test_no_backward_tokens(self):
        token_stream = Mock()
        token_stream.current_kind.return_value = TokenType.params_begin_
        token_stream.backward.return_value = False

        with pytest.raises(Exception):
            get_return_part_as_tokens(token_stream)

        assert len(token_stream.mock_calls) == 2
        assert token_stream.current_kind.call_count == 1
        assert token_stream.backward.call_count == 1

    def test_opening_bracket_as_end_barrier(self):
        token_stream = Mock()
        token_stream.current_kind.side_effect = [TokenType.params_begin_, TokenType.opening_bracket_]
        token_stream.backward.return_value = True

        assert len(get_return_part_as_tokens(token_stream)) == 0

        assert len(token_stream.mock_calls) == 4
        assert token_stream.current_kind.call_count == 2
        assert token_stream.backward.call_count == 2

    def test_closing_bracket_as_end_barrier(self):
        token_stream = Mock()
        token_stream.current_kind.side_effect = [TokenType.params_begin_, TokenType.closing_bracket_]
        token_stream.backward.return_value = True

        assert len(get_return_part_as_tokens(token_stream)) == 0

        assert len(token_stream.mock_calls) == 4
        assert token_stream.current_kind.call_count == 2
        assert token_stream.backward.call_count == 2

    def test_semicolon_as_end_barrier(self):
        token_stream = Mock()
        token_stream.current_kind.side_effect = [TokenType.params_begin_, TokenType.semicolon_]
        token_stream.backward.return_value = True

        assert len(get_return_part_as_tokens(token_stream)) == 0

        assert len(token_stream.mock_calls) == 4
        assert token_stream.current_kind.call_count == 2
        assert token_stream.backward.call_count == 2

    def test_scope_token_is_end_barrier(self):
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

    def test_scope_namespace_is_part_of_return_part(self):
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

    def test_virtual_not_in_return_part(self):
        tr = TokenReader(source_code='''
        virtual A& const Foo(
        ''')

        ts = TokenStream(tr)
        ts.forward()
        ts.move_forward_to_token_type(token_type=TokenType.params_begin_)

        return_tokens = get_return_part_as_tokens(ts)

        assert len(return_tokens) == 3

        assert return_tokens[0].content == 'A'
        assert return_tokens[1].content == '&'
        assert return_tokens[2].content == 'const'

        assert return_tokens[0].kind == TokenType.identifier_
        assert return_tokens[1].kind == TokenType.ref_
        assert return_tokens[2].kind == TokenType.const_

    def test_position_is_not_changed(self):
        tr = TokenReader(source_code='''
            private: virtual A::B::C const* const Bar(
            ''')

        ts = TokenStream(tr)
        ts.forward()
        ts.move_forward_to_token_type(token_type=TokenType.params_begin_)

        saved_token = ts.current_token
        assert len(get_return_part_as_tokens(ts)) > 0
        assert saved_token is ts.current_token
