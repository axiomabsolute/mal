from reader import Keyword

def pr_str(mal):
  # If it's a list, map str over elements, join with spaces and surround parens
  # Otherwise just str it.
  if isinstance(mal, list):
    return'(' + ' '.join([pr_str(x) for x in mal]) + ')'
  elif isinstance(mal, tuple):
    return '[' + ' '.join([pr_str(x) for x in mal]) + ']'
  elif isinstance(mal, str):
    return ('"%s"' % mal)
  elif mal == None:
    return 'nil'
  elif isinstance(mal, bool):
    if mal == True:
      return 'true'
    else:
      return 'false'
  elif isinstance(mal, Keyword):
    return ":" + mal.token
  elif isinstance(mal, dict):
    return "{%s}" % (" ".join(["%s %s" % (pr_str(k),pr_str(v)) for k,v in mal.iteritems()]))
  else:
    return repr(mal)