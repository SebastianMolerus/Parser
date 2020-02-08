import enum


class TokenType(enum.Enum):

    _identifier      =   1,
    _namespace       =   2,
    _class           =   3,
    _struct          =   4,
    _semicolon       =   5,     # ;
    _colon           =   6,     # :
    _opening_bracket =   7,     # {
    _closing_bracket =   8,     # }
    _params_begin    =   9,     # (
    _params_end      =   10,    # )
    _public          =   11,
    _private         =   12,
    _protected       =   13,
    _comma           =   14,    # ,
    _eof             =   15,
    _ref             =   16,    # &,
    _star            =   17,    # *
    _preproc         =   18,    # #
    _tilde           =   19,    # ~
    _const           =   20,
    _equal           =   21,
    _typedef         =   22,
    _typename        =   23,
    _virtual         =   24,
    _friend          =   25,
    _template        =   26,
    _operator        =   27


class Token:

    def __init__(self, type, content = ""):
        self.type = type
        self.content = content

    
    def __eq__(self, other):
        if self.type == TokenType._identifier:
            return self.type == other.type and self.content == other.content
        else:
            return self.type == other.type