import unittest
from expressions import *
from atb import *

class Test_AstOperator(unittest.TestCase):


    def test_OnePublicAssignOperator(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            public:
            A& operator =( const A& x );
        };
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertTrue(isinstance(tree[1], OperatorExpression))
        self.assertEqual(tree[1]._identifier, '=')
        self.assertEqual(tree[1]._parameters, 'const A& x')
        self.assertEqual(tree[1]._returns, 'A&')

    def test_OnePrivateAssignOperator(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            private:
            A& operator =( const A& x );
        };
        """).build_ast()

        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0], ClassExpression('A'))

    def test_OnePublicImplementedAssignOperator(self):
        tree = AbstractTreeBuilder(source_code="""
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
        """).build_ast()

        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0], ClassExpression('A'))


    def test_TwoDifferentPublicOperatoros(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            public:
            A& operator =( const A& x );
            A& operator + ( const A& bagno);
        };
        """).build_ast()

        self.assertEqual(len(tree), 3)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertTrue(isinstance(tree[1], OperatorExpression))
        self.assertEqual(tree[1]._identifier, '=')
        self.assertEqual(tree[1]._parameters, 'const A& x')
        self.assertEqual(tree[1]._returns, 'A&')
        self.assertTrue(isinstance(tree[2], OperatorExpression))
        self.assertEqual(tree[2]._identifier, '+')
        self.assertEqual(tree[2]._parameters, 'const A& bagno')
        self.assertEqual(tree[2]._returns, 'A&')
    
    def test_OnePublicOperatorWithLongNamespace(self):
        tree = AbstractTreeBuilder(source_code="""
        class A{
            public:
            A::B::C::D::E::F::G::H::I::J::K::L::M::N::O::P& operator =(const A::B::C::D::E::F::G::H::I::J::K::L::M::N::O::P& x);
        };
        """).build_ast()
        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertTrue(isinstance(tree[1], OperatorExpression))
        self.assertEqual(tree[1]._identifier, '=')
        self.assertEqual(tree[1]._parameters, 'const A::B::C::D::E::F::G::H::I::J::K::L::M::N::O::P& x')
        self.assertEqual(tree[1]._returns, 'A::B::C::D::E::F::G::H::I::J::K::L::M::N::O::P&')


    def test_OnePublicOperatorWithGarbageComments(self):
        tree = AbstractTreeBuilder(source_code="""
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
        """).build_ast()

        self.assertEqual(len(tree), 2)
        self.assertEqual(tree[0], ClassExpression('A'))
        self.assertTrue(isinstance(tree[1], OperatorExpression))
        self.assertEqual(tree[1]._identifier, '+')
        self.assertEqual(tree[1]._parameters, 'const A& bagno')
        self.assertEqual(tree[1]._returns, 'A&')

        