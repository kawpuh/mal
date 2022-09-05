import re


class Reader:

    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        self.len = len(tokens)

    def next(self):
        if self.i >= self.len:
            raise EOFError
        ret = self.tokens[self.i]
        self.i += 1
        return ret

    def peek(self):
        if self.i >= self.len:
            raise EOFError
        return self.tokens[self.i]


tokenizer_re = r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)"""


def tokenize(s):
    return [token for token in re.split(tokenizer_re, s) if not token == '']


OPENING_BRACKETS = ("(", "[", "{")
CLOSING_BRACKETS = {"(": ")", "[": "]", "{": "}"}


def read_list(reader):
    opening = reader.next()
    closing = CLOSING_BRACKETS[opening]
    ret = []
    while reader.peek()[0] != closing:
        ret.append(read_form(reader))
    reader.next()

    if opening == "(":
        return ret
    else:
        return (opening, ret)


def read_atom(reader):
    val = reader.next()
    # We're using 2-tuples as a hacky way to implement typed values as (type, val)
    if '0' <= val[0] <= '9' or (val[0] == '-' and len(val) > 1
                                and '0' <= val[1] <= '9'):
        # TODO: catch and handle ValueError if invalid number literal
        return ("int", int(val))
    elif val[0] == '"':
        if not (val[-1] == '"' and len(val) > 1):
            raise EOFError
        return ("string", val[1:-1])
    elif val == "nil":
        return None
    elif val in ("True", "False"):
        return ("bool", True if val == "True" else False)
    else:
        return ("symbol", val)


def read_form(reader):
    if reader.peek()[0] in OPENING_BRACKETS:
        return read_list(reader)
    else:
        return read_atom(reader)


def read_str(s):
    reader = Reader(tokenize(s))
    return read_form(reader)
    # return tokenize(s)
