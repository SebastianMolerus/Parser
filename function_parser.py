from token_stream import TokenStream
from token_stream_resto import TokenStreamRestoWrapper
from nodes import functionNode
from parsing import Token



class FunctionParser:
    def __init__(self, token_stream):
        self._stream = token_stream


    # type :==    (n * (identifier + ':' + ':')) + identifier + ( '&' | '*' )
    # A::B::MyType * 
    def _try_parse_type(self):
        
        f = ""
        stream = TokenStreamRestoWrapper(self._stream)
        # get rid of ns:

        while stream.next() and (stream.currentTok.type == Token.tok_identifier or\
            stream.currentTok.type == Token.tok_colon):
            f+=stream.currentTok.content


        stream = TokenStreamRestoWrapper(self._stream)

        while stream.next() and (stream.currentTok.type == Token.tok_identifier or\
            stream.currentTok.type == Token.tok_colon):
            f+=stream.currentTok.content

        
    


            


