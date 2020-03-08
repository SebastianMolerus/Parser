import unittest
from TreeBuilder.expressions import MethodExpression
from TreeBuilder.expressions import ClassExpression
from TreeBuilder.parsing import build_ast
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream


class Test_AstMethod(unittest.TestCase):

    def test_MethodParsingreturn_part0(self):
        tr = TokenReader(source_code="""
        class Foo{
            public:
            uint_32 const* Bar(int* a);
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'uint_32 const*')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingreturn_part1(self):
        tr = TokenReader(source_code="""
        class Foo{
            public:
            A::B const* Bar(int* a);
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'A::B const*')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingreturn_part2(self):
        tr = TokenReader(source_code="""
        class Foo{
            public:
            G const* Bar(int* a);
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'G const*')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingreturn_part3(self):
        tr = TokenReader(source_code="""
        class Foo{
            public:
            G::B const* Bar(int* a);
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'G::B const*')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingreturn_part4(self):
        tr = TokenReader(source_code="""
        class Foo{
            public:
            Foo();
            int Bar(int* a);
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertTrue(isinstance(tree[2], MethodExpression))
        self.assertEqual(tree[2].identifier, 'Bar')
        self.assertEqual(tree[2].parameters, 'int* a')
        self.assertEqual(tree[2].return_part, 'int')
        self.assertFalse(tree[2].is_const)

    def test_MethodParsingreturn_part5(self):
        tr = TokenReader(source_code="""
        class Foo{
            public:
            Foo(){}
            int Bar(int* a);
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'int')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingreturn_part6(self):
        tr = TokenReader(source_code="""
        class Foo{
            public:
            Foo(){}
            int const* const Bar(int* a);
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'int const* const')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingreturn_part7(self):
        tr = TokenReader(source_code="""
        class Foo{
            public:
            Foo(){}
            A::B const* const Bar(int* a);
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'A::B const* const')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingreturn_part8(self):
        tr = TokenReader(source_code="""
        class Foo{
            public:
            Foo(){}
            A::B const& const Bar(int* a);
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'A::B const& const')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingParameters0(self):
        tr = TokenReader(source_code="""
        class Foo{
            public:
            void Bar();
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, '')
        self.assertEqual(tree[1].return_part, 'void')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingParameters1(self):
        tr = TokenReader(source_code="""
        class Foo{
            public:
            void Bar(int* a);
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'void')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingParameters2(self):
        tr = TokenReader(source_code="""
        class Foo{
            public:
            void Bar(int* a, A::B const* value2);
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a, A::B const* value2')
        self.assertEqual(tree[1].return_part, 'void')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingParameters3(self):
        tr = TokenReader(source_code="""
        class Foo{
            public:
            void Bar(int* a, A::B const* value2);
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a, A::B const* value2')
        self.assertEqual(tree[1].return_part, 'void')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingParameters4(self):
        tr = TokenReader(source_code="""
        class Foo{
            public:
            void Bar(int * a);
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'void')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingConstness0(self):
        tr = TokenReader(source_code="""
        class Foo{
            public:
            void Bar(int * a) const;
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertTrue(tree[1].is_const)

    def test_MethodParsingConstness1(self):
        tr = TokenReader(source_code="""
        class Foo{
            public:
            void Bar(int * a) const;
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertTrue(tree[1].is_const)

    def test_PrivateMethodsByDefaultNotParsed(self):
        tr = TokenReader(source_code="""
        class Foo{
            private:
            typedef (*a)(*a);
            void Bar();
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 1)
        self.assertTrue(tree[0] == ClassExpression("Foo"))

    def test_VirtualMethod(self):
        tr = TokenReader(source_code="""
        class Foo{
            private:
            void bar1();
            public:
            virtual void bar2() const = 0;
            virtual void bar3() const;
            virtual void bar4() const
            {

            }
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression("Foo"))
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'bar3')
        self.assertEqual(tree[1].parameters, '')
        self.assertEqual(tree[1].return_part, 'void')

    def test_ClassWithFriend(self):
        tr = TokenReader(source_code="""
        class Foo{
            friend class Fos;
            public:
            void bar1();
            private:
            virtual void bar2() const = 0;
            virtual void bar3() const;
            virtual void bar4() const
            {

            }
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 3)
        self.assertEqual(tree[0], ClassExpression("Foo"))

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'bar1')
        self.assertEqual(tree[1].parameters, '')
        self.assertEqual(tree[1].return_part, 'void')

        self.assertTrue(isinstance(tree[2], MethodExpression))
        self.assertEqual(tree[2].identifier, 'bar3')
        self.assertTrue(tree[2].is_const)
        self.assertEqual(tree[2].parameters, '')
        self.assertEqual(tree[2].return_part, 'void')

    def test_ClassWithoutFriend(self):
        tr = TokenReader(source_code="""
        class Foo{
            private:
            void bar1();
            virtual void bar2() const = 0;
            virtual void bar3() const;
            virtual void bar4() const
            {

            }
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0], ClassExpression("Foo"))
