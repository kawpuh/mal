import readline
import reader
import printer
from env import Env
from core import core_env


# TODO: replace err handling
def err(msg):
    print("ERR: ", msg)
    raise BaseException


def is_symbol(val):
    if type(val) == tuple and val[0] == "symbol":
        # We could also verify it's a 2-tuple
        return True
    return False


def eval_ast(env, ast):
    if ast is None:
        return None
    if type(ast) == tuple:
        mal_type, val = ast
        if mal_type == "symbol":
            return env.get(val)
        elif mal_type == "string":
            return val
        elif mal_type == "int":
            return val
        elif mal_type == "bool":
            return val
        elif mal_type == "[":
            return ("[", [EVAL(env, child) for child in val])
        elif mal_type == "{":
            # TODO: implement hashmap
            return ast
        else:
            err(f"can't eval_ast given mal_type: {mal_type}")

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
    if type(ast) == tuple:
        return eval_ast(env, ast)
    if type(ast) == list:
        if len(ast) == 0:
            return ast
        if ast[0][1] == "def!":
            if not is_symbol(ast[1]):
                err("Invalid defn! form: Can only assign to symbol")
            return env.set(ast[1][1], EVAL(env, ast[2]))
        elif ast[0][1] == "let*":
            # TODO: vector binding
            if not len(ast) == 3:
                err(
                    "Invalid let* form: should have 2 args (list of bindings and body)"
                )
            if not type(ast[1]) == list and len(ast[1]) % 2 == 0:
                err(
                    "Invalid let* form: first argument should be list of binding pairs"
                )
            sub_env = Env(env)
            for i in range(0, len(ast[1]), 2):
                (_, symbol_name), val = ast[1][i], EVAL(sub_env, ast[1][i + 1])
                sub_env.set(symbol_name, val)
            return EVAL(sub_env, ast[2])
        elif ast[0][1] == "do":
            for body in ast[1:-1]:
                EVAL(env, body)
            return EVAL(env, ast[-1])
        elif ast[0][1] == "if":
            if len(ast) not in [3, 4]:
                err(
                    f"Invalid if form: Only takes 2 or 3 arguments, got {len(ast)}"
                )
            if EVAL(env, ast[1]) not in [False, None]:
                return EVAL(env, ast[2])
            elif len(ast) == 4:
                return EVAL(env, ast[3])
            else:
                return None
        elif ast[0][1] == "fn*":
            keys = ast[1]
            if type(keys) == tuple and keys[0][0] == "[":
                keys = keys[1]
            return lambda *args: EVAL(Env(env, add_binds=(keys, args)), ast[2])
        else:
            [fn, *args] = eval_ast(env, ast)
            return fn(*args)
    print("Couldn't EVAL ast")
    return BaseException


def PRINT(ast):
    print(printer.pr_str(ast))


def rep(env, s):
    PRINT(EVAL(env, READ(s)))


def main():
    readline.read_init_file()

    while (1):
        try:
            inp = input("user> ")
        except EOFError:
            print("\nExiting...")
            return 0
        readline.add_history(inp)
        try:
            rep(core_env, inp)
        except BaseException:
            print("Continuing...")


if __name__ == "__main__":
    main()
