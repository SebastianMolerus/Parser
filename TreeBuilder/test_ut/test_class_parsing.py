import pytest
from TreeBuilder.expressions import ClassExpression, MethodExpression
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


def test_not_identifier_token_after_class_keyword():
    tr = TokenReader(source_code='''
    class class { }
    ''')
    ts = TokenStream(tr)
    ts.forward()

    with pytest.raises(Exception):
        parse_class(ts)


def test_forwarded_class():
    tr = TokenReader(source_code='''
    class A;
    ''')
    ts = TokenStream(tr)
    ts.forward()

    assert parse_class(ts) is None


def test_class_inheritance():
    tr = TokenReader(source_code='''
    class A : public B{};
    ''')
    ts = TokenStream(tr)
    ts.forward()

    parsed_class = parse_class(ts)

    assert parsed_class.identifier == 'A'
    assert isinstance(parsed_class, ClassExpression)


def test_class_with_child():
    tr = TokenReader(source_code='''
    class A{
    public:
        void Foo();
    }
    ''')
    ts = TokenStream(tr)
    ts.forward()

    parsed_class = parse_class(ts)

    assert parsed_class.identifier == 'A'
    assert isinstance(parsed_class, ClassExpression)
    assert len(parsed_class) == 1
    assert isinstance(parsed_class[0], MethodExpression)


def test_class_with_child_in_private_section():
    tr = TokenReader(source_code='''
    class A{
        void Foo();
    }
    ''')
    ts = TokenStream(tr)
    ts.forward()

    parsed_class = parse_class(ts)

    assert parsed_class.identifier == 'A'
    assert isinstance(parsed_class, ClassExpression)
    assert len(parsed_class) == 0


def test_class_with_child_in_private_section_but_with_friend():
    tr = TokenReader(source_code='''
    class A{
    friend class B;
        void Foo();
    }
    ''')
    ts = TokenStream(tr)
    ts.forward()

    parsed_class = parse_class(ts)

    assert parsed_class.identifier == 'A'
    assert isinstance(parsed_class, ClassExpression)
    assert len(parsed_class) == 1
    assert isinstance(parsed_class[0], MethodExpression)

