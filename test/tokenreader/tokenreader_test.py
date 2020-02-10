import unittest
from parameterized import parameterized

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

    def test_identifier_token(self):
        t = TokenReader(text="Foo")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType.identifier_, 'Foo'))

    @parameterized.expand([
        ('namespace', TokenType.namespace_),
        ('class', TokenType.class_),
        ('struct', TokenType.struct_),
        (';', TokenType.semicolon_),
        (':', TokenType.colon_),
        ('{', TokenType.opening_bracket_),
        ('}', TokenType.closing_bracket_),
        ('(', TokenType.params_begin_),
        (')', TokenType.params_end_),
        ('public', TokenType.public_),
        ('private', TokenType.private_),
        ('protected', TokenType.protected_),
        (',', TokenType.comma_),
        ('e0f', TokenType.eof_),
        ('&', TokenType.ref_),
        ('*', TokenType.star_),
        ('#', TokenType.hash_),
        ('~', TokenType.tilde_),
        ('const', TokenType.const_),
        ('=', TokenType.equal_),
        ('typedef', TokenType.typedef_),
        ('typename', TokenType.typename_),
        ('virtual', TokenType.virtual_),
        ('friend', TokenType.friend_),
        ('template', TokenType.template_),
        ('operator', TokenType.operator_),
    ])
    def test_different_token_kind(self, identifier, token_type):
        t = TokenReader(text=identifier)
        token = t.get_next_token()
        self.assertEqual(token, Token(token_type))


if __name__ == '__main__':
    unittest.main()