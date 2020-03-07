from TreeBuilder.tok import TokenType


def get_return_part_as_tokens(token_stream):
    stop_parsing_tokens = [TokenType.opening_bracket_,
                           TokenType.closing_bracket_,
                           TokenType.semicolon_]

    # save position
    starting_position = token_stream.current_index
    result = []

    while token_stream.backward():
        if token_stream.current_kind() in stop_parsing_tokens:
            break

        # public: etc.
        if token_stream.current_kind() == TokenType.colon_ and \
                token_stream.right_token().kind != TokenType.colon_ and \
                token_stream.left_token().kind != TokenType.colon_:
            break

        if token_stream.current_kind() != TokenType.virtual_:
            result.append(token_stream.current_token)

    # restore position
    token_stream.current_index = starting_position

    result.reverse()

    return result


def convert_param_tokens_to_string(param_tokens):
    str_method_params = ''
    for methodParamToken in param_tokens:
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


def format_method_parameters_as_string(token_stream):
    method_parameters_as_tokens = token_stream.copy_forward(not_valid_token_types=
                                                                            [TokenType.params_end_])
    return convert_param_tokens_to_string(method_parameters_as_tokens)


def format_return_part_as_string(token_stream):
    method_return_part_as_tokens = get_return_part_as_tokens(token_stream)
    return convert_param_tokens_to_string(method_return_part_as_tokens)



