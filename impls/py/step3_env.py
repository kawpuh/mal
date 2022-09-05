import readline
import reader
import printer
from env import Env, UnboundSymbolError
from functools import reduce


def is_symbol(val):
    if type(val) == tuple and val[0] == "symbol":
        # We could also verify it's a 2-tuple
        return True
    return False


def eval_ast(env, ast):
    if type(ast) == tuple:
        mal_type, val = ast
        if mal_type == "symbol":
            try:
                return env.get(val)
            except KeyError:
                raise UnboundSymbolError
        elif mal_type == "string":
            return val
        elif mal_type == "int":
            return val
        elif mal_type == "[":
            return ("[", [EVAL(env, child) for child in val])
        elif mal_type == "{":
            # TODO: implement hashmap
            return ast
        else:
            raise NotImplementedError

    elif type(ast) == list:
        return [EVAL(env, child) for child in ast]

    elif type(ast) == int:
        return ast
    assert 0


def READ(s):
    try:
        return reader.read_str(s)
    except EOFError:
        print("EOF reached while parsing s-expression")


def EVAL(env, ast):
    # TODO: Replace BaseException with proper exceptions
    if type(ast) == list:
        if len(ast) == 0:
            return ast
        if not is_symbol(ast[0]):
            print("Invalid list form: begins with non-symbol token")
            raise BaseException

        if ast[0][1] == "def!":
            if not is_symbol(ast[1]):
                print("Invalid defn! form: Can only assign to symbol")
                raise BaseException
            return env.set(ast[1][1], EVAL(env, ast[2]))
        elif ast[0][1] == "let*":
            # TODO: vector binding
            if not len(ast) == 3:
                print("Invalid let* form: should have 2 args (list of bindings and body)")
                raise BaseException
            if not type(ast[1]) == list and len(ast[1]) % 2 == 0:
                print("Invalid let* form: first argument should be list of binding pairs")
                raise BaseException
            sub_env = Env(env)
            for i in range(0, len(ast[1]), 2):
                (_, symbol_name), val = ast[1][i], EVAL(sub_env, ast[1][i+1])
                sub_env.set(symbol_name, val)
            return EVAL(sub_env, ast[2])
        else:
            [fn, *args] = eval_ast(env, ast)
            return fn(*args)
    elif type(ast) == tuple:
        return eval_ast(env, ast)


def PRINT(ast):
    print(printer.pr_str(ast))


def _make_variadic(fn):
    return lambda *args: reduce(fn, args)


repl_env = Env()


def rep(s):
    PRINT(EVAL(repl_env, READ(s)))


def main():
    readline.read_init_file()

    # Setup Environment
    repl_env.set('+', _make_variadic(lambda a, b: a+b))
    repl_env.set('-', _make_variadic(lambda a, b: a - b))
    repl_env.set('*', _make_variadic(lambda a, b: a * b))
    repl_env.set('/', _make_variadic(lambda a, b: a // b))
    while (1):
        try:
            inp = input("user> ")
        except EOFError:
            print("\nExiting...")
            return 0
        readline.add_history(inp)
        try:
            rep(inp)
        except UnboundSymbolError:
            print("Referenced Unbound Symbol\n")
        except BaseException:
            print("TODO error")


if __name__ == "__main__":
    main()
