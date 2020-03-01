from TreeBuilder.expressions import ClassExpression
from TreeBuilder.parsing import parse_class
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream


def test_empty_class():
    tr = TokenReader(source_code='''
    class A {
    }
    ''')
    ts = TokenStream(tr)
    ts.forward()

    parsed_class = parse_class(ts)

    assert parsed_class.identifier == 'A'
    assert isinstance(parsed_class, ClassExpression)
    assert len(parsed_class) == 0
