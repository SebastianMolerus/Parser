from abc import abstractmethod
from TreeBuilder.expressions import ClassExpression
from TreeBuilder.tok import TokenType


class State:
    def __init__(self, kind):
        self._kind = kind

    def is_successful_compared(self, token_kind):
        return self._kind == token_kind

    @abstractmethod
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
