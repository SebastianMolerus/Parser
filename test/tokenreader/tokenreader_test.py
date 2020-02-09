import unittest
from mock import Mock

from tokenreader import TokenReader
from token_ import TokenType
from token_ import Token

from preproc import Preproc


class Test_TokenReader(unittest.TestCase):

    def test_chars_are_preprocessed_before_use(self):
        mock = Mock(Preproc)
        t = TokenReader(text=" ", preproc=mock)
        mock.Preprocess.assert_called()


    def test_only_spaces(self):
        t = TokenReader(text="\n   \t   ")
        end_token = t.get_next_token()
        self.assertEqual(end_token, Token(TokenType._eof))


    def test_floor_is_part_of_alnum(self):
        t = TokenReader(text="a_aa bbb")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._identifier, 'a_aa'))


    def test_not_alnum_is_not_part_of_identifier_token(self):
        t = TokenReader(text="bbb&ccc")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._identifier, 'bbb'))


    def test_oneline_commented_code(self):
        t = TokenReader(text='''// bbb
        aaa
        ''')
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._identifier, 'aaa'))


    def test_multiline_commented_code(self):
        t = TokenReader(text='''\
        /* bbb
        aaa
        */
        ccc
        ''')
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._identifier, 'ccc'))


    def test_namespace_token(self):
        t = TokenReader(text="namespace")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._namespace))


    def test_class_token(self):
        t = TokenReader(text="class")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._class))


    def test_struct_token(self):
        t = TokenReader(text="struct")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._struct))


    def test_semicolon_token(self):
        t = TokenReader(text=";")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._semicolon))


    def test_colon_token(self):
        t = TokenReader(text=":")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._colon))


    def test_opening_bracket_token(self):
        t = TokenReader(text="{")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._opening_bracket))


    def test_closing_bracket_token(self):
        t = TokenReader(text="}")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._closing_bracket))


    def test_params_begin_token(self):
        t = TokenReader(text="(")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._params_begin))


    def test_params_end_token(self):
        t = TokenReader(text=")")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._params_end))


    def test_public_token(self):
        t = TokenReader(text="public")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._public))


    def test_private_token(self):
        t = TokenReader(text="private")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._private))


    def test_protected_token(self):
        t = TokenReader(text="protected")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._protected))


    def test_comma_token(self):
        t = TokenReader(text=",")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._comma))


    def test_star_token(self):
        t = TokenReader(text="*")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._star))


    def test_ref_token(self):
        t = TokenReader(text="&")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._ref))


    def test_tilde_token(self):
        t = TokenReader(text="~")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._tilde))


    def test_const_token(self):
        t = TokenReader(text="const")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._const))


    def test_equal_token(self):
        t = TokenReader(text="=")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._equal))


    def test_typedef_token(self):
        t = TokenReader(text="typedef")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._typedef))


    def test_virtual_token(self):
        t = TokenReader(text="virtual")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._virtual))


    def test_friend_token(self):
        t = TokenReader(text="friend")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._friend))


    def test_template_token(self):
        t = TokenReader(text="template")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._template))


    def test_operator_token(self):
        t = TokenReader(text="operator")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._operator))


    def test_identifierr_token(self):
        t = TokenReader(text="Foo")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._identifier, 'Foo'))


if __name__ == '__main__':
    unittest.main()