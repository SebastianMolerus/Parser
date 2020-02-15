from abc import abstractmethod
from TreeBuilder.tok import TokenType


class State:
    def __init__(self, kind, token_stream, context=None):
        self._kind = kind
        self._token_stream = token_stream
        self._context = context

    def is_valid(self):
        return self._kind == self._current_kind()

    @abstractmethod
    def handle(self):
        pass

    @staticmethod
    def convert_param_tokens_to_string(method_params_tokens):
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

    def get_all_valid_next_tokens(self, not_valid_tokens):
        '''This method returns list of all tokens parsed forward till
           it reaches some of given not_valid_tokens.

           offset value enables to move forward start point of parsing.

        '''

        if not_valid_tokens is None:
            raise Exception("No arguments given.")

        original_position_token = self._token_stream.current_token

        how_many_steps = 0
        result = []

        while self._forward():
            how_many_steps += 1

            # Not valid token
            if self._token_stream.current_token.kind in not_valid_tokens:
                break

            result.append(self._token_stream.current_token)

        # move backward to original position
        for i in range(how_many_steps):
            self._backward()

        # check for original position
        assert (original_position_token is self._token_stream.current_token)

        return result

    def get_token_content_from_left(self):
        self._backward()
        identifier = self._current_content()
        self._forward()
        return identifier

    def _get_method_return_type(self):
        '''
        Get return type for method starting from params begin.
        From caller perspective this method does not move tokenStream.

        Parsing backward and get all tokens as method return type.

        if we get -> _opening_bracket, _closing_bracket or _semicolon we are done.

        if we get -> _colon and prev() token is some of scope token (_public, _private, _protected)
        we are done also, otherwise treat it as part of namespace and continue parsing.

        '''
        assert (self._current_kind() == TokenType.params_begin_)

        stop_parsing_tokens = [TokenType.opening_bracket_,
                               TokenType.closing_bracket_,
                               TokenType.semicolon_]

        original_position_token = self._token_stream.current_token

        # At method identifier
        assert (self._backward())
        how_many_steps = 1

        result = []

        while self._backward():
            how_many_steps += 1

            # We are done finally
            if self._current_kind() in stop_parsing_tokens:
                break

            # Are we done ?
            if self._current_kind() == TokenType.colon_:
                t1 = self._token_stream.current_token
                assert (self._backward())
                how_many_steps += 1
                # no this is namespace only
                if self._current_kind() == TokenType.colon_:
                    t2 = self._token_stream.current_token
                    result.append(t1)
                    result.append(t2)
                    continue
                # this is part of scope we are done
                else:
                    break

            result.append(self._token_stream.current_token)

        # move forward to original position
        for i in range(how_many_steps):
            self._forward()

        # check for original position
        assert (original_position_token is self._token_stream.current_token)

        for item in result:
            if item.kind == TokenType.virtual_:
                result.remove(item)
                break

        result.reverse()

        return result

    def _current_content(self):
        return self._token_stream.current_token.content

    def _current_kind(self):
        return self._token_stream.current_token.kind

    def _forward(self):
        return self._token_stream.next()

    def _backward(self):
        return self._token_stream.prev()