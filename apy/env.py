class Env:
  def __init__(self, outer, data={}, binds=[], exprs=[]):
    # Something about `binds and exprs`.  not sure what that means...
    self.outer = outer
    # Special case if binds contains a '&'
    # binds may only contain '&' as the second to last symbol
    # all remaining expressions get bound to the last symbol as list
    if '&' in binds:
      if binds[-2] != '&':
        raise Exception('Syntax Error: variadic argument must appear as last parameter in binding list.')
      var_arg_idx = len(binds)-2
      reg_args = binds[:var_arg_idx]
      var_arg = binds[-1]
      self.data = dict(data.items() + zip(reg_args, exprs[:var_arg_idx]) + [(var_arg, exprs[var_arg_idx:])])
    # Otherwise, just another day in the neighborhood
    else:
      self.data = dict(data.items() + zip(binds, exprs))

  def set(self, sym, val):
    self.data[sym] = val

  def find(self, sym):
    if self.data == None:
      return {}
    if sym in self.data:
      return self.data
    if self.outer == None:
      return {}
    return self.outer.find(sym)

  def get(self, sym):
    return self.find(sym)[sym]

  def __str__(self):
    return str(self.data)

  def __repr__(self):
    return repr(self.data)