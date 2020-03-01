from TreeBuilder.expressions import ClassExpression, NamespaceExpression, CTorExpression, MethodExpression, \
    DTorExpression, OperatorExpression
from TreeBuilder.tok import TokenType, Token


def get_return_part(token_stream):
    assert (token_stream.current_kind() == TokenType.params_begin_)

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


def parse_class(token_stream):
    if token_stream.current_kind() != TokenType.class_:
        raise Exception("Expected 'class' keyword")

    token_stream.forward()

    # At class 'identifier'
    parsed_class = ClassExpression(token_stream.current_content())

    token_stream.forward()

    # forwarded class
    if token_stream.current_kind() == TokenType.semicolon_:
        return None

    token_stream.move_forward_to_token_type(TokenType.opening_bracket_)

    add_child_expressions_into_class(parsed_class, token_stream)

    return parsed_class


def add_child_expressions_into_class(parsed_class, token_stream):
    while token_stream.forward():

        if token_stream.current_kind() == TokenType.friend_:
            parsed_class.set_friend_inside()

        parsed_class.set_scope(token_stream.current_kind())

        if token_stream.current_kind() == TokenType.closing_bracket_:
            break

        child_expr = parse_expression(token_stream, parsed_class)
        if child_expr is None:
            continue
        parsed_class.attach(child_expr)


def parse_namespace(token_stream):
    # At namespace
    token_stream.forward()

    # At namespace identifier
    parsed_namespace = NamespaceExpression(token_stream.current_content())

    # At opening bracket
    token_stream.forward()

    while token_stream.forward():
        if token_stream.current_kind() == TokenType.closing_bracket_:
            break

        expr = parse_expression(token_stream, parsed_namespace)
        if expr is None:
            continue
        parsed_namespace.attach(expr)

    return parsed_namespace


def is_method(token_stream, expression_context):
    return token_stream.get_token_content_from_left() != expression_context.identifier and\
           (expression_context.get_current_scope() == TokenType.public_ or expression_context.is_friend_inside())


def is_constructor(token_stream, expression_context):
    return isinstance(expression_context, ClassExpression) and\
           token_stream.get_token_content_from_left() == expression_context.identifier and\
           (expression_context.get_current_scope() == TokenType.public_ or expression_context.is_friend_inside())


def parse_params(token_stream, expression_context=None):

    if expression_context is None:
        return None

    if is_method(token_stream, expression_context):
        return parse_method(token_stream)
    elif is_constructor(token_stream, expression_context):
        return parse_constructor(token_stream, expression_context)


def parse_method(token_stream):
    # At params begin
    method_name = token_stream.get_token_content_from_left()

    method_return_part_as_string = get_return_part_as_str(token_stream)

    method_parameters_as_string = get_method_parameters_as_str(token_stream)

    token_stream.move_forward_to_token_type(TokenType.params_end_)

    after_method_parameters_tokens = \
        token_stream.get_all_valid_forward_tokens(not_valid_token_types=
                                                  [TokenType.semicolon_, TokenType.opening_bracket_])

    is_method_const = False
    if Token(TokenType.const_) in after_method_parameters_tokens:
        is_method_const = True

    # Pure virtual
    if Token(TokenType.equal_) in after_method_parameters_tokens:
        return None

    while token_stream.forward():
        if token_stream.current_kind() == TokenType.semicolon_:
            return MethodExpression(method_name,
                                    method_parameters_as_string,
                                    method_return_part_as_string,
                                    is_method_const)

        elif token_stream.current_kind() == TokenType.opening_bracket_:
            token_stream.move_forward_to_token_type(TokenType.closing_bracket_)
            break


def parse_constructor(token_stream, expression_context):
    constructor_identifier = expression_context.identifier

    constructor_parameters_as_tokens = \
        token_stream.get_all_valid_forward_tokens(not_valid_token_types=[TokenType.params_end_])

    constructor_parameters_as_string = convert_param_tokens_to_string(constructor_parameters_as_tokens)

    token_stream.move_forward_to_token_type(TokenType.params_end_)

    token_stream.forward()
    if token_stream.current_kind() == TokenType.semicolon_:
        return CTorExpression(constructor_identifier, constructor_parameters_as_string)
    else:
        token_stream.move_forward_to_token_type(TokenType.closing_bracket_)


def parse_destructor(token_stream, expression_context):
    if expression_context.get_current_scope() != TokenType.public_:
        return None

    destructor_identifier = expression_context.identifier

    token_stream.move_forward_to_token_type(TokenType.params_end_)

    token_stream.forward()

    if token_stream.current_kind() == TokenType.semicolon_:
        return DTorExpression(destructor_identifier)
    else:
        token_stream.move_forward_to_token_type(TokenType.closing_bracket_)


def parse_operator(token_stream, expression_context):

    if expression_context is None:
        return None

    if expression_context.get_current_scope() != TokenType.public_ and not expression_context.is_friend_inside():
        return None

    operator_name = ''
    token_stream.forward()

    while token_stream.current_kind() != TokenType.params_begin_:
        operator_name += token_stream.current_content()
        token_stream.forward()

    operator_return_tokens = get_return_part(token_stream)
    del operator_return_tokens[-1]
    return_pars_as_str = convert_param_tokens_to_string(operator_return_tokens)

    operator_params_tokens = token_stream.get_all_valid_forward_tokens(not_valid_token_types=[TokenType.params_end_])
    str_params = convert_param_tokens_to_string(operator_params_tokens)

    token_stream.move_forward_to_token_type(TokenType.params_end_)

    token_stream.forward()
    if token_stream.current_kind() == TokenType.semicolon_:
        return OperatorExpression(operator_name, str_params, return_pars_as_str)
    else:
        token_stream.move_forward_to_token_type(TokenType.closing_bracket_)


def parse_expression(token_stream, expression_context=None):
    current_kind = token_stream.current_kind()

    if current_kind == TokenType.class_:
        return parse_class(token_stream)

    elif current_kind == TokenType.namespace_:
        return parse_namespace(token_stream)

    elif current_kind == TokenType.params_begin_:
        return parse_params(token_stream, expression_context)

    elif current_kind == TokenType.tilde_:
        return parse_destructor(token_stream, expression_context)

    elif current_kind == TokenType.operator_:
        return parse_operator(token_stream, expression_context)
