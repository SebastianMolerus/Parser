import unittest

from TokenReader import TokenReader
from TokenReader import TokenType

class Test_TokenReader(unittest.TestCase):
    def test_GetTokenClassForwardDeclared(self):
        reader = TokenReader(Text="class A;")
        token1 = reader.GetToken()
        token2 = reader.GetToken()
        token3 = reader.GetToken()

        self.assertEqual(token1.type, TokenType._class)

        self.assertEqual(token2.type, TokenType._identifier)
        self.assertEqual(token2.content, "A")

        self.assertEqual(token3.type, TokenType._semicolon)
        self.assertEqual(token3.content, "")

    def test_GetTokenCommented(self):
        reader = TokenReader(Text="//class A;")
        token1 = reader.GetToken()

        self.assertEqual(token1.type, TokenType._eof)

    def test_GetTokenClassDefinition(self):
        reader = TokenReader(Text=r"//class A;    \n\
                                    class B{};     ")
        token1 = reader.GetToken()
        token2 = reader.GetToken()
        token3 = reader.GetToken()
        token4 = reader.GetToken()
        token5 = reader.GetToken()

        self.assertEqual(token1.type, TokenType._class)

        self.assertEqual(token2.type, TokenType._identifier)
        self.assertEqual(token2.content, "B")

        self.assertEqual(token3.type, TokenType._opening_bracket)

        self.assertEqual(token4.type, TokenType._closing_bracket)

        self.assertEqual(token5.type, TokenType._semicolon)


def main():
    unittest.main()