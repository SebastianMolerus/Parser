from TreeBuilder.tok import TokenType


def get_return_part(token_stream):
    assert token_stream.current_kind() == TokenType.params_begin_

    stop_parsing_tokens = [TokenType.opening_bracket_,
                           TokenType.closing_bracket_,
                           TokenType.semicolon_]

    starting_position = token_stream.current_index

    assert (token_stream.backward())
    result = []

    while token_stream.backward():
        if token_stream.current_kind() in stop_parsing_tokens:
            break

        if token_stream.current_kind() == TokenType.colon_ and \
                token_stream.get_token_kind_from_right() != TokenType.colon_ and \
                token_stream.get_token_kind_from_left() != TokenType.colon_:
            break

        if token_stream.current_kind() != TokenType.virtual_:
            result.append(token_stream.current_token)

    token_stream.current_index = starting_position

    result.reverse()

    return result


def get_method_parameters_as_str(token_stream):
    method_parameters_as_tokens = token_stream.get_all_valid_forward_tokens(not_valid_token_types=
                                                                            [TokenType.params_end_])
    method_parameters_as_string = convert_param_tokens_to_string(method_parameters_as_tokens)
    return method_parameters_as_string


def get_return_part_as_str(token_stream):
    method_return_part_as_tokens = get_return_part(token_stream)
    method_return_part_as_string = convert_param_tokens_to_string(method_return_part_as_tokens)
    return method_return_part_as_string


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
