class Env:
  def __init__(self, outer, data={}, binds=[], exprs=[]):
    # Something about `binds and exprs`.  not sure what that means...
    self.outer = outer
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