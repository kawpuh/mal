import readline
import reader
import printer


class UnboundSymbolError(BaseException):
    pass


def READ(s):
    try:
        return reader.read_str(s)
    except EOFError:
        print("EOF reached while parsing s-expression")


def eval_ast(env, ast):
    if type(ast) == tuple:
        if ast[0] == "symbol":
            try:
                return env[ast[1]]
            except KeyError:
                raise UnboundSymbolError
        elif ast[0] == "string":
            return ast[1]
        elif ast[0] == "int":
            return ast[1]
        elif ast[0] == "[":
            return ("[", [EVAL(env, child) for child in ast[1]])
        elif ast[0] == "{":
            # TODO: implement hashmap
            return ast
        else:
            raise NotImplementedError
    elif type(ast) == list:
        return [EVAL(env, child) for child in ast]
    elif type(ast) == int:
        return ast
    assert 0


def EVAL(env, ast):
    if type(ast) == list:
        if len(ast) == 0:
            return ast
        else:
            [fn, *args] = eval_ast(env, ast)
            return fn(*args)
    elif type(ast) == tuple:
        return eval_ast(env, ast)


def PRINT(ast):
    print(printer.pr_str(ast))


repl_env = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: int(a / b)
}


def rep(s):
    PRINT(EVAL(repl_env, READ(s)))


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
            rep(inp)
        except UnboundSymbolError:
            print("Referenced Unbound Symbol\n")


if __name__ == "__main__":
    main()
