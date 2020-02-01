from tokenstream import *
from tokenreader import *
from expressions import *


class AbstractTreeBuilder:
    def __init__(self, source_code = None, file = None):

        if source_code is not None:
            self.tokenReader = TokenReader(text=source_code)
        else:
            self.tokenReader = TokenReader(fileName=file)

        self.tokenStream = TokenStream(self.tokenReader)


    def build_ast(self):

        ASTTree = None

        while self.tokenStream.next():
            expr = self._try_parse_expression(ASTTree)
            if expr is not None:
                if ASTTree is None:
                    ASTTree = expr
                else:
                    ASTTree.attach(expr)

        return ASTTree


    def _try_parse_expression(self, context = None):
        '''Main dispatch method for all expresions.
        
        Every method called from here should return 
        
        Expression if parsed succesfull

        or None
        
        '''

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
            
            # take care of public, prot, private
            parsedClass._set_scope_from_scope_token(self._current_type())

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
        """Used as dispatch method for parsing
        
        everything from TokenType._params_begin
        
        """

        #Mozna sprobowac takie cos. To tylko przyklad ale smiga
        if self._isCtor(context):
            return self._parse_ctor(context)
        else:
            return self._parse_method(context) 
 
        # parsedExpr = self._parse_ctor(context) 
        # if parsedExpr is not None:
        #     return parsedExpr

        # parsedExpr = self._parse_method(context) 
        # if parsedExpr is not None:
        #     return parsedExpr

        #return None


    def _parse_ctor(self, context):

        if context is None:
            return None

        if not isinstance(context, ClassExpression):
            return None
        
        cTorName = context._identifier
        strParams = ''

        if self._giveMethodName() != context._identifier:
            return None
        
        # at Params_begin
        methodParamsTokens = self._get_all_valid_next_tokens(not_valid_tokens = [TokenType._params_end])
        
        methodParameters = [item.content for item in methodParamsTokens]

        strParams = self._parseAndFormatParams(methodParameters)

        while self._current_type() != TokenType._params_end:
            self.tokenStream.next()
        # at Params_end

        self.tokenStream.next()
        if self._current_type() == TokenType._semicolon:
            parsedCtor = CTorExpression(cTorName, strParams)
            return parsedCtor
        else:
            while self._current_type() != TokenType._closing_bracket:
                self.tokenStream.next()
        return None


    def _parse_dtor(self, context):
        dTorName = context._identifier

        self.tokenStream.next()
        self.tokenStream.next()

        if self._current_type() != TokenType._params_begin:
            raise Exception("Identifier expected correct destructor declaration")
        
        self.tokenStream.next() 
        self.tokenStream.next()

        if self._current_type() == TokenType._semicolon:
            parsedDtor = DTorExpression(dTorName)
            return parsedDtor
        else:
            while self._current_type() != TokenType._closing_bracket:
                self.tokenStream.next()

        return None


    def _parse_method(self, context):
        '''Used for parsing class methods.
    
        starting at params_begin token.

        '''

        if context is None:
            return None

        if not isinstance(context, ClassExpression):
            return None

        assert(self._current_type() == TokenType._params_begin)

        methodIdentifier = self._giveMethodName()

        if methodIdentifier == context._identifier:
            return None

        # at Params_begin

        methodReturnTokens = self._get_method_return_type()

        methodReturns = [item.content for item in methodReturnTokens]
        strReturns = self._parseAndFormatParams(methodReturns)

        # at Params_begin

        methodParamsTokens = self._get_all_valid_next_tokens(not_valid_tokens = [TokenType._params_end])
        
        methodParameters = [item.content for item in methodParamsTokens]
        strParams = self._parseAndFormatParams(methodParameters)

        while self._current_type() != TokenType._params_end:
            self.tokenStream.next()

        # at Params_end
        
        methodConstToken = \
            self._get_all_valid_next_tokens(not_valid_tokens = \
                [TokenType._semicolon, TokenType._opening_bracket])

        methodConstness = False
        if len(methodConstToken) == 1 and methodConstToken[0].content == 'const':
            methodConstness = True

        self.tokenStream.next()

        if methodConstness:
            self.tokenStream.next()

        if self._current_type() == TokenType._semicolon:
            methodExpr = MethodExpression(methodIdentifier,
                                          strParams,
                                          strReturns,
                                          methodConstness)

            return methodExpr
        else:
            while self._current_type() != TokenType._closing_bracket:
                self.tokenStream.next()

        return None 


    def _current_type(self):
        '''Returns current token type eq: TokenType._eof, TokenType._identifier'''
        return self.tokenStream.currentToken.type


    def _current_content(self):
        '''Returns current token content eq: Foo, uint32_t'''
        return self.tokenStream.currentToken.content


    def _isCtor(self,context):
        if not isinstance(context, ClassExpression):
            return False
        if self._giveMethodName() != context._identifier:
            return False
        return True
            

    def _parseAndFormatParams(self, methodParameters):

        # ta metode bym zmienil na taka co przyjmuje liste tokenow
        # z zwraca string
        # a dodatkowo ona z A::B robi A:: B
        strParams = ''
        for methodParam in methodParameters:
            if (methodParam == '&') or (methodParam == '*'):
                pass
            else:
                strParams += ' '
            strParams += methodParam
        strParams = strParams.replace(" ,",",")
        strParams = strParams.strip()
        return strParams


    def _get_all_valid_previous_tokens(self, not_valid_tokens, offset = 0):
        '''This method returns list of all tokens parsed backward till
           it reaches some of given not_valid_tokens.

           offset value enables to move backward start point of parsing.
        
        '''
        assert(offset >= 0)

        if not_valid_tokens is None:
            raise Exception("No arguments given.")

        originalPositionToken = self.tokenStream.currentToken

        howManySteps = offset

        # move backward
        while offset > 0:
            assert(self.tokenStream.prev())
            offset -= 1

        result = []

        while self.tokenStream.prev():
            howManySteps += 1

            # Not valid token
            if self._current_type() in not_valid_tokens:
                break

            result.append(self.tokenStream.currentToken)

        # move forward to original position
        for i in range(howManySteps):
            self.tokenStream.next()

        # check for original position
        assert(originalPositionToken is self.tokenStream.currentToken)

        result.reverse()

        return result


    def _get_all_valid_next_tokens(self, not_valid_tokens, offset = 0):
        '''This method returns list of all tokens parsed forward till
           it reaches some of given not_valid_tokens.

           offset value enables to move forward start point of parsing.
        
        '''
        assert(offset >= 0)

        if not_valid_tokens is None:
            raise Exception("No arguments given.")

        originalPositionToken = self.tokenStream.currentToken

        howManySteps = offset

        # move forward
        while offset > 0:
            assert(self.tokenStream.next())
            offset -= 1

        result = []

        while self.tokenStream.next():
            howManySteps += 1

            # Not valid token
            if self._current_type() in not_valid_tokens:
                break

            result.append(self.tokenStream.currentToken)

        # move backward to original position
        for i in range(howManySteps):
            self.tokenStream.prev()

        # check for original position
        assert(originalPositionToken is self.tokenStream.currentToken)

        return result


    def _giveMethodName(self):
        # ja bym pomyslal nad inna nazwa poniewaz to jest dobre do uzycia w wielu miejscach
        # a nie zawsze zwraca Method Name
        # moze np. get identifier from left albo cos takiego ?
        methodName = ''
        if self._current_type() == TokenType._params_begin:
            self.tokenStream.prev()
            methodName += self._current_content()
            self.tokenStream.next()
        return methodName


    def _get_method_return_type(self):
        '''Get return type for method starting from params begin.
        From caller perspective this method does not move tokenStream.
        
        Parsing backward and get all tokens as method return type.

        if we get -> _opening_bracket, _closing_bracket or _semicolon we are done.

        if we get -> _colon and prev() token is some of scope token (_public, _private, _protected)
        we are done also, otherwise treat it as part of namespace and continue parsing.

        '''

        assert(self._current_type() == TokenType._params_begin)

        stopParsingTokens = [TokenType._opening_bracket,
                             TokenType._closing_bracket,
                             TokenType._semicolon]

        originalPositionToken = self.tokenStream.currentToken

        # At method identifier
        assert(self.tokenStream.prev())
        howManySteps = 1

        result = []

        while self.tokenStream.prev():
            howManySteps += 1

            # We are done finally
            if self._current_type() in stopParsingTokens:
                break

            # Are we done ?
            if self._current_type() == TokenType._colon:
                t1 = self.tokenStream.currentToken
                assert(self.tokenStream.prev())
                howManySteps+=1
                # no this is namespace only
                if self._current_type() == TokenType._colon:
                    t2 = self.tokenStream.currentToken
                    result.append(t1)
                    result.append(t2)
                    continue
                # this is part of scope we are done
                else:
                    break
              
            result.append(self.tokenStream.currentToken)

        # move forward to original position
        for i in range(howManySteps):
            self.tokenStream.next()

        # check for original position
        assert(originalPositionToken is self.tokenStream.currentToken)

        result.reverse()

        return result