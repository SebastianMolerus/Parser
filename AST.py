from tokenstream import TokenStream

from TokenReader import TokenType
from TokenReader import Token
from TokenReader import TokenReader

from Expressions import NamespaceExpression
from Expressions import ClassExpression
from Expressions import CTorExpression
from Expressions import DTorExpression
from Expressions import Expression

class AbstractTreeBuilder:
    def __init__(self, tokenStream):
        self.tokenStream = tokenStream

    def _try_parse_expression(self, context = None):

        CurrentToken = self.tokenStream.currentToken

        if CurrentToken.type == TokenType._namespace:
            return self._parse_namespace(context)

        if CurrentToken.type == TokenType._class:
            return self._parse_class(context)

        if CurrentToken.type == TokenType._params_begin:
            return self._parse_params(context)

        if CurrentToken.type == TokenType._tilde:
            return self._parse_dtor(context)

        return None

    def build_ast(self):

        ASTTree = Expression("Root")

        while self.tokenStream.next():
            expr = self._try_parse_expression(ASTTree)
            if expr is not None:
                ASTTree.attach(expr)

        return ASTTree


    def _current_type(self):
        return self.tokenStream.currentToken.type


    def _current_content(self):
        return self.tokenStream.currentToken.content


    def _parse_namespace(self, context):

        # we have "namespace" already
        # go next
        self.tokenStream.next()

        # consume identifier
        if self._current_type() != TokenType._identifier:
            raise Exception("Identifier expected after namespace keyword")

        # we have identifier
        parsed_namespace  = NamespaceExpression(self._current_content())
        
        self.tokenStream.next()

        if self._current_type() != TokenType._opening_bracket:
            raise Exception("No opening brackets after namespace identifier")

        # currentToken == token.opening_brackets

        while self.tokenStream.next():

            # we're done
            if self._current_type() == TokenType._closing_bracket:
                break

            expr = self._try_parse_expression(parsed_namespace)
            if expr is None:
                continue
            print "Node {} added into {}.".format(expr._identifier ,parsed_namespace._identifier)
            parsed_namespace.attach(expr)

        return parsed_namespace


    def _parse_class(self, context):
        # we have class already
        # go next
        self.tokenStream.next()

        # consume identifier
        if self._current_type() != TokenType._identifier:
            raise Exception("Identifier expected after class keyword")

        # we have identifier
        parsedClass = ClassExpression(self._current_content())

        self.tokenStream.next()

        # we have something...

        # ...maybe forwarded class
        if self._current_type() == TokenType._semicolon:
            return None

        # ...move after opening bracket
        while self._current_type() != TokenType._opening_bracket:
            self.tokenStream.next()

        # currentToken == token.opening_brackets

        while self.tokenStream.next():

            # we're done
            if self._current_type() == TokenType._closing_bracket:
                break
            expr = self._try_parse_expression(parsedClass)
            if expr is None:
                continue
            print "Node {} added into {}.".format(expr._identifier ,parsedClass._identifier)
            parsedClass.attach(expr)

        return parsedClass


    def _parse_params(self, context):
        """Used for parsing methods, ctors etc..."""
        self._parse_ctor(context)

    def _parse_ctor(self, context):
        cTorName = context._identifier + "()"
        strParams = ''
        if self._giveMethodName() != context._identifier:
            return None

        if self._current_type() != TokenType._params_begin:
            return None
        self.tokenStream.next()

        while self._current_type() != TokenType._params_end:
            #Ugly?! I know that... ;d
            if (self._current_type() == TokenType._ref) or (self._current_type() == TokenType._star):
                pass
            else:
                strParams += ' '
            strParams += self._current_content()
            self.tokenStream.next()
        self.tokenStream.next()

        if self._current_type() == TokenType._semicolon:
            parsedCtor = CTorExpression(cTorName, strParams)
            context.attach(parsedCtor)
        else:
            while self._current_type() != TokenType._closing_bracket:
                self.tokenStream.next()

    def _parse_dtor(self, context):
        dTorName = "~" + context._identifier + "()"

        if self._current_type() != TokenType._tilde:
            return None
        self.tokenStream.next()
        self.tokenStream.next()

        if self._current_type() != TokenType._params_begin:
            return None
        
        while self._current_type() != TokenType._params_end:
            self.tokenStream.next()

        self.tokenStream.next()

        if self._current_type() == TokenType._semicolon:
            parsedDtor = DTorExpression(dTorName)
            context.attach(parsedDtor)
        else:
            while self._current_type() != TokenType._closing_bracket:
                self.tokenStream.next()

    def _giveMethodName(self):
        methodName = ''
        if self._current_type() == TokenType._params_begin:
            self.tokenStream.prev()
            methodName += self._current_content()
            self.tokenStream.next()
        return methodName

# p = TokenReader(text="""\
#     namespace NS0{
# 	namespace NS1
# 	{
# 		class C1{};
# 		class C2{class C12{}
# 			class C4{
#                 Hello();
#                 C4(int a, int* pWsk, char &ref);
#                 ~C4();

# 				class C5{
# 					class C6{
#                         C6 {}
# 					class C10;};
# 				}
# 			}
# 			class C3;
# 			class C7{}
# 		}}}

#     namespace NS4{
#         class C11{}
#     }
#     """)

# a = AbstractTreeBuilder(TokenStream(p))

# expr =  a.build_ast()
# print expr