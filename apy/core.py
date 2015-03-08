from printer import pr_str

def prelude():
  return {
    '+': lambda a,b: a+b,
    '-': lambda a,b: a-b,
    '*': lambda a,b: a*b,
    '/': lambda a,b: int(a/b),
    'list': lambda *args: list(args),
    'list?': lambda x, *args: isinstance(x, list),
    'empty?': lambda x, *args: len(x) == 0,
    '=': lambda x,y: are_eq(x,y),
    'count': lambda x: len(x) if x != None else 0,
    '<': lambda x,y: x<y,
    '<=': lambda x,y: x<=y,
    '>': lambda x,y: x>y,
    '>=': lambda x,y: x>=y,
    '/=': lambda x,y: x!=y,
    'pr-str': lambda *args: prstr(*args),
    'prn': lambda *args: prn(*args)
  }

def prstr(*args):
    return " ".join([pr_str(arg) for arg in args])

def prn(*args):
    print(prstr(*args))
    return None

def are_eq(x,y):
    try:
        if len(x) != len(y):
            return False
        for xys in zip(x,y):
            if xys[0] != xys[1]:
                return False
        return True
    except:
        return x == y