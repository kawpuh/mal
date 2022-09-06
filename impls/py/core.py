from functools import reduce
from mal_types import Env


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


core_env = Env()
core_env.set('+', _make_variadic_reducable(lambda a, b: a + b))
core_env.set('-', _make_variadic_reducable(lambda a, b: a - b))
core_env.set('*', _make_variadic_reducable(lambda a, b: a * b))
core_env.set('/', _make_variadic_reducable(lambda a, b: a // b))
core_env.set('=', _make_variadic_compare(lambda a, b: a == b))
core_env.set('>=', _make_variadic_compare(lambda a, b: a >= b))
core_env.set('<=', _make_variadic_compare(lambda a, b: a <= b))
core_env.set('>', _make_variadic_compare(lambda a, b: a > b))
core_env.set('<', _make_variadic_compare(lambda a, b: a < b))
