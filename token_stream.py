from parsing import Parser
from parsing import Token
from token_expr import TokExpr

class TokenStream:
    def __init__(self, parser):
        self._parser = parser
        self._currTok = None
        self._tokBuffer = []

    def next(self):

        if len(self._tokBuffer) > 0:
            self._get_from_buffer()
        else:
            self._get_from_parser()

        if self._currTok.type == Token.tok_eof:
            return False

        return True

    def _get_from_buffer(self):
        self._currTok = self._tokBuffer.pop(0)

    def _get_from_parser(self):
        tokType = self._parser.GetToken()
        cont = self._parser.identifier
        self._currTok = TokExpr(tokType, cont)
    
    @property
    def currentTok(self):
        return self._currTok

    def returnTok(self, tok):
        self._tokBuffer.insert(0, tok)
        self._currTok = None