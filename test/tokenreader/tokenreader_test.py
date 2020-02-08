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
        t = TokenReader(text="      ")
        end_token = t.get_next_token()
        self.assertEqual(end_token, Token(TokenType._eof))


    def test_floor_is_part_of_alnum(self):
        t = TokenReader(text="aaa_  ")
        token = t.get_next_token()
        self.assertEqual(token, Token(TokenType._identifier, 'aaa_'))


    def test_not_alnum_is_not_part_of_token(self):
        t = TokenReader(text="bbb!b")
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


if __name__ == '__main__':
    unittest.main()