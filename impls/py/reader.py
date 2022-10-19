import re
import mal_types


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


def read_bracketed(reader):
    opening = reader.next()
    closing = CLOSING_BRACKETS[opening]
    ret = []
    while reader.peek()[0] != closing:
        ret.append(read_form(reader))
    reader.next()

    if opening == "(":
        return mal_types.List(ret)
    if opening == "[":
        return ret
    else:  # opening "{"
        if not len(ret) % 2 == 0:
            print(f"ERR: hashmap literal with non-even number of forms ({len(ret)})")
            raise mal_types.MalError
        hm = dict()
        for key, val in zip(ret[:1:], ret[1:]):
            hm[key] = val
        return hm


def read_atom(reader):
    val = reader.next()
    if '0' <= val[0] <= '9' or (val[0] == '-' and len(val) > 1
                                and '0' <= val[1] <= '9'):
        try:
            return int(val)
        except ValueError:
            print(f"Invalid number literal: {str(val)}")
            raise mal_types.MalError
    elif val[0] == '"':
        if not (val[-1] == '"' and len(val) > 1):
            raise EOFError
        ret = val[1:-1]
        # When a string is read, the following transformations are applied:
        # a backslash followed by a doublequote is translated into a plain doublequote character
        ret = ret.replace("\\\"", "\"")
        # a backslash followed by "n" is translated into a newline
        ret = ret.replace("\\\n", "\n")
        # a backslash followed by another backslash is translated into a single backslash.
        ret = ret.replace("\\\\", "\\")
        return ret
    elif val[0] == ":":
        return mal_types.Keyword(val[1:])
    elif val == "nil":
        return None
    elif val in ("true", "false"):
        return True if val == "true" else False
    else:
        return mal_types.Symbol(val)


def read_form(reader):
    if reader.peek()[0] in OPENING_BRACKETS:
        return read_bracketed(reader)
    else:
        return read_atom(reader)


def read_str(s):
    reader = Reader(tokenize(s))
    return read_form(reader)
