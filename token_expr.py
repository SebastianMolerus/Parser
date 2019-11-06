class TokExpr:
    def __init__(self, tokType, content):
        self._type = tokType
        self._content = content

    @property
    def type(self):
        return self._type
    
    @property
    def content(self):
        return self._content