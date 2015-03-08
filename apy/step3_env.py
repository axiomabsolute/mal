import cmd
import reader
import printer
import sys
import traceback
import env as environment
from itertools import izip

class Mal(cmd.Cmd):
  """Command line interpreter for the Mal programming language"""

  def __init__(self):
    self.prompt = "mal-user> "
    self.repl_env = environment.Env(None, {
      '+': lambda a,b: a+b,
      '-': lambda a,b: a-b,
      '*': lambda a,b: a*b,
      '/': lambda a,b: int(a/b)
    })
    cmd.Cmd.__init__(self)

  def do_EOF(self, params):
    return True

  def do_exit(self, params):
    return self.do_EOF(params)

  def READ(self, param):
    return reader.read_str(param)

  def eval_ast(self, ast, env):
    if isinstance(ast, reader.Symbol):
      return env.get(ast.token)
    if isinstance(ast, list):
      return [self.EVAL(a, env) for a in ast]
    return ast

  def EVAL(self, ast, env):
    if isinstance(ast, list):
      if len(ast) == 0:
        return
      elif isinstance(ast[0], reader.Symbol) and ast[0].token == "def!":
        value = self.EVAL(ast[2], env)
        env.set(ast[1].token, value)
        return value
      elif isinstance(ast[0], reader.Symbol) and ast[0].token == "let*":
        let_env = environment.Env(env)
        pairs = izip(*[iter(ast[1])]*2)
        for pair in pairs:
          let_env.set(pair[0].token, self.EVAL(pair[1], let_env))
        return self.EVAL(ast[2], let_env)
      else:
        prep = self.eval_ast(ast, env)
        return self.apply(prep)
    elif isinstance(ast, tuple):
      return tuple([self.EVAL(x, env) for x in ast])
    elif isinstance(ast, dict):
      return {k:self.EVAL(v, env) for (k,v) in ast.iteritems()}
    else:
      return self.eval_ast(ast, env)

  def apply(self, sexp):
    return sexp[0](*sexp[1:])

  def PRINT(self, param):
    return printer.pr_str(param)

  def do_rep(self, param):
    print(self.PRINT(self.EVAL(self.READ(param), self.repl_env)))

  def do_printenv(self, param):
    print(self.repl_env)

  def default(self, line):
    try:
      return self.do_rep(line)
    except Exception as e:
      print("".join(traceback.format_exception(*sys.exc_info())))

if __name__ == "__main__":
  Mal().cmdloop()
  print("DONE")