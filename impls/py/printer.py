def pr_str(ast):
  if type(ast) == list:
    children = [pr_str(child) for child in ast]
    ret = "(" + " ".join(children) + ")"
    return ret
  elif type(ast) == tuple:
    if ast[0] == "symbol":
      return ast[1]
    elif ast[0] == "string":
      return '"' + ast[1] + '"'
    elif ast[0] == "[":
      children = [pr_str(child) for child in ast[1]]
      return "[" + " ".join(children) + "]"
    elif ast[0] == "{":
      # TODO: implement hashmap
      return "Unimplemented Hashmap"
    else:
      raise NotImplementedError
  else:
    # should only be a number
    return str(ast)
