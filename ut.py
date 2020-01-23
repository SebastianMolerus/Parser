import unittest


from TokenReader import TokenReader
from TokenReader import TokenType


# ------------------------------------------------------------
# ------------------- HELPER METHODS -------------------------


def _TokenReader_get_all_tokens(TokenReader):
    tokens = []
    while True:
        token = TokenReader.GetNextToken()
        if token.type == TokenType._eof:
            break
        tokens.append(token)

    return tokens


# ------------------------------------------------------------
# --------------------- TESTS --------------------------------


class Test_TokenReader(unittest.TestCase):
    def test_GetNextTokenClassForwardDeclared(self):
        reader = TokenReader(text="class A;")
        token1 = reader.GetNextToken()
        token2 = reader.GetNextToken()
        token3 = reader.GetNextToken()

        self.assertEqual(token1.type, TokenType._class)

        self.assertEqual(token2.type, TokenType._identifier)
        self.assertEqual(token2.content, "A")

        self.assertEqual(token3.type, TokenType._semicolon)
        self.assertEqual(token3.content, ";")


    def test_GetNextTokenCommented(self):
        reader = TokenReader(text="//class A;")
        token1 = reader.GetNextToken()

        self.assertEqual(token1.type, TokenType._eof)


    def test_GetNextTokenClassDefinition(self):
        reader = TokenReader(text=""" //class A;
                                      class B{};     """)
        token1 = reader.GetNextToken()
        token2 = reader.GetNextToken()
        token3 = reader.GetNextToken()
        token4 = reader.GetNextToken()
        token5 = reader.GetNextToken()

        self.assertEqual(token1.type, TokenType._class)

        self.assertEqual(token2.type, TokenType._identifier)
        self.assertEqual(token2.content, "B")

        self.assertEqual(token3.type, TokenType._opening_bracket)

        self.assertEqual(token4.type, TokenType._closing_bracket)

        self.assertEqual(token5.type, TokenType._semicolon)


    def test_GetNextTokenMethodDefinition1(self):
        reader = TokenReader(text=r"void Foo::Bar(uint32_t& ref, int * ptr) const;")
        tokens = _TokenReader_get_all_tokens(reader)

        self.assertEqual(len(tokens), 13)

        self.assertEqual(tokens[0].type, TokenType._identifier)
        self.assertEqual(tokens[0].content, "void")

        self.assertEqual(tokens[1].type, TokenType._identifier)
        self.assertEqual(tokens[1].content, "Foo::Bar")

        self.assertEqual(tokens[2].type, TokenType._params_begin)
        self.assertEqual(tokens[2].content, "(")

        self.assertEqual(tokens[3].type, TokenType._identifier)
        self.assertEqual(tokens[3].content, "uint32_t")

        self.assertEqual(tokens[4].type, TokenType._ref)
        self.assertEqual(tokens[4].content, "&")

        self.assertEqual(tokens[5].type, TokenType._identifier)
        self.assertEqual(tokens[5].content, "ref")

        self.assertEqual(tokens[6].type, TokenType._comma)
        self.assertEqual(tokens[6].content, ",")

        self.assertEqual(tokens[7].type, TokenType._identifier)
        self.assertEqual(tokens[7].content, "int")

        self.assertEqual(tokens[8].type, TokenType._star)
        self.assertEqual(tokens[8].content, "*")

        self.assertEqual(tokens[9].type, TokenType._identifier)
        self.assertEqual(tokens[9].content, "ptr")

        self.assertEqual(tokens[10].type, TokenType._params_end)
        self.assertEqual(tokens[10].content, ")")

        self.assertEqual(tokens[11].type, TokenType._const)
        self.assertEqual(tokens[11].content, "const")

        self.assertEqual(tokens[12].type, TokenType._semicolon)
        self.assertEqual(tokens[12].content, ";")


    def test_GetNextTokenEoF(self):
        reader = TokenReader(text=r"//void Foo::Bar(uint32_t& ref, int * ptr) const;")
        token = reader.GetNextToken()

        self.assertEqual(token.type, TokenType._eof)
        self.assertEqual(token.content, "")


def main():
    unittest.main()