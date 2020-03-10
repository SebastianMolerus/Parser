from TreeBuilder.parsing_utilities import get_return_part_as_tokens, convert_param_tokens_to_string
from TreeBuilder.tok import TokenType
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream
from mock import Mock


def get_all_tokens(source_code):
    tr = TokenReader(source_code=source_code)
    ts = TokenStream(tr)
    tokens = []
    while ts.forward():
        tokens.append(ts.current_token)
    return tokens


class TestGetReturnPartAsTokensSuite:
    def test_with_semicolon_as_stop(self):
        tr = TokenReader(source_code='''
        ;const A* foo(
        ''')

        ts = TokenStream(tr)
        ts.forward()
        ts.move_forward_to(token_type=TokenType.params_begin_)
        ts.backward()

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
        Bar& const foo(
        ''')

        ts = TokenStream(tr)
        ts.forward()
        ts.move_forward_to(token_type=TokenType.params_begin_)
        ts.backward()

        return_tokens = get_return_part_as_tokens(ts)

        assert len(return_tokens) == 3
        assert return_tokens[0].content == 'Bar'
        assert return_tokens[0].kind == TokenType.identifier_

        assert return_tokens[1].content == '&'
        assert return_tokens[1].kind == TokenType.ref_

        assert return_tokens[2].content == 'const'
        assert return_tokens[2].kind == TokenType.const_

    def test_opening_bracket_as_end_barrier(self):
        token_stream = Mock()
        token_stream.current_kind.return_value = TokenType.opening_bracket_
        token_stream.backward.return_value = True

        assert len(get_return_part_as_tokens(token_stream)) == 0

        assert len(token_stream.mock_calls) == 2
        assert token_stream.current_kind.call_count == 1
        assert token_stream.backward.call_count == 1

    def test_closing_bracket_as_end_barrier(self):
        token_stream = Mock()
        token_stream.current_kind.return_value = TokenType.closing_bracket_
        token_stream.backward.return_value = True

        assert len(get_return_part_as_tokens(token_stream)) == 0

        assert len(token_stream.mock_calls) == 2
        assert token_stream.current_kind.call_count == 1
        assert token_stream.backward.call_count == 1

    def test_semicolon_as_end_barrier(self):
        token_stream = Mock()
        token_stream.current_kind.return_value = TokenType.semicolon_
        token_stream.backward.return_value = True

        assert len(get_return_part_as_tokens(token_stream)) == 0

        assert len(token_stream.mock_calls) == 2
        assert token_stream.current_kind.call_count == 1
        assert token_stream.backward.call_count == 1

    def test_scope_token_is_end_barrier(self):
        tr = TokenReader(source_code='''
        public :void Foo(
        ''')

        ts = TokenStream(tr)
        ts.forward()
        ts.move_forward_to(token_type=TokenType.params_begin_)
        ts.backward()

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
        ts.move_forward_to(token_type=TokenType.params_begin_)
        ts.backward()

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
        ts.move_forward_to(token_type=TokenType.params_begin_)
        ts.backward()

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
        ts.move_forward_to(token_type=TokenType.params_begin_)

        saved_token = ts.current_token
        assert len(get_return_part_as_tokens(ts)) > 0
        assert saved_token is ts.current_token


class TestConvertParamTokensToString:
    def test_reference_is_applied_with_space(self):
        tokens = get_all_tokens("&A")
        assert convert_param_tokens_to_string(tokens) == '& A'

    def test_star_is_applied_with_space(self):
        tokens = get_all_tokens("*A")
        assert convert_param_tokens_to_string(tokens) == '* A'

    def test_colon_is_applied_without_space(self):
        tokens = get_all_tokens(": A")
        assert convert_param_tokens_to_string(tokens) == ':A'

    def test_two_colons_are_applied_without_space(self):
        tokens = get_all_tokens(": : A")
        assert convert_param_tokens_to_string(tokens) == '::A'

    def test_comma_applied_space(self):
        tokens = get_all_tokens("A,B")
        assert convert_param_tokens_to_string(tokens) == 'A, B'

    def test_space_between_identifier_tokens(self):
        tokens = get_all_tokens("A B")
        assert convert_param_tokens_to_string(tokens) == 'A B'

    def test_two_colons_between_identifiers(self):
        tokens = get_all_tokens("A : : B")
        assert convert_param_tokens_to_string(tokens) == 'A::B'

    def test_two_stars_between_identifiers(self):
        tokens = get_all_tokens("A**B")
        assert convert_param_tokens_to_string(tokens) == 'A** B'

    def test_star_ref_between_identifiers(self):
        tokens = get_all_tokens("A*&B")
        assert convert_param_tokens_to_string(tokens) == 'A*& B'

    def test_two_colons_star_and_comma(self):
        tokens = get_all_tokens("A::B*,C")
        assert convert_param_tokens_to_string(tokens) == 'A::B*, C'