from stateBase import State
from TreeBuilder.tok import TokenType
from stateBuilder import StateParserBuilder
from TreeBuilder.expressions import ClassExpression


class ClassState(State):
    def __init__(self, token_stream, context):
        State.__init__(self, TokenType.class_, token_stream, context)

    def handle(self):
        # we have class already
        self._forward()

        # consume identifier
        if self._current_kind() != TokenType.identifier_:
            raise Exception("Identifier expected after class keyword")

        # we have identifier
        parsed_class = ClassExpression(self._current_content())

        self._forward()

        # we have something...

        # ...maybe forwarded class
        if self._current_kind() == TokenType.semicolon_:
            return None

        # ...move after opening bracket
        while self._current_kind() != TokenType.opening_bracket_:
            self._forward()

        # currentToken == token.opening_brackets

        state_parser = StateParserBuilder(self._token_stream, parsed_class). \
            add_class_parsing(). \
            add_dtor_parsing(). \
            add_operator_parsing(). \
            add_params_parsing(). \
            get_product()

        while self._forward():

            # friend inside class
            if self._current_kind() == TokenType.friend_:
                parsed_class.set_friend_inside()

            # take care of public, prot, private
            parsed_class.set_scope(self._current_kind())

            # we're done
            if self._current_kind() == TokenType.closing_bracket_:
                break

            expr = state_parser.process()
            if expr is None:
                continue
            parsed_class.attach(expr)

        return parsed_class
