class List:

    def __init__(self, from_listlike):
        self.data = list(from_listlike)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, n):
        return self.data[n]

    def __eq__(self, o):
        if not (getattr(o, "__getitem__", False) and getattr(
                o, "__len__", False)):
            return False
        if len(self) != len(o):
            return False
        for self_item, o_item in zip(self, o):
            if self_item != o_item:
                return False
        return True


class Symbol:

    def __init__(self, name):
        self.name = name


class Keyword:

    def __init__(self, name):
        self.name = name

    def __eq__(self, o):
        return type(o) is type(self) and self.name == o.name


class MalError(BaseException):
    pass


class NotFound:
    pass


class Env:

    def __init__(self, outer=None, add_binds=None):
        self.outer = outer
        self.data = {}

        if add_binds is not None:
            if type(add_binds) is dict:
                keys, vals = add_binds.keys(), add_binds.values()
            elif type(add_binds) in [tuple, list] and len(add_binds) == 2:
                keys, vals = add_binds
            else:
                print("Invalid Environment Binding: ", add_binds)
                assert 0
            for key, val in zip(keys, vals):
                self.set(key.name, val)

    def set(self, k, v):
        self.data[k] = v
        return v

    def get(self, k):
        inner_val = self.data.get(k, NotFound)
        if inner_val is not NotFound:
            return inner_val

        if self.outer is not None:
            outer_val = self.outer.get(k)
            # if NotFound the error will bubble-up
            return outer_val

        print(f"ERR: Binding for {k} not found")
        raise MalError
