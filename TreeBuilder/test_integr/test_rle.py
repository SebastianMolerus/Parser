from TreeBuilder.expressions import ClassExpression, NamespaceExpression, MethodExpression
from TreeBuilder.parsing import build_ast
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream


def test_namespace_class_method_implemented_below():
    tr = TokenReader(source_code='''
    namespace N{
    class Foo{
    public:
    void Bar();
    };
    
    void N::Foo::Bar(){
    }
    }
    ''')
    ts = TokenStream(tr)

    tree = build_ast(ts)

    assert len(tree) == 2
    assert isinstance(tree[0], NamespaceExpression)
    assert tree[0].identifier == 'N'

    assert isinstance(tree[1], ClassExpression)
    assert tree[1].identifier == 'Foo'


def test_class_method_implemented_below():
    tr = TokenReader(source_code='''
    namespace N{
    class Foo{
    public:
    void Bar();
    };

    void Foo::Bar(){
    }
    }
    ''')
    ts = TokenStream(tr)

    tree = build_ast(ts)

    assert len(tree) == 2
    assert isinstance(tree[0], NamespaceExpression)
    assert tree[0].identifier == 'N'

    assert isinstance(tree[1], ClassExpression)
    assert tree[1].identifier == 'Foo'


def test_namespace_class_method_implemented_below_after_namespace():
    tr = TokenReader(source_code='''
    namespace N{
    class Foo{
    public:
    void Bar();
    };
    }

    void N::Foo::Bar(){
    }
    
    ''')
    ts = TokenStream(tr)

    tree = build_ast(ts)

    assert len(tree) == 2
    assert isinstance(tree[0], NamespaceExpression)
    assert tree[0].identifier == 'N'

    assert isinstance(tree[1], ClassExpression)
    assert tree[1].identifier == 'Foo'


def test_function_declared_in_namespace():
    tr = TokenReader(source_code='''
    namespace N{
    void foo(int a);
    }

    void N::foo(int a){
    }
    
    ''')
    ts = TokenStream(tr)

    tree = build_ast(ts)

    assert len(tree) == 1
    assert isinstance(tree[0], NamespaceExpression)
    assert tree[0].identifier == 'N'


def test_namespace_function_declared_and_defined_in_namespace():
    tr = TokenReader(source_code='''
    namespace N{
    void foo(int a);

    void N::foo(int a){}
    }
    ''')
    ts = TokenStream(tr)

    tree = build_ast(ts)

    assert len(tree) == 1
    assert isinstance(tree[0], NamespaceExpression)
    assert tree[0].identifier == 'N'


def test_function_declared_and_defined_in_namespace():
    tr = TokenReader(source_code='''
    namespace N{
    void foo(int a);

    void foo(int a){}
    }
    ''')
    ts = TokenStream(tr)

    tree = build_ast(ts)

    assert len(tree) == 1
    assert isinstance(tree[0], NamespaceExpression)
    assert tree[0].identifier == 'N'


def test_same_function_as_method():
    tr = TokenReader(source_code='''
    namespace N{
    class Bar{
        public:
        void foo();
    };
    void foo(int a);
    void foo(int a)
    {}
    
    ''')
    ts = TokenStream(tr)

    tree = build_ast(ts)

    assert len(tree) == 3
    assert isinstance(tree[0], NamespaceExpression)
    assert tree[0].identifier == 'N'

    assert isinstance(tree[1], ClassExpression)
    assert tree[1].identifier == 'Bar'

    assert isinstance(tree[2], MethodExpression)
    assert tree[2].identifier == 'foo'


