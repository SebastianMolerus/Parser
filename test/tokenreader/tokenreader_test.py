import unittest
from mock import Mock

from tokenreader import TokenReader
from token_ import TokenType
from token_ import Token

from preproc import Preproc


class Test_TokenReader(unittest.TestCase):

    def test_chars_are_preprocessed_before_use(self):
        mock = Mock(Preproc)
        t = TokenReader(text=" ", pre_process=mock)
        mock.Preprocess.assert_called()

    def test_only_spaces(self):
        t = TokenReader(text="\n   \t   ")
        end_token = t.get_next_token()
        self.assertEqual(end_token, Token(TokenType.eof_))

    def test_floor_is_part_of_alnum(self):
        t = TokenReader(text="a_aa bbb")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.identifier_, 'a_aa'))

    def test_not_alnum_is_not_part_of_identifier_token(self):
        t = TokenReader(text="bbb&ccc")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.identifier_, 'bbb'))

    def test_oneline_commented_code(self):
        t = TokenReader(text='''// bbb
        aaa
        ''')
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.identifier_, 'aaa'))

    def test_multiline_commented_code(self):
        t = TokenReader(text='''\
        /* bbb
        aaa
        */
        ccc
        ''')
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.identifier_, 'ccc'))

    def test_namespace_token(self):
        t = TokenReader(text="namespace")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.namespace_))

    def test_class_token(self):
        t = TokenReader(text="class")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.class_))

    def test_struct_token(self):
        t = TokenReader(text="struct")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.struct_))

    def test_semicolon_token(self):
        t = TokenReader(text=";")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.semicolon_))

    def test_colon_token(self):
        t = TokenReader(text=":")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.colon_))

    def test_opening_bracket_token(self):
        t = TokenReader(text="{")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.opening_bracket_))

    def test_closing_bracket_token(self):
        t = TokenReader(text="}")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.closing_bracket_))

    def test_params_begin_token(self):
        t = TokenReader(text="(")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.params_begin_))

    def test_params_end_token(self):
        t = TokenReader(text=")")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.params_end_))

    def test_public_token(self):
        t = TokenReader(text="public")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.public_))

    def test_private_token(self):
        t = TokenReader(text="private")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.private_))

    def test_protected_token(self):
        t = TokenReader(text="protected")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.protected_))

    def test_comma_token(self):
        t = TokenReader(text=",")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.comma_))

    def test_star_token(self):
        t = TokenReader(text="*")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.star_))

    def test_ref_token(self):
        t = TokenReader(text="&")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.ref_))

    def test_tilde_token(self):
        t = TokenReader(text="~")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.tilde_))

    def test_const_token(self):
        t = TokenReader(text="const")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.const_))

    def test_equal_token(self):
        t = TokenReader(text="=")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.equal_))

    def test_typedef_token(self):
        t = TokenReader(text="typedef")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.typedef_))

    def test_virtual_token(self):
        t = TokenReader(text="virtual")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.virtual_))

    def test_friend_token(self):
        t = TokenReader(text="friend")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.friend_))

    def test_template_token(self):
        t = TokenReader(text="template")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.template_))

    def test_operator_token(self):
        t = TokenReader(text="operator")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.operator_))

    def test_typename_token(self):
        t = TokenReader(text="typename")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.typename_))

    def test_identifier_token(self):
        t = TokenReader(text="Foo")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.identifier_, 'Foo'))


if __name__ == '__main__':
    unittest.main()