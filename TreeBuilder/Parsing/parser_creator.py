from TreeBuilder.Parsing.stateBuilder import StateParserBuilder


class ParserCreator(object):
    def __init__(self):
        pass

    def get_parser(self):
        raise NotImplementedError


class ClassParserCreator(ParserCreator):
    def get_parser(self, token_stream):
        state_parser = StateParserBuilder(token_stream). \
            add_class_parsing(). \
            add_dtor_parsing(). \
            add_operator_parsing(). \
            add_params_parsing().\
            get_product()
        return state_parser
