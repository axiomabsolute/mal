import cmd
import reader
import printer
import sys
import traceback
import env as environment
from itertools import izip
from core import prelude
from reader import Symbol
import logging

class Fn:
  def __init__(self, fn, ast, params, env):
    self.fn = fn
    self.ast = ast
    self.params = params
    self.env = env

class Mal(cmd.Cmd):
  """Command line interpreter for the Mal programming language"""

  def __init__(self):
    self.prompt = "mal-user> "
    self.repl_env = environment.Env(None, prelude())
    logging.basicConfig(format='  <%(levelname)s>\t%(message)s')
    self._logger = logging.getLogger()
    cmd.Cmd.__init__(self)

  def do_EOF(self, params):
    return True

  def do_exit(self, params):
    return self.do_EOF(params)

  def READ(self, param):
    return reader.read_str(param)

  def eval_ast(self, ast, env):
    if isinstance(ast, reader.Keyword):
      return ast.token
    if isinstance(ast, reader.Symbol):
      return env.get(ast.token)
    if isinstance(ast, list):
      return [self.EVAL(a, env) for a in ast]
    if isinstance(ast, tuple):
      return tuple([self.EVAL(a,env) for a in ast])
    if isinstance(ast, dict):
      return {self.EVAL(k, env):self.EVAL(v, env) for k,v in ast.iteritems()}
    return ast

  def EVAL(self, ast, env):
    while True:
      if isinstance(ast, list):
        if len(ast) == 0:
          return []
        # Begin the special forms
        # Find a cleaner way to do this :(
        if isinstance(ast[0], reader.Symbol):
          if ast[0].token == "def!":
            return env.set(ast[1].token, self.EVAL(ast[2], env))
          if ast[0].token == "let*":
            let_env = environment.Env(env)
            pairs = izip(*[iter(ast[1])]*2)
            for pair in pairs:
              let_env.set(pair[0].token, self.EVAL(pair[1], let_env))
            env = let_env
            ast = ast[2]
            continue
          if ast[0].token == "do":
            last = None
            for item in ast[1:-1]:
              last = self.EVAL(item, env)
            ast = ast[-1]
            continue
          if ast[0].token == "if":
            cond = self.EVAL(ast[1], env)
            if cond == None or (isinstance(cond, bool) and cond == False):
              if len(ast) == 4:
                ast = ast[3]
                continue
              ast = None
              continue
            else:
              ast = ast[2]
              continue
          if ast[0].token == "fn*":
            logging.debug("Special form: fn*")
            fn = lambda *args: self.EVAL(ast[2], environment.Env(env, binds=[x.token for x in ast[1]], exprs=args))
            return Fn(fn, ast[2], ast[1], env)
        if isinstance(ast[0], reader.Keyword):
          if isinstance(ast[1], dict):
            key = self.eval_ast(ast[0], env)
            dics = [self.eval_ast(x, env) for x in ast[1:]]
            res = [dic[key] if key in dic else None for dic in dics]
            if len(res) == 1:
              return res[0]
            return res
            return None
          return None
        prep = self.eval_ast(ast, env)
        if isinstance(prep[0], Fn):
          fnstar = prep[0]
          ast = fnstar.ast
          env = environment.Env(outer=fnstar.env, binds=[x.token for x in fnstar.params], exprs=prep[1:])
          continue
        else:
          return self.apply(prep)
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

  def do_debug(self, param):
    logger = self._logger
    if param == None:
      if logger.getEffectiveLevel() == logging.DEBUG:
        logger.setLevel(logging.WARNING)
      else:
        logger.setLevel(logging.DEBUG)
    else:
      if bool(param):
        logger.setLevel(logging.DEBUG)
      else:
        logger.setLevel(logging.WARNING)
    print("DEBUG MODE: %s" % (logger.getEffectiveLevel() == logging.DEBUG))

if __name__ == "__main__":
  mal = Mal()
  garbage = mal.do_rep("(def! not (fn* (a) (if a false true)))")
  # garbage = mal.do_debug(None)
  mal.cmdloop()
  print("DONE")