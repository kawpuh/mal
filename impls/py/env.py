class UnboundSymbolError(BaseException):
    pass


class Env:
    def __init__(self, outer={}, add_binds=None):
        self.outer = outer
        self.data = {}

        if add_binds is not None:
            key_list, val_list = add_binds
            for (_, key_name), val in zip(key_list, val_list):
                self.set(key_name, val)

    def set(self, k, v):
        self.data[k] = v
        return v

    def get(self, k):
        inner_val = self.data.get(k)
        if inner_val is not None:
            return inner_val
        elif self.outer.get(k) is not None:
            return self.outer.get(k)
        else:
            raise UnboundSymbolError
