
from stateparser import *
from expressions import *


class State:
    def __init__(self, kind):
        self._kind = kind

    def is_successful_compared(self, token):
        return self._kind == token.kind

    def handle(self, token_stream, context):
        pass

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

    @staticmethod
    def _get_all_valid_next_tokens(token_stream, not_valid_tokens, offset=0):
        '''This method returns list of all tokens parsed forward till
           it reaches some of given not_valid_tokens.

           offset value enables to move forward start point of parsing.

        '''
        assert (offset >= 0)

        if not_valid_tokens is None:
            raise Exception("No arguments given.")

        original_position_token = token_stream.current_token

        how_many_steps = offset

        # move forward
        while offset > 0:
            assert (token_stream.next())
            offset -= 1

        result = []

        while token_stream.next():
            how_many_steps += 1

            # Not valid token
            if token_stream.current_token.kind in not_valid_tokens:
                break

            result.append(token_stream.current_token)

        # move backward to original position
        for i in range(how_many_steps):
            token_stream.prev()

        # check for original position
        assert (original_position_token is token_stream.current_token)

        return result

    def _get_identifier_from_left(self, token_stream):
        id_from_left_name = ''
        if token_stream.current_token.kind == TokenType.params_begin_:
            token_stream.prev()
            id_from_left_name += token_stream.current_token.content
            token_stream.next()
        return id_from_left_name

    def _get_method_return_type(self, token_stream):
        '''Get return type for method starting from params begin.
        From caller perspective this method does not move tokenStream.

        Parsing backward and get all tokens as method return type.

        if we get -> _opening_bracket, _closing_bracket or _semicolon we are done.

        if we get -> _colon and prev() token is some of scope token (_public, _private, _protected)
        we are done also, otherwise treat it as part of namespace and continue parsing.

        '''

        assert (token_stream.current_token.kind == TokenType.params_begin_)

        stop_parsing_tokens = [TokenType.opening_bracket_,
                               TokenType.closing_bracket_,
                               TokenType.semicolon_]

        original_position_token = token_stream.current_token

        # At method identifier
        assert (token_stream.prev())
        how_many_steps = 1

        result = []

        while token_stream.prev():
            how_many_steps += 1

            # We are done finally
            if token_stream.current_token.kind in stop_parsing_tokens:
                break

            # Are we done ?
            if token_stream.current_token.kind == TokenType.colon_:
                t1 = token_stream.current_token
                assert (token_stream.prev())
                how_many_steps += 1
                # no this is namespace only
                if token_stream.current_token.kind == TokenType.colon_:
                    t2 = token_stream.current_token
                    result.append(t1)
                    result.append(t2)
                    continue
                # this is part of scope we are done
                else:
                    break

            result.append(token_stream.current_token)

        # move forward to original position
        for i in range(how_many_steps):
            token_stream.next()

        # check for original position
        assert (original_position_token is token_stream.current_token)

        for item in result:
            if item.kind == TokenType.virtual_:
                result.remove(item)
                break

        result.reverse()

        return result


class ClassState(State):
    def __init__(self):
        State.__init__(self, TokenType.class_)

    def handle(self, token_stream, context):
        # we have class already
        # go next
        token_stream.next()

        # consume identifier
        if token_stream.current_token.kind != TokenType.identifier_:
            raise Exception("Identifier expected after class keyword")

        # we have identifier
        parsed_class = ClassExpression(token_stream.current_token.content)

        token_stream.next()

        # we have something...

        # ...maybe forwarded class
        if token_stream.current_token.kind == TokenType.semicolon_:
            return None

        # ...move after opening bracket
        while token_stream.current_token.kind != TokenType.opening_bracket_:
            token_stream.next()

        # currentToken == token.opening_brackets

        while token_stream.next():

            # friend inside class
            if token_stream.current_token.kind == TokenType.friend_:
                parsed_class._friend_inside_spotted()

            # take care of public, prot, private
            parsed_class._set_scope_from_scope_token(token_stream.current_token.kind)

            # we're done
            if token_stream.current_token.kind == TokenType.closing_bracket_:
                break

            state_parser = StateParserBuilder(token_stream).\
                add_class_parsing().\
                add_dtor_parsing().\
                add_operator_parsing().\
                add_params_parsing().\
                get_product()

            expr = state_parser.process(parsed_class)
            if expr is None:
                continue
            parsed_class.attach(expr)

        return parsed_class


class NamespaceState(State):
    def __init__(self):
        State.__init__(self, TokenType.namespace_)

    def handle(self, token_stream, context):
        # we have "namespace" already
        # go next
        token_stream.next()

        # consume identifier
        if token_stream.current_token.kind != TokenType.identifier_:
            raise Exception("Identifier expected after namespace keyword")

        # we have identifier
        parsed_namespace = NamespaceExpression(token_stream.current_token.content)

        token_stream.next()

        if token_stream.current_token.kind != TokenType.opening_bracket_:
            raise Exception("No opening brackets after namespace identifier")

        # currentToken == token.opening_brackets

        while token_stream.next():

            # we're done
            if token_stream.current_token.kind == TokenType.closing_bracket_:
                break

            state_parser = StateParserBuilder(token_stream).\
                add_class_parsing().\
                add_namespace_parsing().\
                get_product()

            expr = state_parser.process(parsed_namespace)
            if expr is None:
                continue
            parsed_namespace.attach(expr)

        return parsed_namespace


class DtorState(State):
    def __init__(self):
        State.__init__(self, TokenType.tilde_)

    def handle(self, token_stream, context):
        '''Used for parsing class dtor.'''
        if not self._is_proper_class_context(context):
            return None

        if not self._is_public_scope(context):
            return None

        d_tor_name = context.identifier

        while token_stream.current_token.kind != TokenType.params_end_:
            token_stream.next()

        token_stream.next()

        if token_stream.current_token.kind == TokenType.semicolon_:
            return DTorExpression(d_tor_name)
        else:
            while token_stream.current_token.kind != TokenType.closing_bracket_:
                token_stream.next()

        return None


class CtorState(State):
    def __init__(self):
        State.__init__(self, TokenType.params_begin_)

    def handle(self, token_stream, context):
        '''Used for parsing class ctor.'''
        if not self._is_proper_class_context(context):
            return None

        if not self._is_public_scope(context):
            return None

        c_tor_name = context.identifier
        str_params = ''

        if self._get_identifier_from_left(token_stream) != context.identifier:
            return None

        # at Params_begin
        ctor_params_tokens = State._get_all_valid_next_tokens(token_stream=token_stream, not_valid_tokens=[TokenType.params_end_])

        str_params = self._convert_param_tokens_to_string(ctor_params_tokens)

        while token_stream.current_token.kind != TokenType.params_end_:
            token_stream.next()
        # at Params_end

        token_stream.next()
        if token_stream.current_token.kind == TokenType.semicolon_:
            return CTorExpression(c_tor_name, str_params)
        else:
            while token_stream.current_token.kind != TokenType.closing_bracket_:
                token_stream.next()
        return None


class OperatorState(State):
    def __init__(self):
        State.__init__(self, TokenType.operator_)

    def handle(self, token_stream, context):
        '''Used for parsing class operator.'''

        if not self._is_proper_class_context(context):
            return None

        if not self._is_public_scope(context):
            return None

        operator_id_str = ''
        token_stream.next()

        while token_stream.current_token.kind != TokenType.params_begin_:
            operator_id_str += token_stream.current_token.content
            token_stream.next()

        operator_return_tokens = self._get_method_return_type(token_stream)
        del operator_return_tokens[-1]
        str_returns = self._convert_param_tokens_to_string(operator_return_tokens)

        operator_params_tokens = State._get_all_valid_next_tokens(token_stream=token_stream, not_valid_tokens=[TokenType.params_end_])
        str_params = self._convert_param_tokens_to_string(operator_params_tokens)

        while token_stream.current_token.kind != TokenType.params_end_:
            token_stream.next()

        token_stream.next()
        if token_stream.current_token.kind == TokenType.semicolon_:
            return OperatorExpression(operator_id_str, str_params, str_returns)
        else:
            while token_stream.current_token.kind != TokenType.closing_bracket_:
                token_stream.next()
        return None


class ParamsState(State):
    def __init__(self):
        State.__init__(self, TokenType.params_begin_)

    def _is_ctor(self, token_stream, context):
        if not isinstance(context, ClassExpression):
            return False
        if self._get_identifier_from_left(token_stream) != context.identifier:
            return False
        return True

    def handle(self, token_stream, context):
        if self._is_ctor(token_stream, context):
            return CtorState().handle(token_stream, context)
        else:
            return MethodState().handle(token_stream, context)


class MethodState(State):
    def __init__(self):
        State.__init__(self, TokenType.params_begin_)

    def handle(self, token_stream, context):
        '''Used for parsing class methods.

                starting at params_begin token.

                '''

        if not self._is_proper_class_context(context):
            return None
        if not self._is_public_scope(context):
            return None

        assert (token_stream.current_token.kind == TokenType.params_begin_)

        if not context.is_friend_inside() and \
                (
                        context.get_current_scope() == TokenType.protected_ or context.get_current_scope() == TokenType.private_):
            return None

        method_identifier = self._get_identifier_from_left(token_stream)

        if method_identifier == context.identifier:
            return None

        # at Return_Params_begin

        method_return_tokens = self._get_method_return_type(token_stream)
        str_returns = self._convert_param_tokens_to_string(method_return_tokens)

        # at Return_Params_end

        # at Params_begin

        method_params_tokens = self._get_all_valid_next_tokens(token_stream=token_stream, not_valid_tokens=[TokenType.params_end_])
        str_params = self._convert_param_tokens_to_string(method_params_tokens)

        while token_stream.current_token.kind != TokenType.params_end_:
            token_stream.next()

        # at Params_end

        after_parameters_tokens = \
            self._get_all_valid_next_tokens(token_stream=token_stream, not_valid_tokens=
                                                [TokenType.semicolon_, TokenType.opening_bracket_])

        method_constness = False
        for token in after_parameters_tokens:
            if token.kind == TokenType.const_:
                method_constness = True

            # pure virtual
            if token.kind == TokenType.equal_:
                return None

        while token_stream.next():
            if token_stream.current_token.kind == TokenType.semicolon_ or \
                    token_stream.current_token.kind == TokenType.opening_bracket_:
                break

        if token_stream.current_token.kind == TokenType.semicolon_:
            return MethodExpression(method_identifier,
                                    str_params,
                                    str_returns,
                                    method_constness)

        else:
            while token_stream.current_token.kind != TokenType.closing_bracket_:
                token_stream.next()

        return None


class StateParserBuilder:
    def __init__(self, token_stream):
        self._sp = StateParser(token_stream)

    def add_class_parsing(self):
        self._sp.add_state(ClassState())
        return self

    def add_namespace_parsing(self):
        self._sp.add_state(NamespaceState())
        return self

    def add_params_parsing(self):
        self._sp.add_state(ParamsState())
        return self

    def add_operator_parsing(self):
        self._sp.add_state(OperatorState())
        return self

    def add_dtor_parsing(self):
        self._sp.add_state(DtorState())
        return self

    def get_product(self):
        return self._sp
