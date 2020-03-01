from TreeBuilder.Parsing.state_builder import StateParserBuilder


class ClassParserFactory(object):
    @staticmethod
    def get_parser(token_stream):
        state_parser = StateParserBuilder(token_stream). \
            add_class_parsing(). \
            add_dtor_parsing(). \
            add_operator_parsing(). \
            add_params_parsing().\
            get_product()
        return state_parser
