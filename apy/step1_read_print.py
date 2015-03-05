import cmd
import reader
import printer

class Mal(cmd.Cmd):
  """Command line interpreter for the Mal programming language"""

  def __init__(self):
    self.prompt = "mal-user> "
    cmd.Cmd.__init__(self)

  def do_EOF(self, params):
    return True

  def do_exit(self, params):
    return self.do_EOF(params)

  def READ(self, param):
    return reader.read_str(param)

  def EVAL(self, param):
    return param

  def PRINT(self, param):
    return printer.pr_str(param)

  def do_rep(self, param):
    print(self.PRINT(self.EVAL(self.READ(param))))

  def default(self, line):
    try:
      return self.do_rep(line)
    except Exception as e:
      print(e)

if __name__ == "__main__":
  Mal().cmdloop()
  print("DONE")