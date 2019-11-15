class CtorExpr:
    def __init__(self, name, params):
        self.name = name
        self.params = params
        print "CtorExpr (%s) created." % (self.name)

class CopyCtorExpr:
    def __init__(self, name, params):
        self.name = name
        self.params = params
        print "CopyCtorExpr (%s) created." % (self.name)

class AssignOpExpr:
    def __init__(self, params, returns):
        self.params = params
        self.returns = returns
        print "AssignOpExpr operator= created. Params(%s) / Returns(%s)" % (self.params, self.returns)

class MethodExpr:
    def __init__(self, name, params, pre_spec, post_spec):
        self.name = name
        self.params = params
        self.pre_spec = pre_spec
        self.post_spec = post_spec
        print "MethodExpr (%s) created" % (self.name)