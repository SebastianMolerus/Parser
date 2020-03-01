from token_reader import TokenReader
from token_stream import TokenStream
from expressions import Expression
from parsing import parse_expression


class AbstractTreeBuilder:
    def __init__(self, source_code=None, file_path=None):
        if source_code is not None:
            self.tokenReader = TokenReader(text=source_code)
        else:
            self.tokenReader = TokenReader(source_file=file_path)
        self.tokenStream = TokenStream(self.tokenReader)

    def build_ast(self):
        ast_tree = Expression('Root')

        while self.tokenStream.forward():
            expr = parse_expression(self.tokenStream)
            if expr is not None:
                ast_tree.attach(expr)
        return ast_tree
