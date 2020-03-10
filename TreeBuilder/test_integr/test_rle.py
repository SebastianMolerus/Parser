from TreeBuilder.expressions import ClassExpression
from TreeBuilder.parsing import build_ast
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream


def test_method_implemented_below():
    tr = TokenReader(source_code='''
    class Foo{
    public:
    void Bar();
    };
    
    void Foo::Bar(){
    }
    
    ''')
    ts = TokenStream(tr)

    tree = build_ast(ts)

    assert len(tree) == 1
    assert isinstance(tree[0], ClassExpression)


def test_delete_me():
    tr = TokenReader(source_code='''
    class Foo{
    public:
    void Bar();
    };

    void Foo::Bar(){
    }

    ''')
    ts = TokenStream(tr)

    tree = build_ast(ts)

    assert len(tree) == 1
    assert isinstance(tree[0], ClassExpression)
