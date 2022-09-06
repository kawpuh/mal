def pr_str(ast):
    if ast is None:
        return "nil"
    if type(ast) == list:
        children = [pr_str(child) for child in ast]
        ret = "(" + " ".join(children) + ")"
        return ret
    elif type(ast) == tuple:
        if ast[0] == "[":
            children = [pr_str(child) for child in ast[1]]
            return "[" + " ".join(children) + "]"
        elif ast[0] == "{":
            # TODO: implement hashmap
            return "Unimplemented Hashmap"
        else:
            raise NotImplementedError
    elif type(ast) == str:
        return '"' + ast + '"'
    elif type(ast) == bool:
        return "true" if ast is True else "false"
    else:
        # should only be a number
        return str(ast)
