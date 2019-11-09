from token_stream_resto import TokenStreamRestoWrapper
from parsing import Parser
from parsing import Token
from token_expr import TokExpr

class TokenStreamSeekerWrapper(TokenStreamRestoWrapper):
    def __init__(self, token_stream):
        TokenStreamRestoWrapper.__init__(self, token_stream)

    def seek(self, count):

        c = []
        for i in range(count):

            if self._wrappee._currTok.type == Token.tok_eof:
                break

            c.append(self._wrappee._get_from_parser())

        for i in c:
            self._wrappee._tokBuffer.insert(0, i)
        return c[len(c)-1]

        



