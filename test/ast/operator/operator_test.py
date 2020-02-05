import unittest
from expressions import *
from ast import *

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