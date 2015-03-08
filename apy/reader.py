import re

token_pcre = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"|;.*|[^\s\[\]{}()'"`@,;]+)""")

class Reader:
  def __init__(self, tokens):
    self.tokens = tokens
    self.position = 0

  def next(self):
    res = self.tokens[self.position]
    self.position += 1
    return res

  def peek(self):
    return self.tokens[self.position]

class Symbol:
  def __init__(self, token):
    self.token = token

  def __str__(self):
    return "Symbol(%s)" % self.token

  def __repr__(self):
    return self.token

class Keyword:
  def __init__(self, token):
    self.token = token[1:]

  # def __str__(self):
  #   return self.token

  # def __repr__(self):
  #   return repr(self.token)

def read_str(inp):
  tokens = tokenizer(inp)
  reader = Reader(tokens)
  return read_form(reader)

def tokenizer(inp):
  tokens = token_pcre.findall(inp)
  if tokens[0].startswith(";"):
    return []
  return tokens

def read_form(reader):
  curr_token = reader.peek()
  if curr_token == "(":
    return read_list(reader)
  elif curr_token == "[":
    return read_vector(reader)
  elif curr_token == "{":
    return read_map(reader)
  else:
    return read_atom(reader)

# reader should be ON '('
def read_list(reader):
  return read_seq(reader, ")")

def read_vector(reader):
  return tuple(read_seq(reader, "]"))

def read_seq(reader, end_sigil):
  reader.next()
  res = []
  try:
    while reader.peek() != end_sigil:
      res.append(read_form(reader))
    reader.next() # Skip over closing sigil
    return res
  except IndexError:
    print("Unmatched '%s' token." % end_sigil)

# Should be on '{'
def read_map(reader):
  reader.next()
  res = {}
  try:
    while reader.peek() != "}":
      key = read_form(reader)
      value = read_form(reader)
      res[key] = value
    reader.next() # Skip over closing sigil
    return res
  except IndexError:
    print("Unmatched '}' token.")

def read_atom(reader):
  curr_token = reader.next()
  if curr_token == "true":
    return True
  elif curr_token == "false":
    return False
  elif curr_token == "nil":
    return None
  else:
    return parse_atom(curr_token, [parse_int,
              parse_float,
              parse_string,
              parse_keyword,
              lambda inp: Symbol(inp)])

def parse_atom(inp, parsers):
  for parser in parsers:
    res = parser(inp)
    if res != None:
      return res

def parse_int(inp):
  try:
    res = int(inp)
    return int(inp)
  except Exception:
    return None

def parse_float(inp):
  try:
    return float(inp)
  except Exception:
    None

def parse_string(inp):
  if inp.startswith("\"") and inp.endswith("\""):
    return inp[1:-1]
  return None

def parse_keyword(inp):
  if inp.startswith(":"):
    return Keyword(inp)
  return None
