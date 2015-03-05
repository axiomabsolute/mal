def prelude():
  return {
    '+': lambda a,b: a+b,
    '-': lambda a,b: a-b,
    '*': lambda a,b: a*b,
    '/': lambda a,b: int(a/b),
    'list': lambda *args: list(args),
    'list?': lambda x, *args: isinstance(x, list),
    'empty?': lambda x, *args: len(x) == 0,
    '=': lambda x,y: x == y,
    'count': lambda x: len(x),
    '<': lambda x,y: x<y,
    '<=': lambda x,y: x<=y,
    '>': lambda x,y: x>y,
    '>=': lambda x,y: x>=y,
    '/=': lambda x,y: x!=y
  }