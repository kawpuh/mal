class UnboundSymbolError(BaseException):
    pass


class Env:
    def __init__(self, outer=None):
        self.outer = outer
        self.data = {}

    def set(self, k, v):
        self.data[k] = v
        return v

    def get(self, k):
        inner_val = self.data.get(k)
        if inner_val is not None:
            return inner_val
        elif self.outer is not None:
            return self.outer.get(k)
        else:
            raise UnboundSymbolError
