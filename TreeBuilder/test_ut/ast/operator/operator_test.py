import unittest
from TreeBuilder.expressions import ClassExpression
from TreeBuilder.expressions import OperatorExpression
from TreeBuilder.parsing import build_ast
from TreeBuilder.token_reader import TokenReader
from TreeBuilder.token_stream import TokenStream


class Test_AstOperator(unittest.TestCase):
    def test_OnePublicAssignOperator(self):
        tr = TokenReader(source_code="""
        class A{
            public:
            A& operator =( const A& x );
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertTrue(isinstance(tree[1], OperatorExpression))
        self.assertEqual(tree[1].identifier, 'operator=')
        self.assertEqual(tree[1].parameters, 'const A& x')
        self.assertEqual(tree[1].return_part, 'A&')

    def test_OnePrivateAssignOperator(self):
        tr = TokenReader(source_code="""
        class A{
            private:
            A& operator =( const A& x );
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0], ClassExpression('A'))

    def test_OnePublicImplementedAssignOperator(self):
        tr = TokenReader(source_code="""
        class A{
            public:
            A& operator =( const A& x )
            {
                this->bagno = x.bagno;
                return *this
            }
            private:
            int bagno;
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0], ClassExpression('A'))

    def test_TwoDifferentPublicOperatoros(self):
        tr = TokenReader(source_code="""
        class A{
            public:
            A& operator = ( const A& x );
            A& operator + ( const A& bagno);
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 3)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertTrue(isinstance(tree[1], OperatorExpression))
        self.assertEqual(tree[1].identifier, 'operator=')
        self.assertEqual(tree[1].parameters, 'const A& x')
        self.assertEqual(tree[1].return_part, 'A&')
        self.assertTrue(isinstance(tree[2], OperatorExpression))
        self.assertEqual(tree[2].identifier, 'operator+')
        self.assertEqual(tree[2].parameters, 'const A& bagno')
        self.assertEqual(tree[2].return_part, 'A&')

    def test_OnePublicOperatorWithLongNamespace(self):
        tr = TokenReader(source_code="""
        class A{
            public:
            A::B::C::D::E::F::G::H::I::J::K::L::M::N::O::P& operator =(const A::B::C::D::E:
            :F::G::H::I::J::K::L::M::N::O::P& x);
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertTrue(isinstance(tree[1], OperatorExpression))
        self.assertEqual(tree[1].identifier, 'operator=')
        self.assertEqual(tree[1].parameters, 'const A::B::C::D::E::F::G::H::I::J::K::L::M::N::O::P& x')
        self.assertEqual(tree[1].return_part, 'A::B::C::D::E::F::G::H::I::J::K::L::M::N::O::P&')

    def test_OnePublicOperatorWithGarbageComments(self):
        tr = TokenReader(source_code="""
        class A{
            //Public
            public:
            //A& operator =( const A& x );
            //Komentarz
            /*
            Jestes szalona mowie Ci
            Zawsze nia bylas.
            Skonczysz wreszcie snic?
            */

            //Miala matka syna, syna jedynego
            A& operator + ( const A& bagno); //+ operator
            //Chciala go wychowac na pana wielkiego

            /*
                    A& operator * ( const A& bagno);
            */
        };
        """)
        ts = TokenStream(tr)

        tree = build_ast(ts)

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertTrue(isinstance(tree[1], OperatorExpression))
        self.assertEqual(tree[1].identifier, 'operator+')
        self.assertEqual(tree[1].parameters, 'const A& bagno')
        self.assertEqual(tree[1].return_part, 'A&')
