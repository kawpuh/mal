import mal_types
from types import FunctionType as function


def pr_str(ast, print_readable=True):
    if ast is None:
        return "nil"
    if type(ast) is list:
        children = [pr_str(child) for child in ast]
        ret = "[" + " ".join(children) + "]"
        return ret
    if type(ast) is mal_types.List:
        children = [pr_str(child) for child in ast]
        ret = "(" + " ".join(children) + ")"
        return ret
    if type(ast) is mal_types.Keyword:
        return ":" + ast.name
    if type(ast) == str:
        return '"' + ast + '"' if print_readable is True else ast
    if type(ast) == bool:
        return "true" if ast is True else "false"
    if type(ast) is dict:
        return str(ast)
    if type(ast) is int:
        return str(ast)

    if type(ast) is function:
        return str()
    print("Can't print: ", type(ast))
    raise NotImplementedError
