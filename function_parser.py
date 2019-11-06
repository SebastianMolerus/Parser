from token_stream import TokenStream
from nodes import functionNode
from parsing import Token

class FunctionParser:
    def __init__(self, token_stream):
        self._stream = token_stream

    def try_get_function(self):
        pass        

        # go till eof
        # while self._stream.next():

        #     if self._stream.currentTok.type == Token.tok_semicolon:

