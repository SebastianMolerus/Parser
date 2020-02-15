from tokrdr import TokenReader
from tokenstream import TokenStream
from expressions import Expression
from Parsing.stateBuilder import StateParserBuilder


class AbstractTreeBuilder:
    def __init__(self, source_code=None, file_path=None):
        if source_code is not None:
            self.tokenReader = TokenReader(text=source_code)
        else:
            self.tokenReader = TokenReader(source_file=file_path)
        self.tokenStream = TokenStream(self.tokenReader)

    def build_ast(self):
        ast_tree = Expression('Root')

        state_parser = StateParserBuilder(self.tokenStream).\
            add_namespace_parsing().\
            add_class_parsing()\
            .get_product()

        while self.tokenStream.next():
            expr = state_parser.process()
            if expr is not None:
                ast_tree.attach(expr)
        return ast_tree
