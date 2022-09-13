from functools import reduce
import mal_types
from mal_types import Env
import printer


def _make_variadic_reducable(fn):
    return lambda *args: reduce(fn, args)


def _make_variadic_compare(fn):

    def variadic_compare(*args):
        prev = args[0]
        for val in args[1:]:
            if fn(prev, val):
                prev = val
            else:
                return False
        return True

    return variadic_compare


pre = {
    mal_types.Symbol('+'):
    _make_variadic_reducable(lambda a, b: a + b),
    mal_types.Symbol('-'):
    _make_variadic_reducable(lambda a, b: a - b),
    mal_types.Symbol('*'):
    _make_variadic_reducable(lambda a, b: a * b),
    mal_types.Symbol('/'):
    _make_variadic_reducable(lambda a, b: a // b),
    mal_types.Symbol('='):
    _make_variadic_compare(lambda a, b: a == b),
    mal_types.Symbol('>='):
    _make_variadic_compare(lambda a, b: a >= b),
    mal_types.Symbol('<='):
    _make_variadic_compare(lambda a, b: a <= b),
    mal_types.Symbol('>'):
    _make_variadic_compare(lambda a, b: a > b),
    mal_types.Symbol('<'):
    _make_variadic_compare(lambda a, b: a < b),

    mal_types.Symbol("pr-str"):
    lambda *args: " ".join(printer.pr_str(arg) for arg in args),
    mal_types.Symbol("str"):
    lambda *args: "".join(printer.pr_str(arg, False) for arg in args),
    mal_types.Symbol("prn"):
    lambda *args: print(*args),
    mal_types.Symbol("list"):
    lambda *args: mal_types.List(args),
    mal_types.Symbol("list?"):
    lambda maybeL: type(maybeL) is mal_types.List,
    mal_types.Symbol("empty?"):
    lambda l: True if l is None else len(l) == 0,
    mal_types.Symbol("count"):
    lambda l: 0 if l is None or not getattr(l, "__len__", False) else len(l),
}
core_env = Env(add_binds=pre)
