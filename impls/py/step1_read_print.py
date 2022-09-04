import readline
import reader
import printer


def READ(s):
    try:
        return reader.read_str(s)
    except EOFError:
        print("EOF reached while parsing s-expression")


def EVAL(ast):
    return ast


def PRINT(ast):
    print(printer.pr_str(ast))


def rep(s):
    PRINT(EVAL(READ(s)))


def main():
    readline.read_init_file()
    while (1):
        try:
            inp = input("user> ")
        except EOFError:
            print("\nExiting...")
            return 0
        readline.add_history(inp)
        rep(inp)


if __name__ == "__main__":
    main()
