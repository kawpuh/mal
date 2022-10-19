import mal_types
from types import FunctionType as function


def pr_str(ast, print_readable=True):
    if ast is None:
        return "nil"
    if type(ast) is list:
        children = [pr_str(child, print_readable) for child in ast]
        ret = "[" + " ".join(children) + "]"
        return ret
    if type(ast) is dict:
        children = [pr_str(k, print_readable) + " " + pr_str(v, print_readable) for k,v in ast.items()]
        ret = "{" + " ".join(children) + "}"
        return ret
    if type(ast) is mal_types.List:
        children = [pr_str(child, print_readable) for child in ast]
        ret = "(" + " ".join(children) + ")"
        return ret
    if type(ast) is mal_types.MalFunction:
        return "MalFunction: " + pr_str(ast.params,
                                        print_readable) + " -> " + pr_str(
                                            ast.ast, print_readable)
    if type(ast) is mal_types.Symbol:
        return ast.name
    if type(ast) is mal_types.Keyword:
        return ":" + ast.name
    if type(ast) == str:
        if print_readable:
            # When print_readably is true, doublequotes, newlines, and backslashes are translated into their printed representations (the reverse of the reader)
            ast = ast.replace("\\", "\\\\")
            ast = ast.replace("\n", "\\n")
            ast = ast.replace("\"", "\\\"")
            return '"' + ast + '"'
        return ast
    if type(ast) == bool:
        return "true" if ast is True else "false"
    if type(ast) is int:
        return str(ast)
    if type(ast) is function:
        return str()
    print("Can't print: ", type(ast))
    raise NotImplementedError
