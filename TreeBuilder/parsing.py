import re

from TreeBuilder.expressions import ClassExpression, NamespaceExpression, CTorExpression, MethodExpression, \
    DTorExpression, OperatorExpression, Expression
from TreeBuilder.parsing_utilities import convert_param_tokens_to_string, get_return_part_as_tokens
from TreeBuilder.tok import TokenType, Token


def parse_class(token_stream):
    assert token_stream.current_kind() == TokenType.class_

    token_stream.forward()

    assert token_stream.current_kind() == TokenType.identifier_

    parsed_class = ClassExpression(identifier=token_stream.current_content())

    token_stream.forward()

    # forwarded class
    if token_stream.current_kind() == TokenType.semicolon_:
        return None

    token_stream.move_forward_to(TokenType.opening_bracket_)

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
    assert token_stream.current_kind() == TokenType.namespace_
    token_stream.forward()

    assert token_stream.current_kind() == TokenType.identifier_

    parsed_namespace = NamespaceExpression(token_stream.current_content())

    token_stream.forward()

    assert token_stream.current_kind() == TokenType.opening_bracket_

    while token_stream.forward():
        if token_stream.current_kind() == TokenType.closing_bracket_:
            break

        expr = parse_expression(token_stream, parsed_namespace)
        if expr is None:
            continue
        parsed_namespace.attach(expr)

    return parsed_namespace


def is_method(token_stream, expression_context):
    return token_stream.left_token().kind == TokenType.identifier_ and\
        token_stream.left_token().content != expression_context.identifier and\
        (expression_context.get_current_scope() == TokenType.public_ or expression_context.is_friend_inside())


def is_constructor(token_stream, expression_context):
    return isinstance(expression_context, ClassExpression) and\
           token_stream.left_token().content == expression_context.identifier and\
           (expression_context.get_current_scope() == TokenType.public_ or expression_context.is_friend_inside())


def parse_params(token_stream, expression_context=None):

    if expression_context is None:
        return None

    if is_method(token_stream, expression_context):
        return parse_method(token_stream)
    elif is_constructor(token_stream, expression_context):
        return parse_constructor(token_stream, expression_context)


def parse_method(token_stream):
    assert token_stream.current_kind() == TokenType.params_begin_
    assert token_stream.left_token().kind == TokenType.identifier_

    token_stream.backward()
    assert token_stream.current_kind() == TokenType.identifier_

    method_name = token_stream.current_content()

    return_part_tokens = get_return_part_as_tokens(token_stream)
    return_part_string = convert_param_tokens_to_string(return_part_tokens)

    token_stream.move_forward_to(TokenType.params_begin_)
    token_stream.forward()

    parameters_tokens = token_stream.forward_copy_if(lambda ts: ts.current_kind() != TokenType.params_end_)
    parameters_string = convert_param_tokens_to_string(parameters_tokens)
    assert token_stream.current_kind() == TokenType.params_end_

    after_parameters_tokens = \
        token_stream.forward_copy_if(lambda ts: ts.current_kind() != TokenType.semicolon_
                                     and ts.current_kind() != TokenType.opening_bracket_)

    # Pure virtual
    if Token(TokenType.equal_) in after_parameters_tokens:
        return None

    if token_stream.current_kind() == TokenType.semicolon_:
        return MethodExpression(identifier=method_name,
                                parameters=parameters_string,
                                return_part=return_part_string,
                                is_const=Token(TokenType.const_) in after_parameters_tokens)

    token_stream.move_forward_to(TokenType.closing_bracket_)


def parse_constructor(token_stream, expression_context):
    assert token_stream.current_kind() == TokenType.params_begin_
    assert isinstance(expression_context, ClassExpression)
    constructor_identifier = expression_context.identifier

    token_stream.forward()

    parameters_tokens = \
        token_stream.forward_copy_if(lambda stream: stream.current_kind() != TokenType.params_end_)

    parameters_string = convert_param_tokens_to_string(parameters_tokens)

    token_stream.move_forward_to(TokenType.params_end_)
    token_stream.forward()

    if token_stream.current_kind() == TokenType.semicolon_:
        return CTorExpression(identifier=constructor_identifier,
                              parameters=parameters_string)
    else:
        token_stream.move_forward_to(TokenType.closing_bracket_)


def parse_destructor(token_stream, expression_context):
    assert token_stream.current_kind() == TokenType.tilde_
    assert isinstance(expression_context, ClassExpression)

    if expression_context.get_current_scope() != TokenType.public_:
        return None

    destructor_identifier = expression_context.identifier

    token_stream.move_forward_to(TokenType.params_end_)

    token_stream.forward()

    if token_stream.current_kind() == TokenType.semicolon_:
        return DTorExpression(identifier=destructor_identifier)
    else:
        token_stream.move_forward_to(TokenType.closing_bracket_)


def parse_operator(token_stream, expression_context):
    assert token_stream.current_kind() == TokenType.operator_

    if expression_context.get_current_scope() != TokenType.public_:
        return None

    operator_return_tokens = get_return_part_as_tokens(token_stream)
    operator_return_tokens_as_str = convert_param_tokens_to_string(operator_return_tokens)

    assert token_stream.current_kind() == TokenType.operator_

    operator_name = ''
    tokens = token_stream.forward_copy_if(lambda stream: not (stream.current_content() == '('
                                          and stream.right_token(2).content != '('))
    for tok in tokens:
        operator_name += tok.content

    assert token_stream.current_kind() == TokenType.params_begin_
    token_stream.forward()

    operator_params_tokens = token_stream.forward_copy_if(lambda ts: ts.current_kind() != TokenType.params_end_)
    str_params = convert_param_tokens_to_string(operator_params_tokens)

    token_stream.move_forward_to(TokenType.params_end_)

    token_stream.forward()
    if token_stream.current_kind() == TokenType.semicolon_:
        return OperatorExpression(identifier=operator_name,
                                  parameters=str_params,
                                  return_part=operator_return_tokens_as_str)
    else:
        token_stream.move_forward_to(TokenType.closing_bracket_)


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


def build_ast(token_stream):
    ast_tree_root = Expression('Root')
    while token_stream.forward():
        expr = parse_expression(token_stream)
        if expr is not None:
            ast_tree_root.attach(expr)
    return ast_tree_root

