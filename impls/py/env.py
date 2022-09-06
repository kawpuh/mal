class NotFound:
    pass


class Env:
    def __init__(self, outer=None, add_binds=None):
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
        inner_val = self.data.get(k, NotFound)
        if inner_val is not NotFound:
            return inner_val

        if self.outer is not None:
            outer_val = self.outer.get(k, NotFound)
            if outer_val is not NotFound:
                return outer_val

        print(f"ERR: Binding for {k} not found")
        raise BaseException
