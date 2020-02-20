import unittest
from TreeBuilder.atb import AbstractTreeBuilder
from TreeBuilder.expressions import MethodExpression
from TreeBuilder.expressions import ClassExpression


class Test_AstMethod(unittest.TestCase):

    def test_MethodParsingreturn_part0(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            uint_32 const* Bar(int* a);
        };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'uint_32 const*')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingreturn_part1(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            A::B const* Bar(int* a);
        };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'A::B const*')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingreturn_part2(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            G const* Bar(int* a);
        };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'G const*')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingreturn_part3(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            G::B const* Bar(int* a);
        };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'G::B const*')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingreturn_part4(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            Foo();
            int Bar(int* a);
        };
        """).build_ast()

        self.assertTrue(isinstance(tree[2], MethodExpression))
        self.assertEqual(tree[2].identifier, 'Bar')
        self.assertEqual(tree[2].parameters, 'int* a')
        self.assertEqual(tree[2].return_part, 'int')
        self.assertFalse(tree[2].is_const)

    def test_MethodParsingreturn_part5(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            Foo(){}
            int Bar(int* a);
        };
        """).build_ast()

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'int')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingreturn_part6(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            Foo(){}
            int const* const Bar(int* a);
        };
        """).build_ast()

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'int const* const')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingreturn_part7(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            Foo(){}
            A::B const* const Bar(int* a);
        };
        """).build_ast()

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'A::B const* const')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingreturn_part8(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            Foo(){}
            A::B const& const Bar(int* a);
        };
        """).build_ast()

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'A::B const& const')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingParameters0(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            void Bar();
        };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, '')
        self.assertEqual(tree[1].return_part, 'void')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingParameters1(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            void Bar(int* a);
        };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'void')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingParameters2(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            void Bar(int* a, A::B const* value2);
        };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a, A::B const* value2')
        self.assertEqual(tree[1].return_part, 'void')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingParameters3(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            void Bar(int* a, A::B const* value2);
        };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a, A::B const* value2')
        self.assertEqual(tree[1].return_part, 'void')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingParameters4(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            void Bar(int * a);
        };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'Bar')
        self.assertEqual(tree[1].parameters, 'int* a')
        self.assertEqual(tree[1].return_part, 'void')
        self.assertFalse(tree[1].is_const)

    def test_MethodParsingConstness0(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            void Bar(int * a) const;
        };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertTrue(tree[1].is_const)

    def test_MethodParsingConstness1(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            public:
            void Bar(int * a) const;
        };
        """).build_ast()

        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertTrue(tree[1].is_const)

    def test_PrivateMethodsByDefaultNotParsed(self):
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            private:
            typedef (*a)(*a);
            void Bar();
        };
        """).build_ast()

        self.assertEqual(len(tree), 1)
        self.assertTrue(tree[0] == ClassExpression("Foo"))

    def test_VirtualMethod(self):
        tree = AbstractTreeBuilder(source_code="""
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
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression("Foo"))
        self.assertTrue(isinstance(tree[1], MethodExpression))
        self.assertEqual(tree[1].identifier, 'bar3')
        self.assertEqual(tree[1].parameters, '')
        self.assertEqual(tree[1].return_part, 'void')

    def test_ClassWithFriend(self):
        tree = AbstractTreeBuilder(source_code="""
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
        """).build_ast()

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
        tree = AbstractTreeBuilder(source_code="""
        class Foo{
            private:
            void bar1();
            virtual void bar2() const = 0;
            virtual void bar3() const;
            virtual void bar4() const
            {

            }
        };
        """).build_ast()

        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0], ClassExpression("Foo"))
