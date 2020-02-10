import enum


class TokenType(enum.Enum):
    identifier_ = 1,
    namespace_ = 2,
    class_ = 3,
    struct_ = 4,
    semicolon_ = 5,         # ;
    colon_ = 6,             # :
    opening_bracket_ = 7,   # {
    closing_bracket_ = 8,   # }
    params_begin_ = 9,      # (
    params_end_ = 10,       # )
    public_ = 11,
    private_ = 12,
    protected_ = 13,
    comma_ = 14,            # ,
    eof_ = 15,
    ref_ = 16,              # &,
    star_ = 17,             # *
    hash_ = 18,             # #
    tilde_ = 19,            # ~
    const_ = 20,
    equal_ = 21,
    typedef_ = 22,
    typename_ = 23,
    virtual_ = 24,
    friend_ = 25,
    template_ = 26,
    operator_ = 27


class Token:
    def __init__(self, kind, content=""):
        self.kind = kind
        self.content = content

    def __eq__(self, other):
        if self.kind == TokenType.identifier_:
            return self.kind == other.kind and self.content == other.content
        else:
            return self.kind == other.kind
