from tokenstream import TokenStream
from parsing import Token
from nodes import ctorNode
from nodes import AssignOp


class AbstractTreeBuilder:

    def __init__(self, token_stream):
        self._stream = token_stream

    def _parse_inputs(self):

        # assuming this:
        #    |
        # ...(...)...;

        stream = self._stream

        if self._stream.current.type != Token.tok_params_begin:
            raise Exception("Current Token is not params begin")

        inputs = ""

        while stream.next() and stream.current.type != Token.tok_params_end:
            inputs += stream.current.content + " "

        # eat )
        stream.next()

        # ends with this:
        #        |
        # ...(...)...;

        inputs = inputs.strip()
        return inputs



    def _parse_Ctor(self, Context):
        stream = self._stream
        #  |
        # A(...);
        inputs = self._parse_inputs()
 
        #       |     
        # A(...);

        if stream.current.type == Token.tok_semicolon:
            return ctorNode(Context.name, inputs)

        return None

    def _parse_AssignOp(self, Context):
        # we are know about = already
        # Copy Assignment
        #             |
        # A& operator=(...);

        stream = self._stream
        origIndex = stream._currentIndex

        if stream.seek(-2).content == 'operator':


            inputs = self._parse_inputs()

            if stream.current.type == Token.tok_semicolon:
                
                stream._currentIndex = origIndex
                if stream.seek(-3).content == 'void':
                    return AssignOp(inputs, "void")

                if stream.seek(-3).type == Token.tok_ref and\
                    stream.seek(-4).content == Context.name:
                    return AssignOp(inputs, stream.seek(-4).content + stream.seek(-3).content)


        return None



    def TryHard(self, Context = None):
    
        #      |
        #   ...(...)...;
        stream = self._stream
        identifier = stream.seek(-1).content
        origIndex = stream._currentIndex
        objToRet = None

        if Context:
            # in class

            # 1. Ctor
            #  |
            # A(...);
            if identifier == Context.name:
                objToRet = self._parse_Ctor(Context)
               
            # Copy Assignment
            #             |
            # A& operator=(...);
            if identifier == r'=':
                objToRet = self._parse_AssignOp(Context)

    
        stream._currentIndex = origIndex
        return objToRet


       


    # def ParseNamespace(self):

    #     # we have "namespace" already
        
    #     # consume identifier
    #     if self._GetExpression().token() != Token.tok_identifier:
    #         raise Exception("Identifier expected after namespace keyword")

    #     # we have identifier
    #     n = namespaceNode(self._currentExpression.identifier())

    #     # opening bracket consumed
    #     if self._GetExpression().token() != Token.tok_opening_bracket:
    #         raise Exception("No opening brackets after namespace identifier")

    #     # currentToken == token.opening_brackets

    #     # empty namespace
    #     if self._GetExpression().token() == Token.tok_closing_bracket:
    #         return n
     
    #     # we have something
    #     # check for eof
    #     if self._currentExpression.token() == Token.tok_eof:
    #         raise Exception("EOF before namespace closing bracket")

    #     # return something to stream
    #     self._ReturnExpr(self._currentExpression)

    #     # continue parsing, consume closing bracket
    #     while self._GetExpression().token() != Token.tok_closing_bracket:
    #         self._ReturnExpr(self._currentExpression)
    #         n.addChild(self.GetNextNode())

    #     if None in n.childNodes:
    #         n.childNodes.remove(None)

    #     return n

    # def ParseClass(self):
    #     # we have "class/struct" already
        
    #     # consume identifier
    #     if self._GetExpression().token() != Token.tok_identifier:
    #         raise Exception("Identifier expected after class keyword")

    #     # we have identifier
    #     objectName = self._currentExpression.identifier()

    #     # forwarded class
    #     if self._GetExpression().token() == Token.tok_semicolon:
    #         return forwardedClassNode(objectName)

    #     # not forwarded class
    #     # move after opening bracket
    #     while self._currentExpression.token() != Token.tok_opening_bracket:
    #         self._GetExpression()

    #     # currentToken == token.opening_brackets

    #     # empty class
    #     if self._GetExpression().token() == Token.tok_closing_bracket:
    #         if self._GetExpression().token() != Token.tok_semicolon:
    #             raise Exception("Expecting ; after class ending bracket") # consume ;
    #         return classNode(objectName)

    #     # we have something
    #     # check for eof
    #     if self._currentExpression.token() == Token.tok_eof:
    #         raise Exception("EOF before class closing bracket")

    #     # return something to stream
    #     self._ReturnExpr(self._currentExpression)

    #     c = classNode(objectName)
    #     # continue parsing, consume closing brackets
    #     while self._GetExpression().token() != Token.tok_closing_bracket:
    #         self._ReturnExpr(self._currentExpression)
    #         c.addChild(self.GetNextNode())

    #     if self._GetExpression().token() != Token.tok_semicolon:
    #             raise Exception("Expecting ; after class ending bracket") # consume ;

    #     if None in c.childNodes:
    #         c.childNodes.remove(None)

    #     return c

        