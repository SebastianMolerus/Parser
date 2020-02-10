from tokenstream import *
from tokenreader import *
from expressions import *


class AbstractTreeBuilder:
    def __init__(self, source_code = None, file = None):

        if source_code is not None:
            self.tokenReader = TokenReader(text=source_code)
        else:
            self.tokenReader = TokenReader(file=file)

        self.tokenStream = TokenStream(self.tokenReader)

    def build_ast(self):

        asttree = Expression('Root')

        while self.tokenStream.next():
            expr = self._try_parse_expression(asttree)
            if expr is not None:
                asttree.attach(expr)
        return asttree

    def _try_parse_expression(self, context = None):
        '''Main dispatch method for all expresions.
        
        Every method called from here should return 
        
        Expression if parsed succesfull

        or None
        
        '''

        current_token = self.tokenStream.current_token

        if current_token.kind == TokenType.template_:
            pass

        if current_token.kind == TokenType.typedef_:
            while self.tokenStream.next():
                if self._current_type() == TokenType.semicolon_:
                    break
            return None

        if current_token.kind == TokenType.namespace_:
            return self._parse_namespace(context)

        if current_token.kind == TokenType.class_:
            return self._parse_class(context)

        if current_token.kind == TokenType.params_begin_:
            return self._parse_params(context)

        if current_token.kind == TokenType.tilde_:
            return self._parse_dtor(context)

        if current_token.kind == TokenType.operator_:
            return self._parse_operator(context)

        return None

    def _parse_namespace(self, context):

        # we have "namespace" already
        # go next
        self.tokenStream.next()

        # consume identifier
        if self._current_type() != TokenType.identifier_:
            raise Exception("Identifier expected after namespace keyword")

        # we have identifier
        parsed_namespace  = NamespaceExpression(self._current_content())

        self.tokenStream.next()

        if self._current_type() != TokenType.opening_bracket_:
            raise Exception("No opening brackets after namespace identifier")

        # currentToken == token.opening_brackets

        while self.tokenStream.next():

            # we're done
            if self._current_type() == TokenType.closing_bracket_:
                break

            expr = self._try_parse_expression(parsed_namespace)
            if expr is None:
                continue
            parsed_namespace.attach(expr)

        return parsed_namespace

    def _parse_class(self, context):
        # we have class already
        # go next
        self.tokenStream.next()

        # consume identifier
        if self._current_type() != TokenType.identifier_:
            raise Exception("Identifier expected after class keyword")

        # we have identifier
        parsed_class = ClassExpression(self._current_content())

        self.tokenStream.next()

        # we have something...

        # ...maybe forwarded class
        if self._current_type() == TokenType.semicolon_:
            return None

        # ...move after opening bracket
        while self._current_type() != TokenType.opening_bracket_:
            self.tokenStream.next()

        # currentToken == token.opening_brackets

        while self.tokenStream.next():

            # friend inside class
            if self._current_type() == TokenType.friend_:
                parsed_class._friend_inside_spotted()

            # take care of public, prot, private
            parsed_class._set_scope_from_scope_token(self._current_type())

            # we're done
            if self._current_type() == TokenType.closing_bracket_:
                break

            expr = self._try_parse_expression(parsed_class)
            if expr is None:
                continue
            parsed_class.attach(expr)

        return parsed_class

    def _parse_params(self, context):
        """Used as dispatch method for parsing

        everything from TokenType._params_begin

        """
        if self._is_ctor(context):
            return self._parse_ctor(context)
        else:
            return self._parse_method(context)

    def _parse_ctor(self, context):
        '''Used for parsing class ctor.'''
        if not self._is_proper_class_context(context):
            return None

        if not self._is_public_scope(context):
            return None

        c_tor_name = context._identifier
        str_params = ''

        if self._get_identifier_from_left() != context._identifier:
            return None

        # at Params_begin
        ctorParamsTokens = self._get_all_valid_next_tokens(not_valid_tokens = [TokenType.params_end_])

        str_params = self._convert_param_tokens_to_string(ctorParamsTokens)

        while self._current_type() != TokenType.params_end_:
            self.tokenStream.next()
        # at Params_end

        self.tokenStream.next()
        if self._current_type() == TokenType.semicolon_:
            return CTorExpression(c_tor_name, str_params)
        else:
            while self._current_type() != TokenType.closing_bracket_:
                self.tokenStream.next()
        return None

    def _parse_dtor(self, context):
        '''Used for parsing class dtor.'''
        if not self._is_proper_class_context(context):
            return None

        if not self._is_public_scope(context):
            return None

        d_tor_name = context._identifier

        while self._current_type() != TokenType.params_end_:
            self.tokenStream.next()

        self.tokenStream.next()

        if self._current_type() == TokenType.semicolon_:
            return DTorExpression(d_tor_name)
        else:
            while self._current_type() != TokenType.closing_bracket_:
                self.tokenStream.next()

        return None

    def _parse_method(self, context):
        '''Used for parsing class methods.

        starting at params_begin token.

        '''

        if not self._is_proper_class_context(context):
            return None
        if not AbstractTreeBuilder._is_public_scope(context):
            return None

        assert(self._current_type() == TokenType.params_begin_)

        if not context.is_friend_inside() and \
            (context.get_current_scope() == TokenType.protected_ or context.get_current_scope() == TokenType.private_):
            return None

        method_identifier = self._get_identifier_from_left()

        if method_identifier == context._identifier:
            return None

        # at Return_Params_begin

        method_return_tokens = self._get_method_return_type()
        str_returns = self._convert_param_tokens_to_string(method_return_tokens)

        # at Return_Params_end

        # at Params_begin

        method_params_tokens = self._get_all_valid_next_tokens(not_valid_tokens = [TokenType.params_end_])
        str_params = self._convert_param_tokens_to_string(method_params_tokens)

        while self._current_type() != TokenType.params_end_:
            self.tokenStream.next()

        # at Params_end

        after_parameters_tokens = \
            self._get_all_valid_next_tokens(not_valid_tokens = \
                [TokenType.semicolon_, TokenType.opening_bracket_])

        method_constness = False
        for token in after_parameters_tokens:
            if token.kind == TokenType.const_:
                method_constness = True

            # pure virtual
            if token.kind == TokenType.equal_:
                return None

        while self.tokenStream.next():
            if self._current_type() == TokenType.semicolon_ or \
               self._current_type() == TokenType.opening_bracket_:
                break

        if self._current_type() == TokenType.semicolon_:
            return  MethodExpression(method_identifier,
                                     str_params,
                                     str_returns,
                                     method_constness)

        else:
            while self._current_type() != TokenType.closing_bracket_:
                self.tokenStream.next()

        return None

    def _parse_operator(self,context):
        '''Used for parsing class operator.'''

        if not self._is_proper_class_context(context):
            return None

        if not self._is_public_scope(context):
            return None

        operator_id_str = ''
        self.tokenStream.next()

        while self._current_type() != TokenType.params_begin_:
            operator_id_str += self._current_content()
            self.tokenStream.next()

        operator_return_tokens = self._get_method_return_type()
        del operator_return_tokens[-1]
        str_returns = self._convert_param_tokens_to_string(operator_return_tokens)

        operator_params_tokens = self._get_all_valid_next_tokens(not_valid_tokens = [TokenType.params_end_])
        str_params = self._convert_param_tokens_to_string(operator_params_tokens)

        while self._current_type() != TokenType.params_end_:
            self.tokenStream.next()

        self.tokenStream.next()
        if self._current_type() == TokenType.semicolon_:
            return OperatorExpression(operator_id_str, str_params, str_returns)
        else:
            while self._current_type() != TokenType.closing_bracket_:
                self.tokenStream.next()
        return None

    def _current_type(self):
        '''Returns current token type eq: TokenType._eof, TokenType._identifier'''
        return self.tokenStream.current_token.kind

    def _current_content(self):
        '''Returns current token content eq: Foo, uint32_t'''
        return self.tokenStream.current_token.content

    def _is_ctor(self,context):
        if not isinstance(context, ClassExpression):
            return False
        if self._get_identifier_from_left() != context._identifier:
            return False
        return True

    @staticmethod
    def _is_proper_class_context(context):
        if context is None:
            return False
        if not isinstance(context, ClassExpression):
            return False
        return True

    @staticmethod
    def _convert_param_tokens_to_string(method_params_tokens):
        str_method_params = ''
        for methodParamToken in method_params_tokens:
            if (methodParamToken.kind == TokenType.ref_) or \
               (methodParamToken.kind == TokenType.star_) or \
               (methodParamToken.kind == TokenType.colon_):
                pass
            else:
                str_method_params += ' '
            str_method_params += methodParamToken.content
        str_method_params = str_method_params.replace(" ,", ",")
        str_method_params = str_method_params.replace(": ", ":")
        str_method_params = str_method_params.strip()
        return str_method_params

    @staticmethod
    def _is_public_scope(context):
        if context.get_current_scope() == TokenType.public_:
            return True
        return False

    def _get_all_valid_next_tokens(self, not_valid_tokens, offset = 0):
        '''This method returns list of all tokens parsed forward till
           it reaches some of given not_valid_tokens.

           offset value enables to move forward start point of parsing.

        '''
        assert(offset >= 0)

        if not_valid_tokens is None:
            raise Exception("No arguments given.")

        original_position_token = self.tokenStream.current_token

        how_many_steps = offset

        # move forward
        while offset > 0:
            assert(self.tokenStream.next())
            offset -= 1

        result = []

        while self.tokenStream.next():
            how_many_steps += 1

            # Not valid token
            if self._current_type() in not_valid_tokens:
                break

            result.append(self.tokenStream.current_token)

        # move backward to original position
        for i in range(how_many_steps):
            self.tokenStream.prev()

        # check for original position
        assert(original_position_token is self.tokenStream.current_token)

        return result

    def _get_identifier_from_left(self):
        id_from_left_name = ''
        if self._current_type() == TokenType.params_begin_:
            self.tokenStream.prev()
            id_from_left_name += self._current_content()
            self.tokenStream.next()
        return id_from_left_name

    def _get_method_return_type(self):
        '''Get return type for method starting from params begin.
        From caller perspective this method does not move tokenStream.

        Parsing backward and get all tokens as method return type.

        if we get -> _opening_bracket, _closing_bracket or _semicolon we are done.

        if we get -> _colon and prev() token is some of scope token (_public, _private, _protected)
        we are done also, otherwise treat it as part of namespace and continue parsing.

        '''

        assert(self._current_type() == TokenType.params_begin_)

        stop_parsing_tokens = [TokenType.opening_bracket_,
                               TokenType.closing_bracket_,
                               TokenType.semicolon_]

        original_position_token = self.tokenStream.current_token

        # At method identifier
        assert(self.tokenStream.prev())
        how_many_steps = 1

        result = []

        while self.tokenStream.prev():
            how_many_steps += 1

            # We are done finally
            if self._current_type() in stop_parsing_tokens:
                break

            # Are we done ?
            if self._current_type() == TokenType.colon_:
                t1 = self.tokenStream.current_token
                assert(self.tokenStream.prev())
                how_many_steps+=1
                # no this is namespace only
                if self._current_type() == TokenType.colon_:
                    t2 = self.tokenStream.current_token
                    result.append(t1)
                    result.append(t2)
                    continue
                # this is part of scope we are done
                else:
                    break

            result.append(self.tokenStream.current_token)

        # move forward to original position
        for i in range(how_many_steps):
            self.tokenStream.next()

        # check for original position
        assert(original_position_token is self.tokenStream.current_token)

        for item in result:
            if item.kind == TokenType.virtual_:
                result.remove(item)
                break

        result.reverse()

        return result
