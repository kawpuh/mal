import readline
import reader
import printer
from core import core_env
import mal_types
import types


# TODO: replace err handling
def err(msg):
    print("ERR: ", msg)
    raise mal_types.MalError


def is_symbol(val):
    if type(val) == tuple and val[0] == "symbol":
        # We could also verify it's a 2-tuple
        return True
    return False


def eval_ast(env, ast):
    if type(ast) is mal_types.Symbol:
        return env.get(ast.name)
    if type(ast) is list:
        return [EVAL(env, child) for child in ast]
    if type(ast) is dict:
        return dict(
            zip((EVAL(env, key) for key in ast.keys()),
                (EVAL(env, val) for val in ast.values())))
    if type(ast) is mal_types.List:
        return [EVAL(env, child) for child in ast.data]

    err(f"can't eval_ast given mal_type: {type(ast)}")


def READ(s):
    try:
        return reader.read_str(s)
    except EOFError:
        print("EOF reached while parsing s-expression")


def EVAL(env, ast):
    while True:
        if type(ast) in (str, int, bool, type(None), mal_types.Keyword):
            return ast
        if type(ast) in (mal_types.Symbol, list, dict):
            return eval_ast(env, ast)
        if type(ast) == mal_types.List:
            if len(ast) == 0:
                return ast
            if type(ast[0]) is mal_types.List:
                [fn_obj, *args] = eval_ast(env, ast)
                if not type(fn_obj) is mal_types.MalFunction:
                    err("ERR: first item in evaluated list must be function")
                ast = fn_obj.ast
                env = mal_types.Env(fn_obj.env, (fn_obj.params, args))
                continue
            if type(ast[0]) is not mal_types.Symbol:
                err("ERR: can only evaluate list beginning with symbol or function"
                    )
            if ast[0].name == "def!":
                if type(ast[1]) is not mal_types.Symbol:
                    err("Invalid defn! form: Can only assign to symbol")
                return env.set(ast[1].name, EVAL(env, ast[2]))
            elif ast[0].name == "let*":
                # TODO: vector binding
                if not len(ast) == 3:
                    err("Invalid let* form: should have 2 args (list of bindings and body)"
                        )
                if not (type(ast[1]) in [list, mal_types.List]
                        and len(ast[1]) % 2 == 0):
                    err("Invalid let* form: first argument should be list of binding pairs"
                        )
                sub_env = mal_types.Env(env)
                for i in range(0, len(ast[1]), 2):
                    symbol, val = ast[1][i], EVAL(sub_env, ast[1][i + 1])
                    sub_env.set(symbol.name, val)
                ast = ast[2]
                env = sub_env
                continue
            elif ast[0].name == "do":
                for body in ast[1:-1]:
                    EVAL(env, body)
                ast = ast[-1]
                continue
            elif ast[0].name == "if":
                if len(ast) not in [3, 4]:
                    err(f"Invalid if form: Only takes 2 or 3 arguments, got {len(ast)-1}"
                        )
                if mal_types.is_true(EVAL(env, ast[1])):
                    ast = ast[2]
                    continue
                elif len(ast) == 4:
                    ast = ast[3]
                    continue
                else:
                    return None
            elif ast[0].name == "fn*":
                keys = ast[1]
                if type(keys) == tuple and keys[0][0] == "[":
                    keys = keys[1]
                return mal_types.MalFunction(
                    ast[2], keys, env, lambda *args: EVAL(
                        mal_types.Env(env, add_binds=(keys, args)), ast[2]))
            elif ast[0].name == "eval":
                if len(ast) != 2:
                    err(f"Invalid eval form: expected 1 argument, ast, got {len(ast)-1}"
                        )
                ast = EVAL(mal_types.Env(env), ast[1])
                # print(f"new ast: {ast}")
                continue
            elif type(ast[0]) is mal_types.Symbol:
                [fn_obj, *args] = eval_ast(env, ast)
                if type(fn_obj) is mal_types.MalFunction:
                    ast = fn_obj.ast
                    env = mal_types.Env(fn_obj.env, (fn_obj.params, args))
                    continue
                elif type(fn_obj) is types.FunctionType:
                    return fn_obj(*args)
                else:
                    print(type(fn_obj))
                    assert 0
        err("Couldn't EVAL ast")


def PRINT(ast):
    print(printer.pr_str(ast, True))


def rep(env, s):
    PRINT(EVAL(env, READ(s)))


def main():
    readline.read_init_file()
    EVAL(core_env, READ("(def! not (fn* (a) (if a false true)))"))
    while (1):
        try:
            inp = input("user> ")
        except EOFError:
            print("\nExiting...")
            return 0
        readline.add_history(inp)
        try:
            rep(core_env, inp)
        except mal_types.MalError:
            print("Continuing...")


if __name__ == "__main__":
    main()
