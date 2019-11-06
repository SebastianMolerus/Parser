from parsing import Parser
from parsing import Token
from nodes import namespaceNode
from nodes import classNode
from nodes import functionNode

class AbstractTreeBuilder:

    def __init__(self, parser):
        self._p = parser
        self._expressionBuffer = []
        self._currentExpression = None
        self._lastNode = None

    @classmethod
    def FromTxt(cls, txt):
        _p = Parser(Text=txt)
        return cls(_p)

    @classmethod
    def FromFile(cls, file):
        _p = Parser(fileName=file)
        return cls(_p)

    def _GetExpression(self):

        if len(self._expressionBuffer) > 0:
            self._currentExpression = self._expressionBuffer.pop(0)
        else:
            self._currentExpression = expr(self._p.GetToken(), self._p.identifier)
        return self._currentExpression

    def _ReturnExpr(self, expression):
        self._expressionBuffer.insert(0, expression)


    def GetNextNode(self):

        while self._GetExpression().token() != Token.tok_eof:      

            if self._currentExpression.token() == Token.tok_class:
                self._lastNode =  self.ParseClass()
                return self._lastNode
            if self._currentExpression.token() == Token.tok_namespace:
                self._lastNode = self.ParseNamespace()
                return self._lastNode

            self._ReturnExpr(self._currentExpression)
            self._lastNode = self.TryParseFunction()
            if self._lastNode is not None:
                return self._lastNode
            else:
                return self.GetNextNode()


    def TryParseFunction(self):
    
        consumedExpressions = []

        # eating tokens till ;
        while self._GetExpression().token() != Token.tok_eof:

            if self._currentExpression.token() != Token.tok_semicolon:
                consumedExpressions.append(self._currentExpression)
                for expr in consumedExpressions:
                    # inline method
                    if expr.token() == Token.tok_closing_bracket:
                        return None
            else:
                # we have semicolon
                fn = None
                for index, expr in enumerate(consumedExpressions):
                    if expr.token() == Token.tok_params_begin:
                        # we have method
                        fn = functionNode(consumedExpressions[index-1].identifier())
                        continue
                    if fn is not None:
                        if expr.token() != Token.tok_params_end:
                            fn.params += " " + expr.identifier()

                if fn is not None:
                    fn.params = fn.params.strip()
                    return fn
            
        # return all ?
        # for exp in reversed(consumedExpressions):
        #     self._ReturnExpr(exp)
        
        return None

    def ParseNamespace(self):

        # we have "namespace" already
        
        # consume identifier
        if self._GetExpression().token() != Token.tok_identifier:
            raise Exception("Identifier expected after namespace keyword")

        # we have identifier
        n = namespaceNode(self._currentExpression.identifier())

        # opening bracket consumed
        if self._GetExpression().token() != Token.tok_opening_bracket:
            raise Exception("No opening brackets after namespace identifier")

        # currentToken == token.opening_brackets

        # empty namespace
        if self._GetExpression().token() == Token.tok_closing_bracket:
            return n
     
        # we have something
        # check for eof
        if self._currentExpression.token() == Token.tok_eof:
            raise Exception("EOF before namespace closing bracket")

        # return something to stream
        self._ReturnExpr(self._currentExpression)

        # continue parsing, consume closing bracket
        while self._GetExpression().token() != Token.tok_closing_bracket:
            self._ReturnExpr(self._currentExpression)
            n.addChild(self.GetNextNode())

        if None in n.childNodes:
            n.childNodes.remove(None)

        return n

    def ParseClass(self):
        # we have "class/struct" already
        
        # consume identifier
        if self._GetExpression().token() != Token.tok_identifier:
            raise Exception("Identifier expected after class keyword")

        # we have identifier
        objectName = self._currentExpression.identifier()

        # forwarded class
        if self._GetExpression().token() == Token.tok_semicolon:
            return forwardedClassNode(objectName)

        # not forwarded class
        # move after opening bracket
        while self._currentExpression.token() != Token.tok_opening_bracket:
            self._GetExpression()

        # currentToken == token.opening_brackets

        # empty class
        if self._GetExpression().token() == Token.tok_closing_bracket:
            if self._GetExpression().token() != Token.tok_semicolon:
                raise Exception("Expecting ; after class ending bracket") # consume ;
            return classNode(objectName)

        # we have something
        # check for eof
        if self._currentExpression.token() == Token.tok_eof:
            raise Exception("EOF before class closing bracket")

        # return something to stream
        self._ReturnExpr(self._currentExpression)

        c = classNode(objectName)
        # continue parsing, consume closing brackets
        while self._GetExpression().token() != Token.tok_closing_bracket:
            self._ReturnExpr(self._currentExpression)
            c.addChild(self.GetNextNode())

        if self._GetExpression().token() != Token.tok_semicolon:
                raise Exception("Expecting ; after class ending bracket") # consume ;

        if None in c.childNodes:
            c.childNodes.remove(None)

        return c

        