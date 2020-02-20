from abc import abstractmethod
from TreeBuilder.tok import TokenType


class State:
    def __init__(self, kind):
        self._kind = kind

    def is_valid(self, token_stream, expression_context):
        return self._kind == token_stream.current_kind()

    @abstractmethod
    def handle(self, token_stream, expression_context):
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
