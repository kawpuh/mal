class List:

    def __init__(self, from_listlike):
        self.data = list(from_listlike)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, n):
        return self.data[n]

    def __eq__(self, o):
        if not (getattr(o, "__getitem__", False)
                and getattr(o, "__len__", False)):
            return False
        if len(self) != len(o):
            return False
        for self_item, o_item in zip(self, o):
            if self_item != o_item:
                return False
        return True

    def __str__(self):
        return "MalList: (" + " ".join(str(item) for item in self.data) + ")"

class Symbol:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "MalSymbol: " + self.name

class Keyword:

    def __init__(self, name):
        self.name = name

    def __eq__(self, o):
        return type(o) is type(self) and self.name == o.name

    def __hash__(self):
        return self.name.__hash__()


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


class MalFunction:

    def __init__(self, ast, params, env, ogfn):
        self.ast = ast
        self.params = params
        self.env = env
        self.ogfn = ogfn


def is_true(val):
    if type(val) is bool and val == False:
        return False
    if val is None:
        return False
    return True
