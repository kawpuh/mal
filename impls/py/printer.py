CLOSING_BRACKETS = {
  "(" : ")",
  "[" : "]",
  "{" : "}"
}
def pr_str(ast):
  if type(ast) == list:
    opening = ast[0]
    ast = ast[1:]
    ret = opening
    children = [pr_str(child) for child in ast]
    ret += " ".join(children) + CLOSING_BRACKETS[opening]
    return ret
  elif type(ast) == tuple:
    if ast[0] == "symbol":
      return ast[1]
    elif ast[0] == "string":
      return '"' + ast[1] + '"'
    else:
      raise NotImplementedError
  else:
    return str(ast)
